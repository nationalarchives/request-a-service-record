from flask import current_app, redirect, request, session, url_for
from app.lib.util import get_path

def routing_middleware(app_or_blueprint):
    @app_or_blueprint.before_request
    def allow_progress():
        exempt_routes = ["static", "healthcheck.healthcheck"]

        if request.endpoint and any(
                request.endpoint.startswith(route) for route in exempt_routes
        ):
            return

        if not request.referrer:
            return

        print("========================================")
        print(f"Request referrer: {get_path(request.referrer)}")
        print(f"Request path: {request.path}")
        print("========================================")
