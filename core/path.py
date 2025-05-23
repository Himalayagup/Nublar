import re
import inspect
from .utils import removing_slashes
ALL_PATHS = []

def path(path_pattern, methods=["GET"], prefix="", active=True, base_routes=False):
    caller_frame = inspect.stack()[1]  # [1] gives the caller's frame
    caller_locals = caller_frame[0].f_locals  # Get local variables from the caller's scope
    if prefix:
        prefix = removing_slashes(prefix)
    caller_base_url = caller_locals.get('BASE_PATH', None)
    if caller_base_url:
        caller_base_url = removing_slashes(caller_base_url)
        full_path = f"/{caller_base_url}/{prefix}{path_pattern}" if prefix else f"/{caller_base_url}{path_pattern}"
    else:
        full_path = f"/{prefix}{path_pattern}" if prefix else path_pattern
    # Convert "/user/<id>" → regex with named groups
    pattern = re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", full_path)
    regex = re.compile(f"^{pattern}$")

    def decorator(func):
        if active:
            ALL_PATHS.append({
                "regex": regex,
                "func": func,
                "methods": set(method.upper() for method in methods),
            })
        if not ALL_PATHS:
            if not active and base_routes:
                # If no active routes are found, add the base route
                ALL_PATHS.append({
                    "regex": regex,
                    "func": func,
                    "methods": set(method.upper() for method in methods),
                })
        return func

    return decorator
