# app/models/__init__.py
# Import all models here so Flask-Migrate can find them.
# Flask-Migrate needs to see all models to generate migrations.


from app.models.user          import User
from app.models.prayer_request import PrayerRequest
from app.models.website_visit  import WebsiteVisit
from app.models.settings       import Settings
from app.models.admin_log      import AdminLog

__all__ = [
    'User',
    'PrayerRequest',
    'WebsiteVisit',
    'Settings',
    'AdminLog'
]
