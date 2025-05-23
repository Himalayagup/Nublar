import re

ROUTES = []

def path(path_pattern, methods=["GET"]):
    # Convert "/user/<id>" → regex with named groups
    pattern = re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", path_pattern)
    regex = re.compile(f"^{pattern}$")

    def decorator(func):
        ROUTES.append({
            "regex": regex,
            "func": func,
            "methods": set(method.upper() for method in methods),
        })
        return func

    return decorator
