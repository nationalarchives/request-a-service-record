from flask import Blueprint

bp = Blueprint("main", __name__)

from app.main import routes_shared_by_both_approaches # noqa: E402,F401
from app.main import routes_single_form_journey  # noqa: E402,F401
from app.main import routes_multiple_forms_journey  # noqa: E402,F401
