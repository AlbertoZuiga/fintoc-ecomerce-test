from flask import Flask, flash, redirect, request, session, url_for
from flask_login import current_user

# MIGRATION: Updated extension names for ecommerce project.
# Replaced `scheduler_db` with `fintoc_ecomerce_db` and exposing `ecommerce_app` below.
from app.extensions import fintoc_ecomerce_db, login_manager
from app.models.user import User
from app.routes import blueprints
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    fintoc_ecomerce_db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.unauthorized_handler
    def custom_unauthorized():
        if current_user.is_anonymous:
            flash("Necesitas iniciar sesión para acceder a esta página.", "warning")

        session["next_page"] = request.full_path
        return redirect(url_for("auth.login", next=request.full_path))

    @app.errorhandler(403)
    def forbidden_error(error):
        """Maneja errores 403 Forbidden redirigiendo en lugar de mostrar error genérico."""
        # El flash ya fue configurado en authz.py antes del abort(403)
        # Redirigir a la lista de grupos o página principal
        return redirect(url_for("main.index"))

    @app.errorhandler(404)
    def not_found_error(error):
        """Maneja errores 404 Not Found."""
        flash("La página que buscas no existe.", "warning")
        return redirect(url_for("main.index"))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    for bp in blueprints:
        app.register_blueprint(bp)

    return app


# Application instance for the ecommerce project. Other modules should import
# `ecommerce_app` from `app` (and `fintoc_ecomerce_db` from `app.extensions`).
ecommerce_app = create_app()
