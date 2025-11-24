from flask_login import UserMixin

from app.extensions import fintoc_ecomerce_db


class User(UserMixin, fintoc_ecomerce_db.Model):
    """User model adapted during ecommerce migration.

    MIGRATION: Replaced legacy `scheduler_db` with `fintoc_ecomerce_db`. Convert domain
    fields later to match ecommerce (customers, roles, addresses).
    """
    id = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.Integer, primary_key=True)
    email = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.String(150), unique=True, nullable=False)
    name = fintoc_ecomerce_db.Column(fintoc_ecomerce_db.String(150), nullable=False)


    @classmethod
    def get_or_create_from_oauth(cls, user_info):
        email = user_info.get("email")
        name = user_info.get("name")

        if not email or not name:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user:
            user = cls(email=email, name=name)
            fintoc_ecomerce_db.session.add(user)
            fintoc_ecomerce_db.session.commit()

        return user
