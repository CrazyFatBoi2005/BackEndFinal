# main.py
import os
from flask import Flask
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

app = Flask(__name__)

# Inline-конфигурация без отдельного класса
# Секретный ключ для сессий и CSRF
app.secret_key = os.getenv('SECRET_KEY', 'super-secret-key')

# Настройки SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Настройки загрузки файлов
BASE_UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
AUDIO_UPLOAD_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, 'audio')
IMAGE_UPLOAD_FOLDER = os.path.join(BASE_UPLOAD_FOLDER, 'images')

# Ограничение на размер загружаемых файлов: 5 МБ
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

# Инициализация базы данных и моделей
# db = Database(app)

# Создание необходимых директорий
for folder in (AUDIO_UPLOAD_FOLDER, IMAGE_UPLOAD_FOLDER):
    os.makedirs(folder, exist_ok=True)


# Заглушка главного маршрута
def index():
    return "<h1>Main Page</h1><p>Здесь будет галерея сгенерированных картинок.</p>"


app.add_url_rule('/', 'index', index)

# TODO: добавить маршруты для регистрации, логина, генерации и профиля

if __name__ == '__main__':
    app.run(debug=True)
