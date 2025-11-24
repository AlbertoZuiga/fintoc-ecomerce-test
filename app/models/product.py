from app.extensions import fintoc_ecomerce_db


class Product(fintoc_ecomerce_db.Model):
    __tablename__ = "products"

    id = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.Integer, primary_key=True)
    name = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.String(120), nullable=False)
    price = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.Integer, nullable=False)
    description = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.Text)

    category_id = fintoc_ecomerce_db.Column(
        fintoc_ecomerce_db.Integer,
        fintoc_ecomerce_db.ForeignKey("categories.id"),
        nullable=False
    )

    category = fintoc_ecomerce_db.relationship("Category", back_populates="products")

    def __repr__(self):
        return f"<Product {self.name} ({self.category.name})>"