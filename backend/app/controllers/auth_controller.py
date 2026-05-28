# app/controllers/auth_controller.py — FIXED & STABILIZED

from flask import flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from app import db
from app.models.user import User


# ---------------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------------

def validate_registration(username, email, password, confirm_password):
    """
    Validates registration inputs.
    Returns a list of error strings. Empty list = all valid.
    """
    errors = []

    if not username or not username.strip():
        errors.append('Username is required.')
    elif len(username.strip()) < 3:
        errors.append('Username must be at least 3 characters.')

    if not email or not email.strip():
        errors.append('Email is required.')
    elif '@' not in email:
        errors.append('Please enter a valid email address.')

    if not password:
        errors.append('Password is required.')
    elif len(password) < 8:
        errors.append('Password must be at least 8 characters.')

    if not confirm_password:
        errors.append('Please confirm your password.')
    elif password and password != confirm_password:
        errors.append('Passwords do not match.')

    # Database uniqueness checks (only if no format errors above)
    if not errors:
        if User.query.filter_by(username=username.strip().lower()).first():
            errors.append('That username is already taken.')
        if User.query.filter_by(email=email.strip().lower()).first():
            errors.append('That email address is already registered.')

    return errors


def validate_login(identifier, password):
    """
    Validates login inputs. Accepts username OR email as identifier.
    Returns (user_or_None, list_of_errors).
    """
    errors = []

    if not identifier or not identifier.strip():
        errors.append('Username or email is required.')
    if not password:
        errors.append('Password is required.')
    if errors:
        return None, errors

    # Find user by email first, then by username
    user = User.query.filter_by(email=identifier.strip().lower()).first()
    if not user:
        user = User.query.filter_by(username=identifier.strip().lower()).first()

    if not user or not user.check_password(password):
        errors.append('Invalid username/email or password.')
        return None, errors

    return user, []


# ---------------------------------------------------------------
# REGISTER
# ---------------------------------------------------------------

def register_user(username, email, password, confirm_password):
    """
    Full registration flow:
    validate → create user → hash password → save → auto-login → redirect
    """
    errors = validate_registration(username, email, password, confirm_password)

    if errors:
        for error in errors:
            flash(error, 'danger')
        return redirect(url_for('auth.register'))

    new_user = User(
        username=username.strip().lower(),
        email=email.strip().lower(),
        role='user'
    )
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('An error occurred. Please try again.', 'danger')
        return redirect(url_for('auth.register'))

    login_user(new_user)
    flash(f'Welcome, {new_user.username}! Your account has been created.', 'success')
    return redirect(url_for('public.index'))


# ---------------------------------------------------------------
# LOGIN
# ---------------------------------------------------------------

def login_user_handler(identifier, password, remember):
    """
    Full login flow:
    validate → find user → check password → create session → redirect by role
    Admins go to /dashboard/, regular users go to homepage.
    """
    user, errors = validate_login(identifier, password)

    if errors:
        for error in errors:
            flash(error, 'danger')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    flash(f'Welcome back, {user.username}!', 'success')

    # Admins go straight to the admin dashboard
    if user.is_admin():
        return redirect(url_for('dashboard.dashboard_home'))

    return redirect(url_for('public.index'))


# ---------------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------------

def logout_user_handler():
    """Clear session and redirect to login page."""
    username = current_user.username if current_user.is_authenticated else 'User'
    logout_user()
    flash(f'You have been logged out, {username}.', 'info')
    return redirect(url_for('auth.login'))
