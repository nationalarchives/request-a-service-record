from app.lib.content import load_content
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from tna_frontend_jinja.wtforms import (
    TnaDateField,
    TnaDroppableFileInputWidget,
    TnaRadiosWidget,
    TnaSelectWidget,
    TnaSubmitWidget,
    TnaTextareaWidget,
    TnaTextInputWidget,
)
from tna_frontend_jinja.wtforms import validators as tna_frontend_validators
from wtforms import (
    EmailField,
    FileField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import Email, InputRequired


class RequestAServiceRecord(FlaskForm):
    content = load_content()

    forenames = StringField(
        content["request_form"]["fields"]["forenames"]["label"],
        widget=TnaTextInputWidget(),
        validators=[
            InputRequired(
                message=content["request_form"]["fields"]["forenames"]["messages"][
                    "required"
                ]
            ),
        ],
    )

    lastname = StringField(
        content["request_form"]["fields"]["last_name"]["label"],
        widget=TnaTextInputWidget(),
        validators=[
            InputRequired(
                message=content["request_form"]["fields"]["last_name"]["messages"][
                    "required"
                ]
            ),
        ],
    )

    other_last_names = StringField(
        content["request_form"]["fields"]["other_last_names"]["label"],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    date_of_birth = TnaDateField(
        content["request_form"]["fields"]["dob"]["label"],
        description=content["request_form"]["fields"]["dob"]["description"],
        validators=[
            InputRequired(
                message=content["request_form"]["fields"]["dob"]["messages"]["required"]
            ),
            tna_frontend_validators.PastDate(
                message=content["request_form"]["fields"]["dob"]["messages"][
                    "past_date"
                ]
            ),
        ],
    )

    place_of_birth = StringField(
        content["request_form"]["fields"]["place_of_birth"]["label"],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    date_of_death = TnaDateField(
        content["request_form"]["fields"]["date_of_death"]["label"],
        description=content["request_form"]["fields"]["date_of_death"]["description"],
        validators=[
            tna_frontend_validators.PastDate(
                message=content["request_form"]["fields"]["date_of_death"]["messages"][
                    "past_date"
                ],
                include_today=True
            ),
        ],
    )

    service_number = StringField(
        content["request_form"]["fields"]["service_number"]["label"],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    regiment = StringField(
        content["request_form"]["fields"]["regiment"]["label"],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    service_branch = RadioField(
        content["request_form"]["fields"]["service_branch"]["label"],
        choices=[
            (key, value)
            for key, value in content["request_form"]["fields"]["service_branch"][
                "options"
            ].items()
        ],
        validators=[
            InputRequired(
                message=content["request_form"]["fields"]["service_branch"]["messages"][
                    "required"
                ]
            )
        ],
        widget=TnaRadiosWidget(),
    )

    mod_reference = StringField(
        content["request_form"]["fields"]["mod_reference"]["label"],
        description=content["request_form"]["fields"]["mod_reference"]["description"],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    additional_information = TextAreaField(
        content["request_form"]["fields"]["additional_information"]["label"],
        description=content["request_form"]["fields"]["additional_information"][
            "description"
        ],
        validators=[],
        widget=TnaTextareaWidget(),
    )

    evidence_of_death = FileField(
        content["request_form"]["fields"]["evidence_of_death"]["label"],
        validators=[
            FileAllowed(
                upload_set=["jpg", "png", "gif"],
                message=content["request_form"]["fields"]["evidence_of_death"][
                    "messages"
                ]["file_allowed"],
            ),
            FileSize(
                max_size=20 * 1024 * 1024,
                message=content["request_form"]["fields"]["evidence_of_death"][
                    "messages"
                ]["file_size"],
            ),
        ],
        widget=TnaDroppableFileInputWidget(),
    )

    died_in_service = RadioField(
        content["request_form"]["fields"]["died_in_service"]["label"],
        choices=[("yes", "Yes"), ("no", "No"), ("unknown", "Unknown")],
        validators=[
            InputRequired(
                message=content["request_form"]["fields"]["died_in_service"][
                    "messages"
                ]["required"]
            )
        ],
        widget=TnaRadiosWidget(),
    )

    case_reference_number = StringField(
        content["request_form"]["fields"]["case_reference_number"]["label"],
        description=content["request_form"]["fields"]["case_reference_number"][
            "description"
        ],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    requester_title = StringField(
        content["request_form"]["fields"]["requester_title"]["label"],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    requester_first_name = StringField(
        content["request_form"]["fields"]["requester_first_name"]["label"],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    requester_last_name = StringField(
        content["request_form"]["fields"]["requester_last_name"]["label"],
        widget=TnaTextInputWidget(),
        validators=[
            InputRequired(
                message=content["request_form"]["fields"]["requester_last_name"][
                    "messages"
                ]["required"]
            )
        ],
    )

    requester_contact_preference = RadioField(
        content["request_form"]["fields"]["contact_preferences"]["label"],
        choices=[("email", "Email"), ("post", "Post")],
        validators=[
            InputRequired(
                message=content["request_form"]["fields"]["contact_preferences"][
                    "messages"
                ]["required"]
            )
        ],
        widget=TnaRadiosWidget(),
    )

    requester_email = EmailField(
        content["request_form"]["fields"]["requester_email"]["label"],
        validators=[
            InputRequired(
                message=content["request_form"]["fields"]["requester_email"][
                    "messages"
                ]["required"]
            ),
            Email(
                message=content["request_form"]["fields"]["requester_email"][
                    "messages"
                ]["address_format"]
            ),
        ],
        widget=TnaTextInputWidget(),
    )

    requester_address1 = StringField(
        content["request_form"]["fields"]["requester_address_line_1"]["label"],
        widget=TnaTextInputWidget(),
        validators=[
            InputRequired(
                message=content["request_form"]["fields"]["requester_address_line_1"][
                    "messages"
                ]["required"]
            )
        ],
    )

    requester_address2 = StringField(
        content["request_form"]["fields"]["requester_address_line_2"]["label"],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    requester_town_city = StringField(
        content["request_form"]["fields"]["requester_town_city"]["label"],
        widget=TnaTextInputWidget(),
        validators=[
            InputRequired(
                message=content["request_form"]["fields"]["requester_town_city"][
                    "messages"
                ]["required"]
            )
        ],
    )

    requester_county = StringField(
        content["request_form"]["fields"]["requester_county"]["label"],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    requester_postcode = StringField(
        content["request_form"]["fields"]["requester_postcode"]["label"],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    requester_country = SelectField(
        content["request_form"]["fields"]["requester_country"]["label"],
        choices=[
            (item, item)
            for item in content["request_form"]["fields"]["requester_country"][
                "countries"
            ]
        ],
        widget=TnaSelectWidget(),
        validators=[
            InputRequired(
                message=content["request_form"]["fields"]["requester_country"][
                    "messages"
                ]["required"]
            )
        ],
    )

    submit = SubmitField("Continue", widget=TnaSubmitWidget())
