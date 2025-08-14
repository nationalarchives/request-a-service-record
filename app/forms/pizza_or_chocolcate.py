from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaRadiosWidget,
    TnaSubmitWidget,
)
from wtforms import (
    RadioField,
    SubmitField,
)
from wtforms.validators import InputRequired


class PizzaOrChocolate(FlaskForm):
    food = RadioField(
        "Do you prefer pizza or chocolate?",
        choices=[
            ("pizza", "Pizza"),
            ("chocolate", "Chocolate"),
            ("neither", "I don't like either"),
            ("cats", "Take me to see cats!"),
        ],
        validators=[
            InputRequired(message="Select your favourite food"),
        ],
        widget=TnaRadiosWidget(),
    )

    submit = SubmitField("Continue", widget=TnaSubmitWidget())
