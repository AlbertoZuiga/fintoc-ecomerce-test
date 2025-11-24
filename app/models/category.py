from app.extensions import fintoc_ecomerce_db

class Category(fintoc_ecomerce_db.Model):
    __tablename__ = "categories"

    id = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.Integer, primary_key=True)
    name = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.String(120), nullable=False, unique=True)

    products = fintoc_ecomerce_db.relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"
