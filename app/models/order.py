from datetime import datetime
from enum import Enum


from app.extensions import fintoc_ecomerce_db

class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


class Order(fintoc_ecomerce_db.Model):
    __tablename__ = "orders"

    id = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.Integer, primary_key=True)
    total_amount = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.Integer, nullable=False)

    status = fintoc_ecomerce_db.Column(
        fintoc_ecomerce_db.Enum(OrderStatus),
        nullable=False,
        default=OrderStatus.PENDING
    )

    fintoc_session_id = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.String(120))
    created_at = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.DateTime, default=datetime.utcnow, nullable=False)

    items = fintoc_ecomerce_db.relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Order {self.id} - {self.status.value}>"