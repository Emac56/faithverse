# FaithVerse Backend

Python Flask backend for the FaithVerse prayer community platform.

## Tech Stack

- Python Flask
- MySQL (MariaDB via Termux)
- Flask SQLAlchemy + Flask Migrate
- Flask-Login + Flask-Bcrypt
- Tailwind CSS CDN
- Vanilla JavaScript (Fetch API)

## Phases Completed

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Flask + MySQL Setup | ✅ Done |
| Phase 2 | Database Models & Migrations | ✅ Done |
| Phase 3 | Authentication System | ✅ Done |
| Phase 4 | Dashboard Backend APIs | ✅ Done |
| Phase 5 | Tailwind CSS Dashboard UI | ✅ Done |
| Phase 6 | JavaScript Interactivity | ✅ Done |

## JavaScript Architecture

| File | Responsibility |
|---|---|
| sidebar.js | Mobile sidebar toggle |
| toast.js | Success/error notifications |
| modal.js | Confirmation popups |
| search.js | Live table filtering |
| dashboard.js | AJAX actions + stat refresh |

## API Routes

### Public (no login)
- GET /api/ping
- GET /api/site-info
- POST /api/prayer-request

### Admin (login required)
- GET /dashboard/
- GET /dashboard/stats
- GET /dashboard/users
- GET /dashboard/prayers
- GET /dashboard/analytics
- POST /dashboard/prayers/<id>/approve
- POST /dashboard/prayers/<id>/answer
- DELETE /dashboard/prayers/<id>/delete
- POST /dashboard/users/<id>/promote
- DELETE /dashboard/users/<id>/delete

## Getting Started (Termux)

```bash
# Start MySQL
mysqld_safe -u $(whoami) &

# Activate environment
cd ~/FaithVerse/backend
source venv/bin/activate

# Run server
python run.py
