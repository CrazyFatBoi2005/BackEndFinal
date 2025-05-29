from flask import Blueprint, render_template, redirect, flash, request, current_app, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from ..forms import ImageGenerationForm
from ..models import GeneratedImage, User
from .. import db
import datetime, uuid, base64, os
from ..openai_client import client


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')  # Или другой шаблон для главной страницы


@main_bp.route('/feed')
def feed():
    username = request.args.get('username', '', type=str).strip()

    if username:
        # Фильтруем по имени пользователя (не обязательно точное совпадение)
        images = GeneratedImage.query.join(User).filter(User.username.ilike(f'%{username}%')).order_by(GeneratedImage.timestamp.desc()).all()
    else:
        images = GeneratedImage.query.order_by(GeneratedImage.timestamp.desc()).all()

    return render_template('feed.html', images=images)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


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
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        with open(file_path, "wb") as f:
            f.write(image_bytes)

        print(f"Изображение успешно сохранено как {file_path}")
        return file_path  # Возвращаем путь к изображению

    except Exception as e:
        return f"Error: {str(e)}"  # В случае ошибки возвращаем текст ошибки


@main_bp.route('/generate', methods=['GET', 'POST'])
@login_required
def generate_image():
    form = ImageGenerationForm()
    if form.validate_on_submit():
        # Получаем аудиофайл из формы (если требуется)
        audio_file = request.files.get('audio')
        if audio_file and allowed_file(audio_file.filename):
            filename = secure_filename(audio_file.filename)
            audio_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
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
                image_path="/".join(image_url.split("\\")[-3:-1]),  # Сохраняем путь к изображению
                prompt=prompt
            )
            db.session.add(generated_image)
            db.session.commit()

            return redirect(url_for('main.feed'))

    return render_template('generate.html', form=form)


@main_bp.route('/image/<int:image_id>', methods=['POST', 'DELETE'])
@login_required
def delete_image(image_id):
    if request.method == 'DELETE' or request.form.get('_method') == 'DELETE':
        image = GeneratedImage.query.get_or_404(image_id)
        if image.user_id != current_user.id:
            flash("Вы не можете удалить это изображение.", "danger")
        else:
            try:
                os.remove(image.image_path)
            except Exception:
                pass
            db.session.delete(image)
            db.session.commit()
            flash("Изображение удалено.", "success")
    return redirect(url_for('main.feed'))


@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)