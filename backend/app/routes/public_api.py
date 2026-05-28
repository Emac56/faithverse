# app/routes/public_api.py
# Public-facing API routes.
# NO login required — anyone can access these.

from flask import Blueprint, jsonify, request
from app.controllers.prayer_controller import submit_prayer, log_visit
from app.models.settings import Settings

public_api_bp = Blueprint('public_api', __name__)


@public_api_bp.route('/prayer-request', methods=['POST'])
def submit_prayer_request():
    """
    POST /api/prayer-request
    Public endpoint for submitting prayer requests.

    Expected JSON body:
    {
        "name":           "Maria Santos",
        "email":          "maria@example.com",  (optional)
        "prayer_title":   "Prayer for healing",
        "prayer_message": "Please pray for my mother..."
    }

    Content-Type must be: application/json

    request.get_json() reads and parses the JSON body.
    Returns None if body is empty or not valid JSON.
    """

    # Log this visit for analytics
    log_visit()

    # Get JSON data from request body
    data = request.get_json()

    if not data:
        return jsonify({
            'success': False,
            'message': 'No data received. Please send JSON.'
        }), 400

    # Call controller to validate and save
    response, status_code = submit_prayer(data)
    return jsonify(response), status_code


@public_api_bp.route('/site-info', methods=['GET'])
def site_info():
    """
    GET /api/site-info
    Returns public website settings.
    Frontend can call this to get the site name, etc.
    """
    log_visit()
    settings = Settings.get_settings()

    return jsonify({
        'success':      True,
        'website_name': settings.website_name,
        'maintenance':  settings.maintenance_mode
    }), 200


@public_api_bp.route('/ping', methods=['GET'])
def ping():
    """
    GET /api/ping
    Simple health check for the public API.
    Frontend can call this to confirm backend is running.
    """
    return jsonify({
        'success': True,
        'message': 'FaithVerse API is running.',
        'version': '1.0.0'
    }), 200
