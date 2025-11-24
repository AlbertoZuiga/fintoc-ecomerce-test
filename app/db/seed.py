"""Seed script adapted during ecommerce migration.

MIGRATION: Imports and DB references updated from `scheduler_*` names to the
ecommerce-neutral names. Domain data remains from legacy project and should
be revisited to model ecommerce entities (products, orders, customers).
"""
from app import ecommerce_app
from app.extensions import fintoc_ecomerce_db
from app.models.product import Product
from app.models.category import Category

def seed_database():
    print("🌱 Iniciando seed de la base de datos...")

    # Ensure all tables are created before seeding. This avoids failures when
    # the database is empty or migrations haven't been run.
    fintoc_ecomerce_db.create_all()

    categories_data = [
        "Snacks Salados",
        "Snacks Dulces",
        "Bebidas",
        "Bebidas Energéticas",
        "Snacks Saludables",
    ]

    products_data = [
        # (name, category_name, price_cents, description, sku)
        # Prices updated to realistic Chilean CLP values. Stored as integer cents
        # (i.e. CLP * 100) to match the app convention where templates divide by 100.
        ("Papas Fritas Clásicas", "Snacks Salados", 1290 * 100, "Papas fritas saladas - bolsa 120g", "SNK-001"),
        ("Maní Tostado", "Snacks Salados", 1890 * 100, "Maní salado tostado - bolsa 100g", "SNK-002"),
        ("Galletas Chocolate", "Snacks Dulces", 1490 * 100, "Galletas con chispas de chocolate - paquete 90g", "SNK-003"),
        ("Barrita de Cereal", "Snacks Saludables", 990 * 100, "Barrita integral con frutos secos - unidad", "SNK-004"),
        ("Chocolate 70%", "Snacks Dulces", 2490 * 100, "Chocolate oscuro 70% cacao - tableta 80g", "SNK-005"),
        ("Agua Mineral 500ml", "Bebidas", 890 * 100, "Agua mineral sin gas - 500ml", "DRK-001"),
        ("Refresco Cola 330ml", "Bebidas", 1190 * 100, "Refresco cola clásico - lata 330ml", "DRK-002"),
        ("Jugo Naranja 1L", "Bebidas", 2990 * 100, "Jugo de naranja natural - 1 litro", "DRK-003"),
        ("Bebida Energética X", "Bebidas Energéticas", 2490 * 100, "Energizante con cafeína - lata 250ml", "ENR-001"),
        ("Agua con Gas 330ml", "Bebidas", 990 * 100, "Agua carbonatada - lata 330ml", "DRK-004"),
    ]

    # Create or get categories
    categories_map = {}
    for name in categories_data:
        cat = Category.query.filter_by(name=name).first()
        if not cat:
            cat = Category(name=name)
            fintoc_ecomerce_db.session.add(cat)
            fintoc_ecomerce_db.session.commit()
            print(f"  - Creada categoría: {name}")
        else:
            print(f"  - Categoría existente: {name}")
        categories_map[name] = cat

    # Create products (idempotent by name + category)
    for pname, cname, price_cents, desc, sku in products_data:
        cat = categories_map.get(cname)
        if not cat:
            print(f"  ! Categoría ausente '{cname}' para producto '{pname}', se salta.")
            continue

        existing = Product.query.filter_by(name=pname, category_id=cat.id).first()
        if existing:
            print(f"  - Producto existente: {pname} (categoría: {cname})")
            continue

        prod = Product(
            name=pname,
            price=price_cents,
            description=desc,
            sku=sku,
            category_id=cat.id,
        )
        fintoc_ecomerce_db.session.add(prod)
        fintoc_ecomerce_db.session.commit()
        print(f"  + Producto creado: {pname} ({cname}) - {price_cents} cents - SKU {sku}")

    print("\n" + "="*70)
    print("🎉 SEED COMPLETADO EXITOSAMENTE")
    print("="*70)


if __name__ == "__main__":
    with ecommerce_app.app_context():
        seed_database()
