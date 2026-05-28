# app/utils/decorators.py
# Custom route protection decorators.
# Use these to restrict access based on user roles.

from functools import wraps
from flask import flash, redirect, url_for, abort
from flask_login import current_user


def admin_required(f):
    """
    Route decorator — only allows admin users.

    Usage:
        @app.route('/admin/dashboard')
        @login_required       ← check logged in first
        @admin_required       ← then check admin role
        def admin_dashboard():
            ...

    IMPORTANT: Always put @login_required ABOVE @admin_required.
    @login_required runs first — if not logged in, it redirects
    before @admin_required even runs.

    What @wraps(f) does:
    Without it, every decorated function would appear to be named
    'decorated_function' in Flask's internals — causing URL conflicts.
    @wraps(f) preserves the original function's name and docstring.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # current_user.is_authenticated is True if logged in
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('auth.login'))

        # Check admin role
        if not current_user.is_admin():
            # 403 = Forbidden — user is logged in but not allowed
            flash('You do not have permission to access this page.', 'danger')
            abort(403)

        # All checks passed — run the original route function
        return f(*args, **kwargs)

    return decorated_function


def role_required(*roles):
    """
    Flexible role decorator — allows multiple roles.

    Usage:
        @role_required('admin', 'moderator')
        def some_route():
            ...

        @role_required('admin')
        def admin_only_route():
            ...

    *roles means you can pass any number of role strings.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in first.', 'danger')
                return redirect(url_for('auth.login'))

            if current_user.role not in roles:
                flash('Access denied.', 'danger')
                abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator
