from datetime import timedelta
import os


class Config:
    SECRET_KEY = 'mysecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # путь к static/uploads внутри папки app
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # это будет папка app/
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

    ALLOWED_EXTENSIONS = {'mp3', 'wav', 'flac'}
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
