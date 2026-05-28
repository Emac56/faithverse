# app/routes/public_routes.py — FIXED & STABILIZED
# Handles all public-facing pages.
# No login required for any of these routes.

from flask import Blueprint, render_template
from app.models.prayer_request import PrayerRequest
from app.models.website_visit import WebsiteVisit
from app import db
from flask import request as flask_request

public_bp = Blueprint('public', __name__)


def _log_visit():
    """Silently record a page visit for analytics. Never crashes the page."""
    try:
        visit = WebsiteVisit(
            ip_address=flask_request.remote_addr,
            user_agent=flask_request.user_agent.string
        )
        db.session.add(visit)
        db.session.commit()
    except Exception:
        db.session.rollback()


def _footer_counts():
    """Returns prayer_count and answered_count for the footer template."""
    try:
        return {
            'prayer_count':   PrayerRequest.query.count(),
            'answered_count': PrayerRequest.query.filter_by(status='answered').count()
        }
    except Exception:
        return {'prayer_count': 0, 'answered_count': 0}


# ---------------------------------------------------------------
# HOMEPAGE
# ---------------------------------------------------------------

@public_bp.route('/')
def index():
    """
    GET / — Public homepage.
    Template: templates/public/index.html
    """
    _log_visit()
    return render_template('public/index.html', **_footer_counts())


# ---------------------------------------------------------------
# ABOUT
# ---------------------------------------------------------------

@public_bp.route('/about')
def about():
    """GET /about — About page."""
    _log_visit()
    return render_template('public/about.html', **_footer_counts())


# ---------------------------------------------------------------
# CONTACT
# ---------------------------------------------------------------

@public_bp.route('/contact')
def contact():
    """GET /contact — Contact page."""
    _log_visit()
    return render_template('public/contact.html', **_footer_counts())


# ---------------------------------------------------------------
# PRAYER WALL
# ---------------------------------------------------------------

@public_bp.route('/prayer-wall')
def prayer_wall():
    """
    GET /prayer-wall — Shows all approved and answered prayers.
    Pending prayers are NOT shown — they need admin approval first.
    """
    _log_visit()

    try:
        prayers = PrayerRequest.query\
            .filter(PrayerRequest.status.in_(['approved', 'answered']))\
            .order_by(PrayerRequest.created_at.desc())\
            .all()
        prayers_data = [p.to_dict() for p in prayers]
    except Exception:
        prayers_data = []

    return render_template(
        'public/prayer_wall.html',
        prayers=prayers_data,
        **_footer_counts()
    )


# ---------------------------------------------------------------
# 404 HANDLER
# ---------------------------------------------------------------

@public_bp.app_errorhandler(404)
def page_not_found(e):
    """Custom 404 page for the entire app."""
    return render_template('public/404.html', **_footer_counts()), 404

