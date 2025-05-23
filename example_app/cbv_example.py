from nublar.views import BaseView  # Importing the BaseView class for creating views
from response.http_response import text_response  # Importing the text_response function for creating text responses

class AboutView(BaseView):
    def get(self, request, **kwargs):
        return text_response("This is the about page.")