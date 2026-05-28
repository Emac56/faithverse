# app/routes/main_routes.py — UPDATED for Phase 7.1
# This file now only handles: health checks, error pages.
# Public website pages are handled by public_routes.py (public_bp).

from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)


@main_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check — public, no login required.
    Use this to confirm the backend is running.
    Visit: http://localhost:5000/health
    """
    from app import db
    from sqlalchemy import text
    from app.models import User, PrayerRequest, Settings

    try:
        db.session.execute(text('SELECT 1'))
        db_status = 'connected'
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
    """Custom 403 page."""
    return jsonify({
        'error':   'Forbidden',
        'message': 'You do not have permission to access this resource.'
    }), 403


@main_bp.app_errorhandler(401)
def unauthorized(e):
    """Custom 401 page."""
    return jsonify({
        'error':   'Unauthorized',
        'message': 'Please log in to access this resource.'
    }), 401
