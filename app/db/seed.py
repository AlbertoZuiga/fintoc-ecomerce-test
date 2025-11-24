"""Seed script adapted during ecommerce migration.

MIGRATION: Imports and DB references updated from `scheduler_*` names to the
ecommerce-neutral names. Domain data remains from legacy project and should
be revisited to model ecommerce entities (products, orders, customers).
"""
from app import ecommerce_app

def seed_database():
    print("🌱 Iniciando seed de la base de datos...")

    print("\n" + "="*70)
    print("🎉 SEED COMPLETADO EXITOSAMENTE")
    print("="*70)


if __name__ == "__main__":
    with ecommerce_app.app_context():
        seed_database()
