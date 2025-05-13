from flask import Blueprint, render_template, request, jsonify, send_from_directory
from flask_login import login_required
import os

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/generate', methods=['POST'])
@login_required
def generate():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    image_path = generate_image_from_prompt(prompt)
    return jsonify({'image_url': '/' + image_path})


@main.route('/generated/<filename>')
def generated_image(filename):
    return send_from_directory('static/generated', filename)


def generate_image_from_prompt(prompt):
    os.makedirs('static/generated', exist_ok=True)
    filename = f"static/generated/{prompt[:10]}_demo.png"
    with open(filename, 'wb') as f:
        f.write(b'')
    return filename
