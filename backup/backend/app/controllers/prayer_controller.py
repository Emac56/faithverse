# app/controllers/prayer_controller.py
# Handles public prayer request submissions.
# This is a PUBLIC API — no login required.

from app import db
from app.models.prayer_request import PrayerRequest
from app.models.website_visit import WebsiteVisit
from flask import request


def log_visit():
    """
    Records a website visit automatically.
    Called from public routes to track traffic.

    request.remote_addr  → visitor's IP address
    request.user_agent.string → browser/device info
    """
    try:
        visit = WebsiteVisit(
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(visit)
        db.session.commit()
    except Exception:
        db.session.rollback()
        pass  # Never crash the main request because of visit logging


def validate_prayer_submission(data):
    """
    Validates the public prayer submission form data.

    'data' is a dictionary from the JSON request body.
    Returns a list of error messages (empty = valid).

    Checks:
    - name is provided
    - prayer_title is provided
    - prayer_message is provided
    - fields are not just empty spaces
    """
    errors = []

    name    = data.get('name', '').strip()
    title   = data.get('prayer_title', '').strip()
    message = data.get('prayer_message', '').strip()

    if not name:
        errors.append('Your name is required.')

    if not title:
        errors.append('Prayer title is required.')

    if not message:
        errors.append('Prayer message is required.')

    if title and len(title) > 200:
        errors.append('Prayer title must be under 200 characters.')

    if message and len(message) < 10:
        errors.append('Prayer message is too short (minimum 10 characters).')

    return errors


def submit_prayer(data):
    """
    Saves a new public prayer request to the database.

    Steps:
    1. Validate the input data
    2. Create PrayerRequest object
    3. Save to database
    4. Return success or error response dict

    'data' comes from request.get_json() in the route.
    """

    # Step 1 — Validate
    errors = validate_prayer_submission(data)

    if errors:
        return {
            'success': False,
            'message': errors[0],   # Return first error
            'errors':  errors       # Return all errors too
        }, 400

    # Step 2 — Create prayer request
    # user_id is None because this is a public submission —
    # the visitor may not have an account.
    prayer = PrayerRequest(
        user_id=None,
        title=data.get('prayer_title', '').strip(),
        message=data.get('prayer_message', '').strip(),
        status='pending'   # Always starts as pending
    )

    # Save the submitter's name in submitted_by if field exists
    # (We'll add this column in migration if needed)

    # Step 3 — Save to database
    try:
        db.session.add(prayer)
        db.session.commit()

        return {
            'success': True,
            'message': 'Prayer request submitted successfully. We will pray for you! 🙏',
            'data': {
                'id':     prayer.id,
                'title':  prayer.title,
                'status': prayer.status
            }
        }, 201  # 201 = Created

    except Exception as e:
        db.session.rollback()
        return {
            'success': False,
            'message': 'Something went wrong. Please try again.'
        }, 500
