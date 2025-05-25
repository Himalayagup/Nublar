# nublar/urls.py
import re
from nublar.path import ALL_PATHS
from nublar.utils import removing_slashes

class URLs:
    def register(self, route_path, view_cls, methods=None):
        """
        Register a class-based view at a given path.
        """
        methods = methods or ["GET", "POST", "PUT", "PATCH", "DELETE"]
        pattern = re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", route_path)
        regex = re.compile(f"^{pattern}$")

        def cbv_wrapper(req, method, query=None, data=None, headers=None, **kwargs):
            view_instance = view_cls()
            return view_instance.dispatch(req, method, query=query or {}, data=data or {}, headers=headers or {}, **kwargs)

        ALL_PATHS.append({
            "regex": regex,
            "func": cbv_wrapper,
            "methods": set(methods),
        })
