import os
import datetime
import uuid

from flask_migrate import Migrate
from openai import OpenAI
import base64
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from forms import ImageGenerationForm, LoginForm, RegistrationForm
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из файла .env
load_dotenv()

client = OpenAI()

# Инициализация приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'flac'}

# Инициализация базы данных
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Защита от CSRF атак
csrf = CSRFProtect(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # Связь с сгенерированными изображениями
    generated_images = db.relationship('GeneratedImage', backref='user', lazy=True)


class GeneratedImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(200), nullable=False)
    prompt = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


# Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')  # Или другой шаблон для главной страницы


@app.route('/feed')
@login_required
def feed():
    # Получаем все сгенерированные изображения
    all_images = GeneratedImage.query.all()
    all_images.reverse()
    return render_template('feed.html', images=all_images)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Логика регистрации пользователя
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Аккаунт создан успешно!', 'success')
        return redirect(url_for('login'))  # Перенаправление на страницу входа
    return render_template('register.html', form=form)


def generate_image_from_prompt(prompt):
    try:
        # Запрос к OpenAI для генерации изображения
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt
        )

        image_base64 = response.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        # Сохраняем изображение в файл
        unique_filename = f"{uuid.uuid4().hex}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        file_path = f"static/uploads/{unique_filename}"
        with open(file_path, "wb") as f:
            f.write(image_bytes)

        print(f"Изображение успешно сохранено как {file_path}")
        return file_path  # Возвращаем путь к изображению

    except Exception as e:
        return f"Error: {str(e)}"  # В случае ошибки возвращаем текст ошибки


@app.route('/generate', methods=['GET', 'POST'])
@login_required
def generate_image():
    form = ImageGenerationForm()
    if form.validate_on_submit():
        # Получаем аудиофайл из формы (если требуется)
        audio_file = request.files['audio']
        if audio_file and allowed_file(audio_file.filename):
            filename = secure_filename(audio_file.filename)
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio_file.save(audio_path)

        # Получаем текстовое описание для генерации
        prompt = form.prompt.data

        # Генерация изображения
        image_url = generate_image_from_prompt(prompt)

        if "Error" in image_url:
            flash(f'Ошибка при генерации изображения: {image_url}', 'danger')
        else:
            flash('Изображение успешно сгенерировано!', 'success')

            # Сохраняем информацию о сгенерированном изображении в базе данных
            generated_image = GeneratedImage(
                user_id=current_user.id,
                image_path=image_url,  # Сохраняем путь к изображению
                prompt=prompt
            )
            db.session.add(generated_image)
            db.session.commit()

            return redirect('feed')

    return render_template('generate.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('generate_image'))
        flash('Ошибка входа. Проверьте ваши данные.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


if __name__ == '__main__':
    app.run(debug=True)
