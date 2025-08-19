from app.lib.models import db
from flask_app import app

with app.app_context():
    db.create_all()
