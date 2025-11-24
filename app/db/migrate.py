"""DB migrate helper for ecommerce migration.

MIGRATION: Replaced `scheduler_app` with `ecommerce_app` and `scheduler_db`
with `fintoc_ecomerce_db`. Kept behavior but adapted names for the ecommerce project.
"""
from app import ecommerce_app
from app.extensions import fintoc_ecomerce_db


def migrate_database():
    with ecommerce_app.app_context():
        print("Migrando base de datos...")
        fintoc_ecomerce_db.create_all()
        print("Base de datos migrada con éxito.\n")


if __name__ == "__main__":
    migrate_database()
