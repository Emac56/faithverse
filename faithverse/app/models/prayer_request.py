# app/models/prayer_request.py
# Defines the PrayerRequest model — maps to the 'prayer_requests' table.

from app import db
from datetime import datetime


class PrayerRequest(db.Model):
    """
    Represents a prayer request submitted by a user.

    Relationship: Many PrayerRequests belong to one User.
    (One user can have many prayer requests.)
    """

    __tablename__ = 'prayer_requests'

    # ---------------------------------------------------------------
    # COLUMNS
    # ---------------------------------------------------------------

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    # FOREIGN KEY — links this prayer request to the user who created it.
    # db.ForeignKey('users.id') means:
    #   "this column must contain a valid id from the users table"
    # nullable=False means every prayer request MUST have an owner.
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )

    # TITLE — short description of the prayer request
    title = db.Column(
        db.String(200),
        nullable=False
    )

    # MESSAGE — the full prayer request text
    # db.Text allows very long text (no character limit like String)
    message = db.Column(
        db.Text,
        nullable=False
    )

    # STATUS — tracks where this prayer request is in its lifecycle.
    # 'pending'  → just submitted, waiting for admin review
    # 'approved' → admin has approved it (visible to others)
    # 'answered' → the prayer was answered
    # default='pending' means all new requests start as pending.
    status = db.Column(
        db.String(20),
        nullable=False,
        default='pending'
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # ---------------------------------------------------------------
    # RELATIONSHIPS
    # ---------------------------------------------------------------

    # This creates the reverse link back to the User model.
    # 'back_populates' must match the name used in User.prayer_requests.
    # After this, you can do: prayer.user → returns the User object
    user = db.relationship(
        'User',
        back_populates='prayer_requests'
    )

    # ---------------------------------------------------------------
    # UTILITY METHODS
    # ---------------------------------------------------------------

    def to_dict(self):
        """Converts this PrayerRequest to a dictionary for JSON responses."""
        return {
            'id':         self.id,
            'user_id':    self.user_id,
            'title':      self.title,
            'message':    self.message,
            'status':     self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            # Include the username of the submitter if relationship is loaded
            'submitted_by': self.user.username if self.user else 'Anonymous'
        }

    def __repr__(self):
        return f'<PrayerRequest {self.id}: {self.title} [{self.status}]>'
