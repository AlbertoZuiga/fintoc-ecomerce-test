import os
from app import ecommerce_app
from app.extensions import fintoc_ecomerce_db

with ecommerce_app.app_context():
    fintoc_ecomerce_db.create_all()


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5050"))
    debug = ecommerce_app.config.get("DEBUG", False)
    ecommerce_app.run(host=host, port=port, debug=debug)
