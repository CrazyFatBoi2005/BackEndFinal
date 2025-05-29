from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from ..forms import LoginForm, RegistrationForm, ChangePasswordForm
from .. import db
from .. import login_manager


auth_bp = Blueprint('auth', __name__)


# Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            if user and check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash('Вход выполнен успешно!', 'success')
                return redirect(url_for('main.generate_image'))
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('main.generate_image'))
        flash('Ошибка входа. Проверьте ваши данные.', 'danger')
    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Логика регистрации пользователя
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Аккаунт создан успешно!', 'success')
        return redirect(url_for('auth.login'))  # Перенаправление на страницу входа
    return render_template('register.html', form=form)


@auth_bp.route('/profile/password', methods=['GET', 'POST', 'PUT'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if request.method == 'PUT' or request.form.get('_method') == 'PUT':
        if form.validate_on_submit():
            if not check_password_hash(current_user.password, form.old_password.data):
                flash("Старый пароль неверен.", "danger")
            else:
                current_user.password = generate_password_hash(form.new_password.data)
                db.session.commit()
                flash("Пароль успешно обновлён!", "success")
                return redirect(url_for('main.profile'))
    return render_template('change_password.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('main.index'))
