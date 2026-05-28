# app/routes/auth.py
# Authentication routes — /auth/login, /auth/register, /auth/logout

from flask_login import login_required
from app.utils.decorators import admin_required
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.controllers.auth_controller import (
    register_user,
    login_user_handler,
    logout_user_handler
)

# Create the auth Blueprint
# 'auth' is the name — used in url_for('auth.login'), etc.
auth_bp = Blueprint('auth', __name__)


# ---------------------------------------------------------------
# REGISTER ROUTE
# ---------------------------------------------------------------

auth_bp.route('/admin-test')
@login_required
@admin_required
def admin_test():
    return jsonify({'message': f'Hello admin {current_user.username}!'})

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET  /auth/register → Show the registration form
    POST /auth/register → Process the submitted form data

    If user is already logged in, redirect to home.
    No point showing a register page to someone already logged in.
    """
    # Redirect already-logged-in users away from this page
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    if request.method == 'POST':
        # request.form is a dictionary of all submitted form fields
        username         = request.form.get('username', '')
        email            = request.form.get('email', '')
        password         = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Pass to controller — it handles validation and saving
        return register_user(username, email, password, confirm_password)

    # GET request — just show the form
    return render_template('auth/register.html')


# ---------------------------------------------------------------
# LOGIN ROUTE
# ---------------------------------------------------------------

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET  /auth/login → Show the login form
    POST /auth/login → Process the submitted login credentials

    If user is already logged in, redirect to home.
    """
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard_home'))

    if request.method == 'POST':
        identifier = request.form.get('identifier', '')  # username or email
        password   = request.form.get('password', '')

        # 'remember' checkbox — True if checked, False if not
        # request.form.get returns None if unchecked, 'on' if checked
        remember = request.form.get('remember') == 'on'

        return login_user_handler(identifier, password, remember)

    # GET request — show the login form
    return render_template('auth/login.html')


# ---------------------------------------------------------------
# LOGOUT ROUTE
# ---------------------------------------------------------------

@auth_bp.route('/logout')
@login_required   # Must be logged in to log out
def logout():
    """
    GET /auth/logout → Log out the current user and redirect to login.

    @login_required ensures anonymous users can't hit this route.
    If they try, Flask-Login redirects them to the login page.
    """
    return logout_user_handler()


# ---------------------------------------------------------------
# PROFILE ROUTE (basic — for testing login_required)
# ---------------------------------------------------------------

@auth_bp.route('/profile')
@login_required
def profile():
    """
    GET /auth/profile → Show the current user's profile.

    This route is protected by @login_required.
    If not logged in, Flask-Login redirects to /auth/login.
    current_user is the logged-in User object — always available.
    """
    return render_template('auth/profile.html', user=current_user)
