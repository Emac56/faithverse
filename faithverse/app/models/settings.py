# app/models/settings.py
# Defines the Settings model — maps to the 'settings' table.
# Stores global configuration for the website.

from app import db
from datetime import datetime


class Settings(db.Model):
    """
    Stores website-wide settings managed by the admin.

    Design decision: This table is intended to have only ONE row.
    The admin updates that single row to change site-wide settings.

    Think of it like a control panel saved in the database.
    """

    __tablename__ = 'settings'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    # WEBSITE NAME — displayed in the browser tab, emails, etc.
    # default gives it a starting value so it works right away.
    website_name = db.Column(
        db.String(200),
        nullable=False,
        default='FaithVerse'
    )

    # ADMIN EMAIL — where system notifications are sent.
    admin_email = db.Column(
        db.String(120),
        nullable=False,
        default='admin@faithverse.com'
    )

    # MAINTENANCE MODE — when True, show a "Site under maintenance" page.
    # db.Boolean stores True/False (1/0 in MySQL).
    # default=False means the site is live by default.
    maintenance_mode = db.Column(
        db.Boolean,
        nullable=False,
        default=False
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
    # CLASS METHOD — Helper to get or create the settings row
    # ---------------------------------------------------------------

    @classmethod
    def get_settings(cls):
        """
        Returns the single settings row.
        If it doesn't exist yet, creates it with default values.

        Usage:
            settings = Settings.get_settings()
            print(settings.website_name)  → 'FaithVerse'

        @classmethod means you call this on the class itself,
        not on an instance:
            Settings.get_settings()   ✅ correct
            settings_obj.get_settings()  ❌ wrong
        """
        settings = cls.query.first()  # Try to get the first (only) row

        if settings is None:
            # No settings row exists yet — create one with defaults
            settings = cls()
            db.session.add(settings)
            db.session.commit()

        return settings

    def to_dict(self):
        """Converts settings to a dictionary for JSON responses."""
        return {
            'id':               self.id,
            'website_name':     self.website_name,
            'admin_email':      self.admin_email,
            'maintenance_mode': self.maintenance_mode,
            'created_at':       self.created_at.isoformat() if self.created_at else None,
            'updated_at':       self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Settings: {self.website_name} | Maintenance: {self.maintenance_mode}>'
