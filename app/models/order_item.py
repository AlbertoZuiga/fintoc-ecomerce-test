from app.extensions import fintoc_ecomerce_db

class OrderItem(fintoc_ecomerce_db.Model):
    __tablename__ = "order_items"

    id = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.Integer, primary_key=True)

    order_id = fintoc_ecomerce_db.Column(
        fintoc_ecomerce_db.Integer,
        fintoc_ecomerce_db.ForeignKey("orders.id"),
        nullable=False
    )

    product_id = fintoc_ecomerce_db.Column(
        fintoc_ecomerce_db.Integer,
        fintoc_ecomerce_db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.Integer, nullable=False)
    unit_price = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.Integer, nullable=False)

    order = fintoc_ecomerce_db.relationship("Order", back_populates="items")
    product = fintoc_ecomerce_db.relationship("Product")

    def __repr__(self):
        return f"<OrderItem order={self.order_id} product={self.product_id}>"
