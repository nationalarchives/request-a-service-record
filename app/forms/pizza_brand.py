from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import (
    TnaSubmitWidget,
    TnaTextInputWidget,
)
from wtforms import (
    StringField,
    SubmitField,
)
from wtforms.validators import Optional


class PizzaBrand(FlaskForm):
    brand = StringField(
        "What is your favourite brand?",
        description="This is optional.",
        validators=[Optional()],
        widget=TnaTextInputWidget(),
    )

    submit = SubmitField("Continue", widget=TnaSubmitWidget())
