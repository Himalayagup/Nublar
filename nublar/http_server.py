from http.server import HTTPServer  # Importing the HTTPServer from Python's standard library
from .request_handler import RequestHandler  # Importing the custom RequestHandler class for handling requests
import settings  # Importing settings to get the server configuration
from .utils import removing_slashes  # Utility function to remove leading/trailing slashes from paths

# Getting the host and port from the settings, or using default values
HOST = getattr(settings, 'HOST', '127.0.0.1')  # Default to '127.0.0.1' if not specified in settings
PORT = getattr(settings, 'PORT', 4000)  # Default to 4000 if not specified in settings

# Ensuring that the port is an integer
PORT = int(PORT) if isinstance(PORT, str) else PORT

# Getting the static folder from settings, or using default 'static'
STATIC_FOLDER = getattr(settings, 'STATIC_FOLDER', 'static')

# If STATIC_FOLDER is not an empty string, remove leading/trailing slashes
if STATIC_FOLDER:
    STATIC_FOLDER = removing_slashes(STATIC_FOLDER)
else:
    STATIC_FOLDER = "static"  # Default to 'static' if not specified

class CoreHTTPServer:
    """
    Core HTTP server class that handles the setup and starting of the HTTP server.
    It uses the Python's built-in HTTPServer and a custom RequestHandler to process incoming requests.
    """

    def __init__(self, host=HOST, port=PORT, static_folder=STATIC_FOLDER):
        """
        Initialize the CoreHTTPServer instance.

        Arguments:
            host: The host IP address or hostname for the server (default is '127.0.0.1').
            port: The port number for the server (default is 4000).
            static_folder: The directory where static files (e.g., images, CSS, JS) are located (default is 'static').
        """
        self.server_address = (host, port)  # Server address tuple (host, port)
        self.static_folder = static_folder  # Static folder path
        self.httpd = HTTPServer(self.server_address, RequestHandler)    # Create HTTP server with the given address and handler


    def start(self):
        """
        Start the HTTP server and listen for incoming requests.
        This method will run the server indefinitely, unless interrupted by a KeyboardInterrupt.
        """
        host, port = self.server_address
        print(f"Starting server at http://{host}:{port}")   # Print the server URL
        print("To shut down the server, press Ctrl+C")

        # Set the static folder for the request handler
        RequestHandler.static_folder = self.static_folder

        try:
            self.httpd.serve_forever()  # Start the server to handle requests indefinitely
        except KeyboardInterrupt:
            # Gracefully shutdown the server on a keyboard interrupt (Ctrl+C)
            print("\nShutting down server.")
            self.httpd.server_close()   # Close the HTTP server

