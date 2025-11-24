from flask import Blueprint, render_template
from flask_login import login_required

from app.models.order import Order, OrderStatus

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart")
@login_required
def view_cart():
    # Show the most recent pending order (simple cart implementation)
    order = Order.query.filter_by(status=OrderStatus.PENDING).order_by(Order.created_at.desc()).first()
    return render_template("cart/index.html", order=order)


@cart_bp.route("/orders")
@login_required
def past_orders():
    # List paid orders
    orders = Order.query.filter_by(status=OrderStatus.PAID).order_by(Order.created_at.desc()).all()
    return render_template("orders/index.html", orders=orders)
