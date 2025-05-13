from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm, LoginForm, ImageGenerationForm
import os
from werkzeug.utils import secure_filename
import datetime

# Инициализация приложения
app = Flask(__name__)

# Настройка секретного ключа и базы данных
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'flac'}

# Инициализация базы данных
db = SQLAlchemy(app)

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Указываем страницу входа

# Защита от CSRF атак
csrf = CSRFProtect(app)

# Модели
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Регистрация пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Проверка на уникальность email или username
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Этот email уже используется.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Аккаунт создан успешно!', 'success')
        return redirect(url_for('login'))  # Редирект на страницу входа
    return render_template('register.html', form=form)

# Вход пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)  # Входим в систему
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('generate_image'))  # Перенаправление на страницу генерации
        flash('Ошибка входа. Проверьте ваши данные.', 'danger')
    return render_template('login.html', form=form)

# Генерация изображения
@app.route('/generate', methods=['GET', 'POST'])
@login_required
def generate_image():
    form = ImageGenerationForm()
    if form.validate_on_submit():
        audio_file = request.files['audio']
        if audio_file and allowed_file(audio_file.filename):
            filename = secure_filename(audio_file.filename)
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio_file.save(audio_path)
            prompt = form.prompt.data

            # Генерация изображения (заглушка, сюда можно добавить логику генерации)
            image_filename = f"generated_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)

            # Сохраняем изображение в базе данных
            generated_image = GeneratedImage(user_id=current_user.id, image_path=image_path, prompt=prompt)
            db.session.add(generated_image)
            db.session.commit()

            flash('Изображение сгенерировано успешно!', 'success')
            return render_template('feed.html', image_path=image_path)
    return render_template('generate.html', form=form)

# Выход пользователя
@app.route('/logout')
def logout():
    logout_user()  # Выход из системы
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
