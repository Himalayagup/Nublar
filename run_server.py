# Import the necessary components to start the HTTP server
from nublar.http_server import CoreHTTPServer  # The custom HTTP server class
import settings  # Settings module to fetch server configurations
import app  # Import the app (not directly used here, but may be part of the app setup)
import nublar.app  # Import the core application logic

# Get the host and port from the settings module, falling back to default values if not defined
HOST = getattr(settings, 'HOST', '127.0.0.1')  # Default to '127.0.0.1' if HOST is not specified
if not HOST:  # If HOST is None or an empty string, set it to '127.0.0.1'
    HOST = '127.0.0.1'

# Get the port from the settings module and ensure it's an integer
PORT = getattr(settings, 'PORT', 4000)  # Default to 4000 if PORT is not specified
if not PORT:  # If PORT is None or an empty string, set it to 4000
    PORT = 4000
else:
    PORT = int(PORT) if isinstance(PORT, str) else PORT  # Ensure PORT is an integer, even if passed as a string

# Main block of code to run when this script is executed
if __name__ == "__main__":
    # Create an instance of the CoreHTTPServer with the host and port settings
    server = CoreHTTPServer(host=HOST, port=PORT)

    # Start the server, this will block and run the server indefinitely
    server.start()
