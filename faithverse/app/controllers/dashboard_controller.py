# app/controllers/dashboard_controller.py
# All database queries and logic for the admin dashboard.
# Routes call these functions — keeping routes clean.

from app import db
from app.models.user import User
from app.models.prayer_request import PrayerRequest
from app.models.website_visit import WebsiteVisit
from app.models.admin_log import AdminLog
from app.models.settings import Settings
from flask_login import current_user
from datetime import datetime, timedelta
from sqlalchemy import func


# ---------------------------------------------------------------
# MAIN STATS
# ---------------------------------------------------------------

def get_dashboard_stats():
    """
    Returns a dictionary of all important dashboard numbers.

    func.count() is SQLAlchemy's way of running COUNT() in SQL.
    filter_by(status='pending') adds a WHERE clause.

    Example SQL generated:
        SELECT COUNT(*) FROM users;
        SELECT COUNT(*) FROM prayer_requests WHERE status='pending';
    """

    total_users    = User.query.count()
    total_prayers  = PrayerRequest.query.count()
    total_visitors = WebsiteVisit.query.count()

    pending_prayers  = PrayerRequest.query.filter_by(status='pending').count()
    approved_prayers = PrayerRequest.query.filter_by(status='approved').count()
    answered_prayers = PrayerRequest.query.filter_by(status='answered').count()

    # Log this dashboard access
    AdminLog.log(
        admin_id=current_user.id,
        action='Viewed dashboard stats'
    )

    return {
        'total_users':       total_users,
        'total_prayers':     total_prayers,
        'total_visitors':    total_visitors,
        'pending_prayers':   pending_prayers,
        'approved_prayers':  approved_prayers,
        'answered_prayers':  answered_prayers
    }


# ---------------------------------------------------------------
# RECENT ACTIVITY
# ---------------------------------------------------------------

def get_recent_users(limit=5):
    """
    Returns the most recently registered users.

    order_by(User.created_at.desc()) sorts newest first.
    .desc() means descending — largest/newest value first.
    .limit(5) returns only 5 results — not the entire table.

    Example SQL:
        SELECT * FROM users ORDER BY created_at DESC LIMIT 5;
    """
    users = User.query\
        .order_by(User.created_at.desc())\
        .limit(limit)\
        .all()

    return [u.to_dict() for u in users]


def get_recent_prayers(limit=5):
    """
    Returns the most recently submitted prayer requests.
    Includes the username of who submitted each one.
    """
    prayers = PrayerRequest.query\
        .order_by(PrayerRequest.created_at.desc())\
        .limit(limit)\
        .all()

    return [p.to_dict() for p in prayers]


def get_recent_admin_logs(limit=10):
    """
    Returns the most recent admin activity logs.
    Useful for auditing who did what and when.
    """
    logs = AdminLog.query\
        .order_by(AdminLog.created_at.desc())\
        .limit(limit)\
        .all()

    return [log.to_dict() for log in logs]


# ---------------------------------------------------------------
# ANALYTICS
# ---------------------------------------------------------------

def get_visitor_analytics(days=7):
    """
    Returns daily visitor counts for the last N days.

    How it works:
    - Loop through each of the last 7 days
    - Count visits where visited_at is within that day
    - Return a list of {date, count} objects

    Example output:
    [
        {"date": "2026-05-18", "visitors": 12},
        {"date": "2026-05-19", "visitors": 8},
        ...
    ]
    """
    result = []
    today  = datetime.utcnow().date()

    for i in range(days - 1, -1, -1):
        # Calculate the start and end of each day
        day       = today - timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time())
        day_end   = datetime.combine(day, datetime.max.time())

        count = WebsiteVisit.query.filter(
            WebsiteVisit.visited_at >= day_start,
            WebsiteVisit.visited_at <= day_end
        ).count()

        result.append({
            'date':     day.strftime('%Y-%m-%d'),
            'visitors': count
        })

    return result


def get_prayer_analytics(days=7):
    """
    Returns daily prayer submission counts for the last N days.
    Same structure as visitor analytics.
    """
    result = []
    today  = datetime.utcnow().date()

    for i in range(days - 1, -1, -1):
        day       = today - timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time())
        day_end   = datetime.combine(day, datetime.max.time())

        count = PrayerRequest.query.filter(
            PrayerRequest.created_at >= day_start,
            PrayerRequest.created_at <= day_end
        ).count()

        result.append({
            'date':    day.strftime('%Y-%m-%d'),
            'prayers': count
        })

    return result


def get_prayer_status_breakdown():
    """
    Returns a count of prayers grouped by status.
    Shows the proportion of pending vs approved vs answered.
    """
    total    = PrayerRequest.query.count()
    pending  = PrayerRequest.query.filter_by(status='pending').count()
    approved = PrayerRequest.query.filter_by(status='approved').count()
    answered = PrayerRequest.query.filter_by(status='answered').count()

    return {
        'total':    total,
        'pending':  pending,
        'approved': approved,
        'answered': answered
    }


# ---------------------------------------------------------------
# USER MANAGEMENT HELPERS
# ---------------------------------------------------------------

def get_all_users():
    """Returns all users ordered by registration date."""
    users = User.query.order_by(User.created_at.desc()).all()
    return [u.to_dict() for u in users]


def get_all_prayers(status=None):
    """
    Returns all prayer requests.
    Optional: filter by status ('pending', 'approved', 'answered').

    Usage:
        get_all_prayers()            → all prayers
        get_all_prayers('pending')   → only pending
    """
    query = PrayerRequest.query

    if status:
        query = query.filter_by(status=status)

    prayers = query.order_by(PrayerRequest.created_at.desc()).all()
    return [p.to_dict() for p in prayers]


def update_prayer_status(prayer_id, new_status):
    """
    Updates a prayer request's status.
    Valid statuses: 'pending', 'approved', 'answered'

    Returns (success, message) tuple.
    """
    valid_statuses = ['pending', 'approved', 'answered']

    if new_status not in valid_statuses:
        return False, f'Invalid status. Must be one of: {valid_statuses}'

    prayer = PrayerRequest.query.get(prayer_id)

    if not prayer:
        return False, f'Prayer request #{prayer_id} not found.'

    old_status    = prayer.status
    prayer.status = new_status

    try:
        db.session.commit()

        # Log the action
        AdminLog.log(
            admin_id=current_user.id,
            action=f'Updated prayer #{prayer_id} status: {old_status} → {new_status}'
        )

        return True, f'Prayer #{prayer_id} updated to {new_status}.'

    except Exception as e:
        db.session.rollback()
        return False, f'Database error: {str(e)}'


def delete_user(user_id):
    """
    Deletes a user and all their prayer requests (cascade).
    Cannot delete your own account or other admins.

    Returns (success, message) tuple.
    """
    if user_id == current_user.id:
        return False, 'You cannot delete your own account.'

    user = User.query.get(user_id)

    if not user:
        return False, f'User #{user_id} not found.'

    if user.is_admin():
        return False, 'Cannot delete an admin account.'

    username = user.username

    try:
        db.session.delete(user)
        db.session.commit()

        AdminLog.log(
            admin_id=current_user.id,
            action=f'Deleted user: {username} (id={user_id})'
        )

        return True, f'User {username} deleted successfully.'

    except Exception as e:
        db.session.rollback()
        return False, f'Database error: {str(e)}'


def promote_user(user_id):
    """Promotes a regular user to admin role."""
    user = User.query.get(user_id)

    if not user:
        return False, 'User not found.'

    if user.is_admin():
        return False, f'{user.username} is already an admin.'

    user.role = 'admin'

    try:
        db.session.commit()
        AdminLog.log(
            admin_id=current_user.id,
            action=f'Promoted {user.username} to admin'
        )
        return True, f'{user.username} is now an admin.'

    except Exception as e:
        db.session.rollback()
        return False, str(e)
