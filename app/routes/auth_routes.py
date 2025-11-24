import os
import pathlib
from urllib.parse import urljoin, urlparse

import google.auth.transport.requests
import google.oauth2.id_token
from flask import Blueprint, redirect, request, session, url_for
from flask_login import login_required, login_user, logout_user
from google_auth_oauthlib.flow import Flow

from app.models.user import User
from config import Config

auth_bp = Blueprint("auth", __name__)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


@auth_bp.route("/login")
def login():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    client_secrets_file = os.path.join(
        pathlib.Path(__file__).parent.parent.parent, "client_secret.json"
    )

    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=[
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
        ],
        redirect_uri=f"{Config.URL}/auth/google/callback",
    )

    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@auth_bp.route("/auth/google/callback")
def callback():
    client_secrets_file = os.path.join(
        pathlib.Path(__file__).parent.parent.parent, "client_secret.json"
    )
    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=[
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
        ],
        redirect_uri=f"{Config.URL}/auth/google/callback",
    )

    flow.fetch_token(authorization_response=request.url)

    # Validate state to protect against CSRF. Use .pop to remove the stored
    # state and avoid KeyError when it is missing. Compare with the state
    # returned by the provider (request.args.get). If validation fails,
    # redirect the user to login with a helpful message.
    session_state = session.pop("state", None)
    request_state = request.args.get("state")

    if not session_state or session_state != request_state:
        # Log details for debugging (printed to console). Avoid exposing
        # sensitive data to the user in production.
        print(f"[auth] Invalid/missing OAuth state. session_state={session_state!r} request_state={request_state!r}")
        return redirect(url_for("auth.login"))

    credentials = flow.credentials

    request_session = google.auth.transport.requests.Request()
    id_info = google.oauth2.id_token.verify_oauth2_token(
        credentials.id_token, request_session, flow.client_config["client_id"]
    )

    user = User.get_or_create_from_oauth(id_info)
    if user:
        # Use Flask-Login "remember" to keep the session persistent across browser restarts
        # Duration is controlled by `REMEMBER_COOKIE_DURATION` in app config.
        login_user(user, remember=True)

        next_page = session.pop("next_page", None)
        if not next_page or not is_safe_url(next_page):
            next_page = url_for("main.index")
        return redirect(next_page)

    return "No se pudo autenticar el usuario", 400


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
