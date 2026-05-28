# app/models/website_visit.py
# Defines the WebsiteVisit model — maps to the 'website_visits' table.
# Tracks each time someone visits the site.

from app import db
from datetime import datetime


class WebsiteVisit(db.Model):
    """
    Records each visit to the website.

    This is a simple log table — no foreign keys, no relationships.
    Each row = one page visit.

    Use this to:
    - Count total visitors
    - See which devices visit your site
    - Track traffic over time
    """

    __tablename__ = 'website_visits'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    # IP ADDRESS — the visitor's internet address.
    # Length 45 supports both IPv4 (e.g. 192.168.1.1)
    # and IPv6 (e.g. 2001:0db8:85a3:...) addresses.
    # nullable=True because sometimes IP cannot be determined.
    ip_address = db.Column(
        db.String(45),
        nullable=True
    )

    # USER AGENT — the browser/device string sent by the visitor.
    # Example: "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0"
    # This tells you if they used Chrome, Safari, a phone, etc.
    # db.Text because user agent strings can be very long.
    user_agent = db.Column(
        db.Text,
        nullable=True
    )

    # VISITED AT — exact date and time of the visit.
    # default=datetime.utcnow sets this automatically on insert.
    visited_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def to_dict(self):
        """Converts this visit record to a dictionary for JSON responses."""
        return {
            'id':         self.id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'visited_at': self.visited_at.isoformat() if self.visited_at else None
        }

    def __repr__(self):
        return f'<WebsiteVisit {self.id}: {self.ip_address} at {self.visited_at}>'
