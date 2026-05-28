# app/models/admin_log.py
# Defines the AdminLog model — maps to the 'admin_logs' table.
# Records every significant action taken by admins.

from app import db
from datetime import datetime


class AdminLog(db.Model):
    """
    An audit trail of admin actions.

    Every time an admin does something important (approves a prayer,
    bans a user, changes settings), we log it here.

    This creates accountability — you can always see who did what and when.

    Relationship: Many AdminLogs belong to one User (the admin).
    """

    __tablename__ = 'admin_logs'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    # ADMIN ID — which admin performed this action.
    # Foreign key links to the users table (admins are also users).
    # nullable=True because if an admin account is deleted, we still
    # want to keep the log — we just lose the link to who did it.
    admin_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )

    # ACTION — description of what the admin did.
    # Examples:
    #   "Approved prayer request #42"
    #   "Banned user john_doe"
    #   "Changed website name to FaithVerse Pro"
    #   "Turned on maintenance mode"
    # db.Text allows long descriptions.
    action = db.Column(
        db.Text,
        nullable=False
    )

    # CREATED AT — when this action happened.
    # No updated_at because logs are never edited — only created.
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # ---------------------------------------------------------------
    # RELATIONSHIP
    # ---------------------------------------------------------------

    # Link back to the User who is the admin.
    # back_populates='admin_logs' matches what we defined in User model.
    admin = db.relationship(
        'User',
        back_populates='admin_logs'
    )

    # ---------------------------------------------------------------
    # CLASS METHOD — Easy way to create a log entry
    # ---------------------------------------------------------------

    @classmethod
    def log(cls, admin_id, action):
        """
        Creates and saves a new admin log entry in one line.

        Usage example:
            AdminLog.log(admin_id=1, action="Approved prayer request #5")

        This is more convenient than writing 3 lines every time:
            log = AdminLog(admin_id=1, action="...")
            db.session.add(log)
            db.session.commit()
        """
        entry = cls(admin_id=admin_id, action=action)
        db.session.add(entry)
        db.session.commit()
        return entry

    def to_dict(self):
        """Converts this log entry to a dictionary for JSON responses."""
        return {
            'id':         self.id,
            'admin_id':   self.admin_id,
            'action':     self.action,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            # Include admin username if the relationship is loaded
            'admin_username': self.admin.username if self.admin else 'deleted_user'
        }

    def __repr__(self):
        return f'<AdminLog {self.id}: admin={self.admin_id} — {self.action[:50]}>'
