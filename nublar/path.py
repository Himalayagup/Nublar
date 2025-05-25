import re  # Import regular expression module to convert path patterns into regex
import inspect  # To get information about the calling function (i.e., caller's frame)
from .utils import removing_slashes  # Utility function to clean up slashes in paths

# Global list to store all registered routes
ALL_PATHS = []

def path(path_pattern, methods=["GET"], prefix="", active=True, base_routes=False):
    """
    A decorator to register routes for the HTTP server.

    Arguments:
        path_pattern (str): The path pattern (e.g., '/user/<id>').
        methods (list): List of HTTP methods that the route should accept (default is ["GET"]).
        prefix (str): An optional prefix for the route (default is "").
        active (bool): Whether the route is active or not (default is True).
        base_routes (bool): If True, add the base route when no other routes are active (default is False).

    Returns:
        decorator: The decorator function to register the route.
    """

    # Get the caller's frame to access the local variables
    caller_frame = inspect.stack()[1]  # [1] gives the caller's frame
    caller_locals = caller_frame[0].f_locals  # Get local variables from the caller's scope

    # Clean up the prefix (remove leading/trailing slashes if any)
    if prefix:
        prefix = removing_slashes(prefix)

    # Check if there's a BASE_PATH in the caller's local variables
    caller_base_url = caller_locals.get('BASE_PATH', None)

    # If BASE_PATH exists, construct the full route by combining it with the prefix and path pattern
    if caller_base_url:
        caller_base_url = removing_slashes(caller_base_url)     # Clean the base path
        full_path = f"/{caller_base_url}/{prefix}{path_pattern}" if prefix else f"/{caller_base_url}{path_pattern}"
    else:
        full_path = f"/{prefix}{path_pattern}" if prefix else path_pattern

    # Convert the path pattern (e.g., "/user/<id>") to a regex pattern (e.g., "/user/(?P<id>[^/]+)")
    pattern = re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", full_path)
    regex = re.compile(f"^{pattern}$")

    def decorator(func):
        """
        The actual decorator function to register the route with the provided function.
        """

        # If the route is active, add it to the ALL_PATHS list
        if active:
            ALL_PATHS.append({
                "regex": regex,
                "func": func,
                "methods": set(method.upper() for method in methods),      # Ensure methods are in uppercase
            })

        # If no routes are active, and base_routes is True, add the base route to ALL_PATHS
        if not ALL_PATHS:
            if not active and base_routes:
                # If no active routes are found, add the base route
                ALL_PATHS.append({
                    "regex": regex,
                    "func": func,
                    "methods": set(method.upper() for method in methods),
                })
        return func  # Return the original function as the decorated function

    return decorator  # Return the decorator function
