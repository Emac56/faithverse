# app/routes/main_routes.py — STABILIZED
# Handles: health check, /admin redirect, global error handlers.

from flask import Blueprint, jsonify, redirect, url_for
from flask_login import current_user

main_bp = Blueprint('main', __name__)


@main_bp.route('/admin')
def admin_redirect():
    """
    /admin → redirect admins to dashboard, others to login.
    Convenient shortcut so admins don't have to type /dashboard/.
    """
    if current_user.is_authenticated and current_user.is_admin():
        return redirect(url_for('dashboard.dashboard_home'))
    return redirect(url_for('auth.login'))


@main_bp.route('/health')
def health_check():
    """GET /health — confirms server + database are alive."""
    from app import db
    from sqlalchemy import text
    from app.models import User, PrayerRequest, Settings

    try:
        db.session.execute(text('SELECT 1'))
        db_status    = 'connected'
        table_counts = {
            'users':           User.query.count(),
            'prayer_requests': PrayerRequest.query.count(),
            'settings':        Settings.query.count()
        }
    except Exception as e:
        db_status    = f'error: {str(e)}'
        table_counts = {}

    return jsonify({
        'status':       'ok',
        'server':       'running',
        'database':     db_status,
        'table_counts': table_counts
    }), 200


@main_bp.app_errorhandler(403)
def forbidden(e):
    return jsonify({'error': 'Forbidden', 'message': 'Access denied.'}), 403


@main_bp.app_errorhandler(401)
def unauthorized(e):
    return redirect(url_for('auth.login'))

