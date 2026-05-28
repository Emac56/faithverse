# app/routes/public_routes.py
# Public-facing website routes.
# All pages here are accessible to everyone — no login required.

from flask import Blueprint, render_template

# Create the Blueprint.
# Name: 'public'
# Used in templates: url_for('public.index'), url_for('public.about'), etc.
public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    """
    Homepage — first page visitors see.
    Template: templates/public/index.html
    """
    return render_template('public/index.html')


@public_bp.route('/about')
def about():
    """
    About page — describes FaithVerse mission and story.
    Template: templates/public/about.html
    """
    return render_template('public/about.html')


@public_bp.route('/contact')
def contact():
    """
    Contact page.
    Template: templates/public/contact.html
    """
    return render_template('public/contact.html')


@public_bp.route('/prayer-wall')
def prayer_wall():
    """
    Prayer Wall page.
    Phase 7.3 will add: prayer form + Fetch API
    Phase 7.4 will add: display of approved prayers from database

    Template: templates/public/prayer_wall.html
    """
    return render_template('public/prayer_wall.html')


@public_bp.app_errorhandler(404)
def page_not_found(e):
    """
    Custom 404 error page for the entire app.

    When any URL doesn't match a route, Flask calls this function
    and shows the violet-themed 404 page instead of Flask's default.

    Returns a tuple: (template, status_code)
    The 404 status code must be explicitly returned — render_template
    alone would return 200 (success), which is wrong for a missing page.
    """
    return render_template('public/404.html'), 404
