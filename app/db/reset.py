from app import ecommerce_app
from app.extensions import fintoc_ecomerce_db


def reset_database():
    """Reset DB helper updated during ecommerce migration.

    MIGRATION: `scheduler_app` -> `ecommerce_app`, `scheduler_db` -> `fintoc_ecomerce_db`.
    """
    with ecommerce_app.app_context():
        fintoc_ecomerce_db.drop_all()
        fintoc_ecomerce_db.create_all()
        print("Base de datos reseteada con éxito.\n")


if __name__ == "__main__":
    reset_database()
