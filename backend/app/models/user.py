# app/models/user.py
# User model — updated for Phase 3 with Flask-Login and Flask-Bcrypt.

from app import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    """
    Represents a registered user.

    UserMixin adds 4 required methods/properties that Flask-Login needs:
      - is_authenticated  → True if user is logged in
      - is_active         → True if user account is enabled
      - is_anonymous      → False for real users
      - get_id()          → Returns the user's id as a string

    Without UserMixin, Flask-Login would not know how to work with
    your User class. Adding it gives all 4 for free — no extra code.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(80),  unique=True, nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)

    # Stores the bcrypt hash — never the real password
    password_hash = db.Column(db.String(255), nullable=False)

    # 'user' or 'admin'
    role = db.Column(db.String(20), nullable=False, default='user')

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships (same as Phase 2)
    prayer_requests = db.relationship(
        'PrayerRequest',
        back_populates='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    admin_logs = db.relationship(
        'AdminLog',
        back_populates='admin',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # ---------------------------------------------------------------
    # PASSWORD METHODS — uses Flask-Bcrypt via app context
    # ---------------------------------------------------------------

    def set_password(self, plain_password):
        """
        Hash a plain password and store it in password_hash.

        bcrypt.generate_password_hash() returns bytes.
        .decode('utf-8') converts it to a string for MySQL storage.

        Usage:
            user.set_password('MyPassword123!')
        """
        from app import bcrypt
        self.password_hash = bcrypt.generate_password_hash(
            plain_password
        ).decode('utf-8')

    def check_password(self, plain_password):
        """
        Compare a plain password against the stored hash.
        Returns True if they match, False if not.

        bcrypt.check_password_hash() re-hashes the plain password
        the same way and compares. The original password is never
        stored or recovered — only compared.

        Usage:
            if user.check_password('MyPassword123!'):
                # correct password
        """
        from app import bcrypt
        return bcrypt.check_password_hash(
            self.password_hash,
            plain_password
        )

    # ---------------------------------------------------------------
    # ROLE HELPERS
    # ---------------------------------------------------------------

    def is_admin(self):
        """Returns True if this user has the admin role."""
        return self.role == 'admin'

    def is_user(self):
        """Returns True if this user has the regular user role."""
        return self.role == 'user'

    # ---------------------------------------------------------------
    # UTILITY
    # ---------------------------------------------------------------

    def to_dict(self):
        """Safe dictionary — never includes password_hash."""
        return {
            'id':         self.id,
            'username':   self.username,
            'email':      self.email,
            'role':       self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<User {self.id}: {self.username} ({self.role})>'
