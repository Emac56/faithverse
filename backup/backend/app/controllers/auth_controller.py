# app/controllers/auth_controller.py
# Business logic for authentication.
# Routes call these functions — keeping routes clean and thin.

from flask import flash, redirect, url_for, session
from flask_login import login_user, logout_user, current_user
from app import db
from app.models.user import User


# ---------------------------------------------------------------
# VALIDATION HELPERS
# ---------------------------------------------------------------

def validate_registration(username, email, password, confirm_password):
    """
    Validates all registration form fields.

    Returns a list of error messages.
    An empty list means everything is valid.

    Checks:
    - All fields are filled in
    - Passwords match
    - Password is long enough
    - Username is not already taken
    - Email is not already registered
    """
    errors = []

    # Check for empty fields
    if not username or not username.strip():
        errors.append('Username is required.')

    if not email or not email.strip():
        errors.append('Email is required.')

    if not password:
        errors.append('Password is required.')

    if not confirm_password:
        errors.append('Please confirm your password.')

    # Check passwords match
    if password and confirm_password and password != confirm_password:
        errors.append('Passwords do not match.')

    # Check password length
    if password and len(password) < 8:
        errors.append('Password must be at least 8 characters long.')

    # Check for @ in email (basic validation)
    if email and '@' not in email:
        errors.append('Please enter a valid email address.')

    # Check username length
    if username and len(username.strip()) < 3:
        errors.append('Username must be at least 3 characters long.')

    # Check if username already exists in database
    if username and User.query.filter_by(
        username=username.strip().lower()
    ).first():
        errors.append('That username is already taken.')

    # Check if email already exists in database
    if email and User.query.filter_by(
        email=email.strip().lower()
    ).first():
        errors.append('That email address is already registered.')

    return errors


def validate_login(identifier, password):
    """
    Validates login form fields.

    'identifier' can be either a username or an email address.
    We check both so users don't have to remember which they used.

    Returns a tuple: (user_object_or_None, list_of_errors)
    """
    errors = []

    if not identifier or not identifier.strip():
        errors.append('Username or email is required.')

    if not password:
        errors.append('Password is required.')

    if errors:
        return None, errors

    # Try to find the user by email first, then by username
    user = User.query.filter_by(
        email=identifier.strip().lower()
    ).first()

    if not user:
        user = User.query.filter_by(
            username=identifier.strip().lower()
        ).first()

    # Check if user exists and password is correct
    if not user or not user.check_password(password):
        errors.append('Invalid username/email or password.')
        return None, errors

    return user, []


# ---------------------------------------------------------------
# REGISTER LOGIC
# ---------------------------------------------------------------

def register_user(username, email, password, confirm_password):
    """
    Handles the full user registration process.

    Steps:
    1. Validate all inputs
    2. Create a new User object
    3. Hash and set the password
    4. Save to database
    5. Log the user in automatically
    6. Redirect to home

    Returns a Flask redirect response.
    """

    # Step 1 — Validate
    errors = validate_registration(username, email, password, confirm_password)

    if errors:
        # Flash each error message to display in the template
        for error in errors:
            flash(error, 'danger')
        return redirect(url_for('auth.register'))

    # Step 2 — Create user
    new_user = User(
        username=username.strip().lower(),
        email=email.strip().lower(),
        role='user'   # All new registrations are regular users by default
    )

    # Step 3 — Hash and store password
    new_user.set_password(password)

    # Step 4 — Save to database
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Undo any partial changes
        flash('An error occurred. Please try again.', 'danger')
        return redirect(url_for('auth.register'))

    # Step 5 — Log the new user in automatically
    login_user(new_user)

    # Step 6 — Show success message and redirect
    flash(f'Welcome, {new_user.username}! Your account has been created.', 'success')
    return redirect(url_for('public.index'))


# ---------------------------------------------------------------
# LOGIN LOGIC
# ---------------------------------------------------------------

def login_user_handler(identifier, password, remember):
    """
    Handles the login process.

    Steps:
    1. Validate inputs
    2. Find user in database
    3. Check password
    4. Create session (log the user in)
    5. Redirect to appropriate page

    'remember' = True means the session cookie lasts 30 days.
    'remember' = False means it expires when the browser closes.

    Returns a Flask redirect response.
    """

    # Step 1 & 2 & 3 — Validate and find user
    user, errors = validate_login(identifier, password)

    if errors:
        for error in errors:
            flash(error, 'danger')
        return redirect(url_for('auth.login'))

    # Step 4 — Log the user in
    # login_user() stores the user's ID in a signed session cookie.
    # Flask-Login will call load_user() on every request from now on.
    login_user(user, remember=remember)

    # Step 5 — Redirect based on role
    flash(f'Welcome back, {user.username}!', 'success')

    if user.is_admin():
        # Admins go to admin dashboard (Phase 4)
        # For now redirect to home until dashboard is built
        return redirect(url_for('public.index'))
    else:
        return redirect(url_for('public.index'))


# ---------------------------------------------------------------
# LOGOUT LOGIC
# ---------------------------------------------------------------

def logout_user_handler():
    """
    Handles the logout process.

    logout_user() from Flask-Login:
    - Clears the user's ID from the session cookie
    - Sets current_user to AnonymousUser (not logged in)

    After this, any @login_required route will redirect to /auth/login.

    Returns a Flask redirect response.
    """
    username = current_user.username if current_user.is_authenticated else 'User'
    logout_user()
    flash(f'You have been logged out, {username}.', 'info')
    return redirect(url_for('auth.login'))
