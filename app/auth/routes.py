from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return "<h2>Login Page</h2>"

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return "<h2>Register Page</h2>"

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
