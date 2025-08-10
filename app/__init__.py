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
    """Create and configure the Flask application.

    Reads configuration from environment variables when available. Keeps
    defaults sensible for local development on RHEL 9.6.
    """
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Basic config — for production you should override with environment variables
    app.config.setdefault("SECRET_KEY", os.environ.get("SECRET_KEY", "super-secret-dev-key"))
    # Server-side session storage (filesystem) for simplicity
    app.config.setdefault("SESSION_TYPE", os.environ.get("SESSION_TYPE", "filesystem"))
    app.config.setdefault("SESSION_COOKIE_HTTPONLY", True)
    app.config.setdefault("SESSION_COOKIE_SAMESITE", "Lax")

    # Register extensions
    server_session.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Import and register blueprints
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

    # Simple health check
    @app.route("/healthz")
    def _healthz():
        return "ok", 200

    return app


# If you want to run with `python -m app` during dev, provide a minimal runner
if __name__ == "__main__":
    app = create_app()
    # For development only. Use socketio.run to enable websocket support.
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)