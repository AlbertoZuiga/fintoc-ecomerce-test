import os
from app import ecommerce_app as app
from app.extensions import fintoc_ecomerce_db

# Expose WSGI variables expected by Gunicorn/Render
# - `app` (common) and `application` (WSGI conventional)
application = app

# Create DB tables only when explicitly allowed via env var.
# This avoids side-effects when Gunicorn imports this module during deploy.
RUN_CREATE = os.getenv("RUN_CREATE_ALL", "false").lower() in ("1", "true", "t", "yes")
if RUN_CREATE:
    with app.app_context():
        fintoc_ecomerce_db.create_all()


if __name__ == "__main__":
    # In local runs you may want to create tables automatically.
    if RUN_CREATE:
        with app.app_context():
            fintoc_ecomerce_db.create_all()

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5050"))
    debug = app.config.get("DEBUG", False)
    app.run(host=host, port=port, debug=debug)
