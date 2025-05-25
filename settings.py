# settings.py

# Debug mode configuration
# Set to True to enable debugging, False to disable.
# In debugging mode, the server will automatically reload on code changes (To Be Added).
DEBUG_CODE = True

# Port configuration
# The port the server will listen on. Default is 4000.
# You can change this to another port if needed.
PORT = 4000

# Host configuration
# The IP address or hostname for the server. Default is '127.0.0.1'.
# If you want to access the server from other devices, change it to '0.0.0.0' or your local network IP.
HOST = "127.0.0.1"

# Static folder configuration
# The directory where static files (e.g., CSS, JavaScript, images) are stored.
# The default folder name is 'static'. You can change this to a different folder if needed.
STATIC_FOLDER = "static"

# Template folder configuration
# The directory where HTML templates are stored. Default is 'templates'.
# If you store your templates in another folder, update this value.
# This gives first default value to any templates folder in app level directory if template not found then it moves to global templates folder
TEMPLATE_FOLDER = "templates"

ALL_APPS = [
    "example_app",
]