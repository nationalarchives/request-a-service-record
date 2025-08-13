import os

from app import create_app
from app.lib.models import db

app = create_app(
    os.getenv("CONFIG", "config.Production"),
)

with app.app_context():
    db.create_all()