import os

SECRET_KEY = 'super-secret-key'  # Секретный ключ для сессий и безопасности
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # Путь к базе данных
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключаем предупреждение SQLAlchemy

MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # Максимальный размер загружаемого файла: 5 МБ

# Пути к директориям для загрузок
BASE_UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/static', 'uploads')
AUDIO_UPLOAD_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, 'audio')
IMAGE_UPLOAD_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, 'images')

# Разрешённые форматы
ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'ogg'}
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
