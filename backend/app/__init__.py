# app/__init__.py — Updated for Phase 7.2

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import config

db            = SQLAlchemy()
migrate       = Migrate()
bcrypt        = Bcrypt()
login_manager = LoginManager()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view             = 'auth.login'
    login_manager.login_message          = 'Please log in to access this page.'
    login_manager.login_message_category = 'danger'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    with app.app_context():
        from app.models import (  # noqa: F401
            User, PrayerRequest, WebsiteVisit, Settings, AdminLog
        )

    # ---------------------------------------------------------------
    # REGISTER BLUEPRINTS
    # ---------------------------------------------------------------

    # PUBLIC WEBSITE — handles /, /about, /contact, /prayer-wall, 404
    # No url_prefix → routes start from the root /
    from app.routes.public_routes import public_bp
    app.register_blueprint(public_bp)

    # MAIN — handles /health and generic error handlers
    from app.routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    # AUTH — handles /auth/login, /auth/register, /auth/logout
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # DASHBOARD — handles /dashboard/* (requires login)
    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    # PUBLIC API — handles /api/prayer-request (Phase 7.3 will use this)
    from app.routes.public_api import public_api_bp
    app.register_blueprint(public_api_bp, url_prefix='/api')

    # ---------------------------------------------------------------
    # CONTEXT PROCESSORS
    # Variables injected into EVERY template automatically.
    # ---------------------------------------------------------------

    from datetime import datetime

    @app.context_processor
    def inject_globals():
        """
        Makes 'now' available in all templates without passing it manually.
        Used in the footer: © {{ now.year }} FaithVerse
        """
        return {'now': datetime.utcnow()}

    # ---------------------------------------------------------------
    # CSRF TOKEN
    # ---------------------------------------------------------------

    @app.before_request
    def set_csrf_token():
        import secrets
        from flask import session
        if '_csrf_token' not in session:
            session['_csrf_token'] = secrets.token_hex(16)

    return app
