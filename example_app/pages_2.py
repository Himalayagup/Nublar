# app.py
from core.path import path
from response.main import json_response, text_response

BASE_PATH = "/v1/" # can be defined as v1 or v1/ or /v1 or /v1/ recommended to not use / at the start or end


@path("/post", methods=["POST"])
def submit_data(req, method, data):
    name = data.get("name") or "Anonymous"
    if isinstance(name, list):
        name = name[0]
    return text_response(f"Post Received name: {name}")

@path("/json", methods=["GET", "POST"], active=False)
def api_data(req, method, data=None):
    if method == "POST":
        return json_response({"message": "This is a POST JSON Response."}, status=200)
    return json_response({"message": "This is a GET JSON Response."}, status=200)

