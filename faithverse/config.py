# config.py
# This file defines different configurations for your app.
# Think of it like a settings file you can switch between.

import os
from dotenv import load_dotenv

# Load variables from the .env file into Python's environment
load_dotenv()

class Config:
    """Base configuration — settings shared by all environments."""

    # SECRET_KEY is used to sign session cookies and security tokens.
    # Never share this or commit it to GitHub.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-secret-change-this'

    # DATABASE URI tells SQLAlchemy how to connect to your database.
    # Format: dialect+driver://username:password@host:port/database_name
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://prayer_user:PrayerPass2024!@localhost/prayer_db'

    # Disable SQLAlchemy event tracking (saves memory, not needed for most apps)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

class DevelopmentConfig(Config):
    """Development configuration — used while building locally."""

    DEBUG = True   # Shows detailed error messages in the browser


class ProductionConfig(Config):
    """Production configuration — used on a real server."""

    DEBUG = False  # NEVER show error details to users in production


# Dictionary to access configs by name
config = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'default':     DevelopmentConfig
}
