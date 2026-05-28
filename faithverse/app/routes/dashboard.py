# app/routes/dashboard.py — REFACTORED & STABILIZED

from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import admin_required
from app.controllers.dashboard_controller import (
    get_dashboard_stats,
    get_recent_users,
    get_recent_prayers,
    get_recent_admin_logs,
    get_visitor_analytics,
    get_prayer_analytics,
    get_prayer_status_breakdown,
    get_all_users,
    get_all_prayers,
    update_prayer_status,
    delete_user,
    promote_user
)

dashboard_bp = Blueprint('dashboard', __name__)


def _is_ajax():
    """Returns True if the request came from JS Fetch AND has a valid CSRF token."""
    from flask import session
    token = request.headers.get('X-CSRFToken')
    return bool(token and token == session.get('_csrf_token'))


# ---------------------------------------------------------------
# DASHBOARD HOME
# ---------------------------------------------------------------

@dashboard_bp.route('/', methods=['GET'])
@login_required
@admin_required
def dashboard_home():
    """Renders the main dashboard overview page."""
    return render_template(
        'dashboard/index.html',
        stats          = get_dashboard_stats(),
        recent_users   = get_recent_users(5),
        recent_prayers = get_recent_prayers(5)
    )


# ---------------------------------------------------------------
# STATS (JSON API — used by dashboard.js auto-refresh)
# ---------------------------------------------------------------

@dashboard_bp.route('/stats', methods=['GET'])
@login_required
@admin_required
def stats():
    """JSON endpoint — returns live stats for dashboard JS refresh."""
    return jsonify({'status': 'success', 'data': get_dashboard_stats()}), 200


# ---------------------------------------------------------------
# ANALYTICS
# ---------------------------------------------------------------

@dashboard_bp.route('/analytics', methods=['GET'])
@login_required
@admin_required
def analytics_page():
    """Renders the analytics page."""
    return render_template(
        'dashboard/analytics.html',
        visitor_data  = get_visitor_analytics(7),
        prayer_data   = get_prayer_analytics(7),
        prayer_status = get_prayer_status_breakdown()
    )


# ---------------------------------------------------------------
# ADMIN LOGS (JSON)
# ---------------------------------------------------------------

@dashboard_bp.route('/logs', methods=['GET'])
@login_required
@admin_required
def admin_logs():
    """Returns recent admin activity as JSON."""
    limit = request.args.get('limit', 20, type=int)
    return jsonify({
        'status': 'success',
        'data':   get_recent_admin_logs(limit)
    }), 200


# ---------------------------------------------------------------
# USER MANAGEMENT
# ---------------------------------------------------------------

@dashboard_bp.route('/users', methods=['GET'])
@login_required
@admin_required
def list_users():
    """Renders the user management page."""
    return render_template(
        'dashboard/users.html',
        users=get_all_users()
    )


@dashboard_bp.route('/users/<int:user_id>/promote', methods=['POST'])
@login_required
@admin_required
def promote(user_id):
    """Promote a user to admin. Supports both AJAX and form POST."""
    success, message = promote_user(user_id)

    if _is_ajax():
        return jsonify({
            'status':  'success' if success else 'error',
            'message': message
        }), 200 if success else 400

    flash(message, 'success' if success else 'danger')
    return redirect(url_for('dashboard.list_users'))


@dashboard_bp.route('/users/<int:user_id>/delete', methods=['POST', 'DELETE'])
@login_required
@admin_required
def remove_user_page(user_id):
    """Delete a user. Supports both AJAX and form POST."""
    success, message = delete_user(user_id)

    if _is_ajax():
        return jsonify({
            'status':  'success' if success else 'error',
            'message': message
        }), 200 if success else 400

    flash(message, 'success' if success else 'danger')
    return redirect(url_for('dashboard.list_users'))


# ---------------------------------------------------------------
# PRAYER MANAGEMENT
# ---------------------------------------------------------------

@dashboard_bp.route('/prayers', methods=['GET'])
@login_required
@admin_required
def list_prayers():
    """Renders the prayer requests management page."""
    status = request.args.get('status', None)
    return render_template(
        'dashboard/prayers.html',
        prayers       = get_all_prayers(status),
        status_filter = status
    )


@dashboard_bp.route('/prayers/<int:prayer_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_prayer(prayer_id):
    """Approve a prayer. Supports AJAX and form POST."""
    success, message = update_prayer_status(prayer_id, 'approved')

    if _is_ajax():
        return jsonify({
            'status':  'success' if success else 'error',
            'message': message
        }), 200 if success else 400

    flash(message, 'success' if success else 'danger')
    return redirect(url_for('dashboard.list_prayers'))


@dashboard_bp.route('/prayers/<int:prayer_id>/answer', methods=['POST'])
@login_required
@admin_required
def answer_prayer(prayer_id):
    """Mark a prayer as answered. Supports AJAX and form POST."""
    success, message = update_prayer_status(prayer_id, 'answered')

    if _is_ajax():
        return jsonify({
            'status':  'success' if success else 'error',
            'message': message
        }), 200 if success else 400

    flash(message, 'success' if success else 'danger')
    return redirect(url_for('dashboard.list_prayers'))


@dashboard_bp.route('/prayers/<int:prayer_id>/delete', methods=['DELETE'])
@login_required
@admin_required
def delete_prayer(prayer_id):
    """Delete a prayer via AJAX."""
    from app.models.prayer_request import PrayerRequest
    from app.models.admin_log import AdminLog
    from app import db

    prayer = PrayerRequest.query.get(prayer_id)
    if not prayer:
        return jsonify({'status': 'error', 'message': 'Prayer not found.'}), 404

    try:
        title = prayer.title[:50]
        db.session.delete(prayer)
        db.session.commit()
        AdminLog.log(
            admin_id=current_user.id,
            action=f'Deleted prayer #{prayer_id}: {title}'
        )
        return jsonify({
            'status':  'success',
            'message': f'Prayer #{prayer_id} deleted.'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500



