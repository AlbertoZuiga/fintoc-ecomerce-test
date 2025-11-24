from app.routes.auth_routes import auth_bp
from app.routes.main_routes import main_bp
from app.routes.product_routes import product_bp

blueprints = [main_bp, auth_bp, product_bp]
