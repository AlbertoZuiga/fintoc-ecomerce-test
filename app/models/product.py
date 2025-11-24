from app.extensions import fintoc_ecomerce_db


class Product(fintoc_ecomerce_db.Model):
    __tablename__ = "products"

    id = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.Integer, primary_key=True)
    name = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.String(120), nullable=False)
    # Price stored as integer cents
    price = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.Integer, nullable=False)
    description = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.Text)
    sku = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.String(64), unique=True, nullable=True)
    image_url = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.String(255), nullable=True)

    category_id = fintoc_ecomerce_db.Column(
        fintoc_ecomerce_db.Integer,
        fintoc_ecomerce_db.ForeignKey("categories.id"),
        nullable=False,
    )

    category = fintoc_ecomerce_db.relationship("Category", back_populates="products")

    def __repr__(self):
        try:
            cat_name = self.category.name
        except Exception:
            cat_name = "?"
        return f"<Product {self.name} ({cat_name})>"