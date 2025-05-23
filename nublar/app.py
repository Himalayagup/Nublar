# app.py
from nublar.path import path
from response.http_response import template_response
from response import status_codes

@path("/", methods=["GET"], active=False, base_routes=True)
def submit_data(req, method):
    template_name = "homepage.html"
    return template_response(template_name, status=status_codes.HTTP_200_OK)
