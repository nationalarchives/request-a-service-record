from flask_wtf import FlaskForm
from tna_frontend_jinja.wtforms import TnaTextInputWidget
from wtforms import StringField


class PizzaBrand(FlaskForm):
    brand = StringField(
        "What is your favourite brand?",
        description='Hint: The correct answer is "dominos".',
        widget=TnaTextInputWidget(),
    )
