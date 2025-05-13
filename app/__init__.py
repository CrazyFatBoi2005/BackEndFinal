from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Загрузка конфигурации
    from app import config
    app.config.from_object(config)

    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Редирект при попытке доступа без авторизации

    # Создание необходимых директорий, если их нет
    os.makedirs(app.config['AUDIO_UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['IMAGE_UPLOAD_FOLDER'], exist_ok=True)

    # Регистрация блюпринтов
    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.profile.routes import profile_bp
    from app.generate.routes import generate_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(generate_bp)

    return app
