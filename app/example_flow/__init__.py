from flask import Blueprint

bp = Blueprint("example_flow", __name__)

from app.example_flow import routes  # noqa: E402,F401
