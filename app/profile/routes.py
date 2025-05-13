from flask import Blueprint, render_template, session, redirect, url_for

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return "<h2>User Profile Page</h2>"
