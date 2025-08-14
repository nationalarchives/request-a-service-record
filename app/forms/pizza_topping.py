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


class PizzaToppings(FlaskForm):
    topping = RadioField(
        "What pizza topping is best?",
        choices=[
            ("plain", "Plain cheese"),
            ("pepperoni", "Pepperoni"),
            ("vegetarian", "Vegetarian"),
            ("hawaiian", "Hawaiian"),
            ("meat_lovers", "Meat Lovers"),
            ("bbq_chicken", "BBQ Chicken"),
            ("other", "Other"),
        ],
        validators=[
            InputRequired(message="Select your favourite pizza topping"),
        ],
        widget=TnaRadiosWidget(),
    )

    submit = SubmitField("Continue", widget=TnaSubmitWidget())
