# core/prefix_url_path.py
from .path import path

def add_prefix_to_routes(module, prefix):
    # Go through all the functions in the module and add the prefix to them
    for name in dir(module):
        func = getattr(module, name)
        if callable(func) and hasattr(func, '__wrapped__'):  # Check if it's decorated
            # Reapply the prefix to each route dynamically
            if hasattr(func, 'prefix'):  # If the function has the 'prefix' attribute
                # Apply the prefix to the wrapped function
                func.__wrapped__ = path(func.__wrapped__.__name__, prefix=prefix)(func.__wrapped__)
            else:
                # Add the prefix to the function's route definition
                path(func.__name__, methods=["GET"], prefix=prefix)(func)
    return module
