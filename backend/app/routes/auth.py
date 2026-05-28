# app/routes/auth.py — FIXED & STABILIZED

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.utils.decorators import admin_required
from app.controllers.auth_controller import (
    register_user,
    login_user_handler,
    logout_user_handler
)

auth_bp = Blueprint('auth', __name__)


# ---------------------------------------------------------------
# REGISTER
# ---------------------------------------------------------------

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET  /auth/register → Show registration form.
    POST /auth/register → Process and save new user.
    Already-logged-in users are redirected to the homepage.
    """
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    if request.method == 'POST':
        return register_user(
            request.form.get('username', ''),
            request.form.get('email', ''),
            request.form.get('password', ''),
            request.form.get('confirm_password', '')
        )

    return render_template('auth/register.html')


# ---------------------------------------------------------------
# LOGIN
# ---------------------------------------------------------------

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET  /auth/login → Show login form.
    POST /auth/login → Verify credentials and create session.
    Already-logged-in users are redirected to the dashboard.
    """
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('dashboard.dashboard_home'))
        return redirect(url_for('public.index'))

    if request.method == 'POST':
        return login_user_handler(
            request.form.get('identifier', ''),
            request.form.get('password', ''),
            request.form.get('remember') == 'on'
        )

    return render_template('auth/login.html')


# ---------------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------------

@auth_bp.route('/logout')
@login_required
def logout():
    """GET /auth/logout → Clear session and redirect to login."""
    return logout_user_handler()


# ---------------------------------------------------------------
# PROFILE
# ---------------------------------------------------------------

@auth_bp.route('/profile')
@login_required
def profile():
    """GET /auth/profile → Show logged-in user's profile."""
    return render_template('auth/profile.html', user=current_user)


# ---------------------------------------------------------------
# ADMIN TEST (protected route — for verifying role decorator)
# ---------------------------------------------------------------

@auth_bp.route('/admin-test')
@login_required
@admin_required
def admin_test():
    """GET /auth/admin-test → Quick check that admin protection works."""
    return jsonify({'message': f'Hello, admin {current_user.username}!'})
