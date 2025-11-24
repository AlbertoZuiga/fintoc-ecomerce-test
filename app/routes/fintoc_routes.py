import os
import uuid
import json
import requests
from flask import Blueprint, request, jsonify

from app.models.product import Product
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.extensions import fintoc_ecomerce_db

fintoc_bp = Blueprint("fintoc", __name__)


DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data.json')


def load_data():
    try:
        if not os.path.exists(DATA_FILE):
            return {"payment_intents": [], "events": [], "orders": []}
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"payment_intents": [], "events": [], "orders": []}


def save_data(data: dict):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print('Error saving data file:', e)


def _fintoc_post(path: str, payload: dict, idempotency_key: str | None = None):
    base = "https://api.fintoc.com/v1"
    url = f"{base}{path}"
    headers = {
        "Authorization": f"Bearer {os.getenv('FINTOC_SECRET_KEY')}",
        "Content-Type": "application/json",
    }
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
    except requests.RequestException as e:
        print(f"Error contactando Fintoc ({url}): {e}")
        return 502, {"error": "network_error", "message": str(e)}
    try:
        body = resp.json()
    except ValueError:
        body = resp.text
    return resp.status_code, body


@fintoc_bp.route('/create_payment_intent', methods=['POST'])
def create_payment_intent():
    # Debug: log raw body and parsed JSON to help trace 400 errors
    try:
        raw = request.data.decode('utf-8') if request.data else ''
    except Exception:
        raw = str(request.data)
    print('\n[debug] POST /create_payment_intent raw body:', raw)
    data = request.get_json(silent=True) or {}
    print('[debug] POST /create_payment_intent parsed JSON:', data)

    # Validate server-side config early
    if not os.getenv('FINTOC_SECRET_KEY'):
        print('[error] FINTOC_SECRET_KEY is not set in environment')
        return jsonify({"error": "FINTOC_SECRET_KEY not configured on server"}), 500
    # Expect amount in CLP (integer, not cents). If frontend sends cents, caller should divide by 100.
    amount = data.get('amount')
    if amount is None:
        return jsonify({"error": "amount is required (CLP integer)", "received": data}), 400

    # Accept numbers or numeric-strings (strip thousand separators)
    try:
        if isinstance(amount, str):
            # remove non-digit characters (commas, spaces, currency symbols)
            cleaned = ''.join(ch for ch in amount if ch.isdigit())
            amount_val = int(cleaned) if cleaned else 0
        else:
            amount_val = int(amount)
    except Exception:
        return jsonify({"error": "amount must be integer or numeric string", "received": data}), 400

    if amount_val <= 0:
        return jsonify({"error": "amount must be greater than 0", "received": data}), 400

    amount = amount_val

    # env flags
    USE_PRESET_RECIPIENT = os.getenv('USE_PRESET_RECIPIENT', 'false').lower() in ('1', 'true', 'yes')
    MOCK_PAYMENT_INTENT = os.getenv('MOCK_PAYMENT_INTENT', 'false').lower() in ('1', 'true', 'yes')

    # Build recipient account from env vars if present
    recipient = {
        "institution_id": os.getenv('RECIPIENT_BANK_ID') or 'cl_fintoc_bank',
        "number": os.getenv('RECIPIENT_ACCOUNT_NUMBER') or '00000000',
        "holder_name": os.getenv('RECIPIENT_HOLDER_NAME') or 'COMERCIO DEMO',
        "holder_id": os.getenv('RECIPIENT_HOLDER_ID') or '11111111-1',
        "type": os.getenv('RECIPIENT_ACCOUNT_TYPE') or 'checking_account',
    }

    payload = {"amount": amount, "currency": "CLP"}
    if not USE_PRESET_RECIPIENT:
        payload['recipient_account'] = recipient

    idempotency_key = str(uuid.uuid4())

    if MOCK_PAYMENT_INTENT:
        fake = {"widget_token": "wgt_test_pi_fake_123"}
        # persist minimal record
        try:
            store = load_data()
            store.setdefault('payment_intents', []).append({"id": idempotency_key, "widget_token": fake['widget_token'], "amount": amount, "status": "created"})
            save_data(store)
        except Exception:
            pass
        return jsonify(fake)

    status, resp = _fintoc_post('/payment_intents', payload, idempotency_key)
    if status >= 400:
        # Try retry logic if API complains about recipient_account
        try:
            error_code = resp.get('error', {}).get('code') if isinstance(resp, dict) else None
        except Exception:
            error_code = None
        if error_code == 'invalid_payment_recipient_account' and not USE_PRESET_RECIPIENT:
            status2, resp2 = _fintoc_post('/payment_intents', {"amount": amount, "currency": "CLP"}, idempotency_key)
            status, resp = status2, resp2
            if status >= 400:
                return jsonify({"error": "Fintoc API error", "details": resp}), status
        else:
            return jsonify({"error": "Fintoc API error", "details": resp}), status

    widget_token = resp.get('widget_token') if isinstance(resp, dict) else None
    if not widget_token:
        return jsonify({"error": "widget_token missing", "response": resp}), 500

    try:
        store = load_data()
        store.setdefault('payment_intents', []).append({"id": resp.get('id') or idempotency_key, "widget_token": widget_token, "amount": amount, "status": "created"})
        save_data(store)
    except Exception:
        pass

    return jsonify({"widget_token": widget_token})


@fintoc_bp.route('/create_transfer', methods=['POST'])
def create_transfer():
    data = request.get_json() or {}
    amount = data.get('amount')
    recipient = data.get('recipient_account')
    if amount is None:
        return jsonify({"error": "amount is required"}), 400
    try:
        amount = int(amount)
    except Exception:
        return jsonify({"error": "amount must be integer"}), 400

    if not recipient:
        recipient = {
            "holder_id": os.getenv('RECIPIENT_HOLDER_ID') or '11.111.111-1',
            "number": os.getenv('RECIPIENT_ACCOUNT_NUMBER') or '123456789',
            "type": os.getenv('RECIPIENT_ACCOUNT_TYPE') or 'checking_account',
            "institution_id": os.getenv('RECIPIENT_BANK_ID') or 'cl_fintoc_bank'
        }

    idempotency_key = str(uuid.uuid4())
    MOCK_TRANSFER = os.getenv('MOCK_TRANSFER', 'false').lower() in ('1', 'true', 'yes')
    if MOCK_TRANSFER:
        return jsonify({"id": "tr_fake_1", "status": "succeeded", "amount": amount})

    payload = {"amount": amount, "currency": "CLP", "recipient_account": recipient}
    status, resp = _fintoc_post('/transfers', payload, idempotency_key)
    if status >= 400:
        return jsonify({"error": "Fintoc transfer error", "details": resp}), status
    return jsonify(resp)


@fintoc_bp.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_json(silent=True)
    print('\n--- Webhook recibido ---')
    if payload is None:
        print('No JSON in webhook. Raw:', request.data)
    else:
        try:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        except Exception:
            print(payload)
    # persist
    try:
        store = load_data()
        evt = {"type": payload.get('type') if isinstance(payload, dict) else None, "payload": payload}
        store.setdefault('events', []).append(evt)
        save_data(store)
    except Exception:
        pass
    return ('', 200)


@fintoc_bp.route('/log_event', methods=['POST'])
def log_event():
    payload = request.get_json(silent=True)
    print('\n--- Frontend log_event ---')
    if payload is None:
        print('No JSON. Raw:', request.data)
    else:
        try:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        except Exception:
            print(payload)
        try:
            store = load_data()
            evt = {"type": payload.get('event') if isinstance(payload, dict) else None, "payload": payload}
            store.setdefault('events', []).append(evt)
            save_data(store)
        except Exception:
            pass
    return ('', 200)


@fintoc_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json() or {}
    product_id = data.get('product_id')
    amount = data.get('amount')
    status = data.get('status') or 'created'
    payment_intent_id = data.get('payment_intent_id')

    if not product_id or amount is None:
        return jsonify({'error': 'product_id and amount required'}), 400
    try:
        amount = int(amount)
    except Exception:
        return jsonify({'error': 'amount must be integer'}), 400

    # Try to find a pending order that matches product and amount (amount expected in cents)
    try:
        # If amount seems like CLP (small) convert to cents if needed
        if amount < 1000:
            # assume CLP, convert to cents
            amount_cents = amount * 100
        else:
            amount_cents = amount
    except Exception:
        amount_cents = amount

    order = None
    try:
        # find most recent pending order containing the product
        candidate = Order.query.filter_by(status=OrderStatus.PENDING).order_by(Order.created_at.desc()).first()
        if candidate:
            # ensure totals roughly match
            if candidate.total_amount == amount_cents:
                order = candidate
    except Exception:
        order = None

    if not order:
        order = Order(total_amount=amount_cents, status=OrderStatus.PAID if status in ('succeeded', 'paid') else OrderStatus.PENDING)
        fintoc_ecomerce_db.session.add(order)
        fintoc_ecomerce_db.session.flush()
        # create a single OrderItem pointing to product if product exists
        try:
            prod = Product.query.filter_by(id=product_id).first()
            if prod:
                item = OrderItem(order_id=order.id, product_id=prod.id, quantity=1, unit_price=prod.price)
                fintoc_ecomerce_db.session.add(item)
        except Exception:
            pass

    # update status and session id
    if status in ('succeeded', 'paid'):
        order.status = OrderStatus.PAID
    else:
        order.status = OrderStatus.PENDING
    if payment_intent_id:
        order.fintoc_session_id = payment_intent_id

    fintoc_ecomerce_db.session.commit()

    # also persist a minimal record in data.json for admin/debug
    try:
        store = load_data()
        store.setdefault('orders', []).append({'product_id': product_id, 'amount': amount, 'status': status, 'payment_intent_id': payment_intent_id})
        save_data(store)
    except Exception:
        pass

    return jsonify({'id': order.id, 'status': order.status.value}), 201
