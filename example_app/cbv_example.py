# views.py
from nublar.views import BaseView
from response.http_response import text_response

class AboutView(BaseView):
    def get(self, request, query=None, **kwargs):
        return text_response("This is the CBV about page.")
