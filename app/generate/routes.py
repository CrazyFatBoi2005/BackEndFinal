from flask import Blueprint, request, session, redirect, url_for

generate_bp = Blueprint('generate', __name__, url_prefix='/generate')

@generate_bp.route('/', methods=['GET', 'POST'])
def generate():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return "<h2>Generate Image Page (Form)</h2>"
