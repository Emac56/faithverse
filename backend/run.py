# run.py
# Entry point for the Flask development server.
# Run this file with: python run.py

import os
from app import create_app

# Get the environment from the ENV variable, default to 'development'
config_name = os.environ.get('FLASK_ENV', 'development')

# Create the Flask app
app = create_app(config_name)

if __name__ == '__main__':
    # host='0.0.0.0' makes the server reachable from your phone's browser
    # and from other devices on the same Wi-Fi network.
    # port=5000 is Flask's default port.
    # debug=True reloads the server automatically when you change code.
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
