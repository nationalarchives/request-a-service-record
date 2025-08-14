import os

from app.lib.models import db

from app import create_app

app = create_app(
    os.getenv("CONFIG", "config.Production"),
)

with app.app_context():
    db.create_all()
