from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
from flask_login import login_required

from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.product import Product
from app.extensions import fintoc_ecomerce_db

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart")
@login_required
def view_cart():
    # Show the most recent pending order (simple cart implementation)
    order = Order.query.filter_by(status=OrderStatus.PENDING).order_by(Order.created_at.desc()).first()
    # Convert total amount to CLP integer for the widget (prices stored in cents)
    order_total_clp = None
    if order and order.total_amount is not None:
        try:
            order_total_clp = int(order.total_amount // 100)
        except Exception:
            order_total_clp = None

    fintoc_public_key = os.getenv('FINTOC_PUBLIC_KEY')
    mock_payment_intent = os.getenv('MOCK_PAYMENT_INTENT', 'false').lower() in ('1', 'true', 'yes')

    return render_template("cart/index.html", order=order, order_total_clp=order_total_clp, fintoc_public_key=fintoc_public_key, mock_payment_intent=mock_payment_intent)


@cart_bp.route("/orders")
@login_required
def past_orders():
    # List paid orders
    orders = Order.query.filter_by(status=OrderStatus.PAID).order_by(Order.created_at.desc()).all()
    return render_template("orders/index.html", orders=orders)


@cart_bp.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id: int):
    """Add a product to the current pending order.

    Simple implementation:
    - Find or create a pending Order
    - Find existing OrderItem for product, increase quantity or create new
    - Update order.total_amount
    """
    qty = 1
    try:
        qty = int(request.form.get("quantity", 1))
        if qty < 1:
            qty = 1
    except Exception:
        qty = 1

    product = Product.query.get_or_404(product_id)

    # Get latest pending order or create one
    order = Order.query.filter_by(status=OrderStatus.PENDING).order_by(Order.created_at.desc()).first()
    if not order:
        order = Order(total_amount=0, status=OrderStatus.PENDING)
        fintoc_ecomerce_db.session.add(order)
        fintoc_ecomerce_db.session.flush()  # ensure order.id is available

    # Check for existing item
    item = OrderItem.query.filter_by(order_id=order.id, product_id=product.id).first()
    if item:
        item.quantity += qty
        # keep unit_price as was (assume stable)
    else:
        item = OrderItem(order_id=order.id, product_id=product.id, quantity=qty, unit_price=product.price)
        fintoc_ecomerce_db.session.add(item)

    # Recalculate total_amount simply by summing items
    fintoc_ecomerce_db.session.flush()
    total = 0
    for it in order.items:
        total += it.unit_price * it.quantity
    order.total_amount = total

    fintoc_ecomerce_db.session.commit()

    flash(f"Se agregó {qty} × {product.name} al carrito.", "success")
    return redirect(url_for("cart.view_cart"))
