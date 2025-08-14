from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import TnaRadiosWidget
from wtforms import RadioField
from wtforms.validators import InputRequired


class TypeOfChocolate(FlaskForm):
    chocolate_preference = RadioField(
        "Which type of chocolate do you prefer?",
        choices=[
            ("dark", "Dark Chocolate"),
            ("milk", "Milk Chocolate"),
            ("white", "White Chocolate"),
        ],
        validators=[
            InputRequired(message="Select your favourite type of chocolate"),
        ],
        widget=TnaRadiosWidget(),
    )
