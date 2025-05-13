import os
from flask import Flask
import config

# configurations
app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# auto folder creation
for folder in (config.AUDIO_UPLOAD_FOLDER, config.IMAGE_UPLOAD_FOLDER):
    os.makedirs(folder, exist_ok=True)


@app.route('/')
def index():
    return "<h1>Main Page</h1><p>Здесь будет галерея сгенерированных картинок.</p>"


# TODO: добавить маршруты для регистрации, логина, генерации и профиля

if __name__ == '__main__':
    app.run(debug=True)
