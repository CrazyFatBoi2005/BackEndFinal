from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from .config import Config


# Инициализация базы данных
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    # Защита от CSRF атак
    csrf.init_app(app)

    from .routes.auth_routes import auth_bp
    from .routes.main_routes import main_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.permanent_session_lifetime = Config.PERMANENT_SESSION_LIFETIME

    return app


