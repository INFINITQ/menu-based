"""
Flask application factory and extensions initialization.
"""
from __future__ import annotations

import os
from typing import Optional

from flask import Flask
from flask_session import Session
from flask_socketio import SocketIO

# Create extension instances (initialized in create_app)
socketio: SocketIO = SocketIO(async_mode="threading")
server_session: Session = Session()


def create_app(config_object: Optional[dict] = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder="static", template_folder="templates")

    if not hasattr(app, "session_cookie_name"):
        app.session_cookie_name = app.config.get("SESSION_COOKIE_NAME", "session")

    # Basic config
    app.config.setdefault("SECRET_KEY", os.environ.get("SECRET_KEY", "super-secret-dev-key"))
    app.config.setdefault("SESSION_TYPE", os.environ.get("SESSION_TYPE", "filesystem"))
    app.config.setdefault("SESSION_COOKIE_HTTPONLY", True)
    app.config.setdefault("SESSION_COOKIE_SAMESITE", "Lax")

    # Extensions
    server_session.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Blueprints
    from app.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.terminal_ws import terminal_bp
    from app.routes.docker_api import docker_bp
    from app.routes.aws_api import aws_bp
    from app.routes.social_api import social_bp
    from app.routes.js_tools import js_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(terminal_bp)
    app.register_blueprint(docker_bp, url_prefix="/api/docker")
    app.register_blueprint(aws_bp, url_prefix="/api/aws")
    app.register_blueprint(social_bp, url_prefix="/api/social")
    app.register_blueprint(js_bp, url_prefix="/api/js")

    @app.route("/healthz")
    def _healthz():
        return "ok", 200

    return app


if __name__ == "__main__":
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
