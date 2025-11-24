from flask import Blueprint, render_template, request, current_app, url_for, redirect
from sqlalchemy import desc, asc

from app.models.product import Product
from app.models.category import Category

product_bp = Blueprint("products", __name__)


@product_bp.route("/products")
def index():
    """List products with simple filters:

    Query params:
    - q: text search on product name (case-insensitive, substring)
    - category: category name or id to filter
    - sort: 'price_desc' | 'price_asc' | 'name_asc' | 'name_desc'
    """
    q = request.args.get("q", "").strip()
    category = request.args.get("category")
    sort = request.args.get("sort")

    # Base query
    query = Product.query

    # Text search
    if q:
        query = query.filter(Product.name.ilike(f"%{q}%"))

    # Category filter (accept name or id)
    categories = Category.query.order_by(Category.name).all()
    if category:
        # try id
        try:
            cid = int(category)
            query = query.filter(Product.category_id == cid)
        except Exception:
            # assume category is name
            query = query.join(Category).filter(Category.name == category)

    # Sorting
    if sort == "price_desc":
        query = query.order_by(desc(Product.price))
    elif sort == "price_asc":
        query = query.order_by(asc(Product.price))
    elif sort == "name_desc":
        query = query.order_by(desc(Product.name))
    else:
        # default name ascending
        query = query.order_by(asc(Product.name))

    products = query.all()

    return render_template(
        "products/index.html",
        products=products,
        categories=categories,
        filters={"q": q, "category": category, "sort": sort},
    )


@product_bp.route("/products/<int:product_id>")
def show(product_id: int):
    product = Product.query.get_or_404(product_id)
    return render_template("products/show.html", product=product)
