from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileSize
from tna_frontend_jinja.wtforms import TnaSubmitWidget, TnaRadiosWidget, TnaTextInputWidget, TnaDateField, TnaTextareaWidget, TnaFileInputWidget
from tna_frontend_jinja.wtforms import validators as tna_frontend_validators
from wtforms import SubmitField, RadioField, StringField, SelectField, TextAreaField, FileField, EmailField, Field
from wtforms.validators import InputRequired, Length, Email
from app.lib.content import load_content

class RequestAServiceRecord(FlaskForm):

    content = load_content()

    forenames = StringField(
        content['request_form']['fields']['forenames']['label'],
        widget=TnaTextInputWidget(),
        validators=[
            InputRequired(message=content['request_form']['fields']['forenames']['messages']['required']),
        ],
    )

    lastname = StringField(
        content['request_form']['fields']['last_name']['label'],
        widget=TnaTextInputWidget(),
        validators=[
            InputRequired(message=content['request_form']['fields']['last_name']['messages']['required']),
        ],
    )

    otherLastNames = StringField(
        content['request_form']['fields']['other_last_names']['label'],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    dateOfBirth = TnaDateField(
        content['request_form']['fields']['dob']['label'],
        description=content['request_form']['fields']['dob']['description'],
        validators=[
            InputRequired(message=content['request_form']['fields']['dob']['messages']['required']),
            tna_frontend_validators.PastDate(
                message=content['request_form']['fields']['dob']['messages']['past_date']
            ),
        ],
    )

    placeOfBirth = StringField(
        content['request_form']['fields']['place_of_birth']['label'],
        widget=TnaTextInputWidget(),
        validators=[]
    )

    dateOfDeath = TnaDateField(
        content['request_form']['fields']['date_of_death']['label'],
        description=content['request_form']['fields']['date_of_death']['description'],
        validators=[
            tna_frontend_validators.PastDate(
                message=content['request_form']['fields']['date_of_death']['messages']['past_date']
            ),
        ],
    )

    serviceNumber = StringField(
        content['request_form']['fields']['service_number']['label'],
        widget=TnaTextInputWidget(),
        validators=[]
    )

    regiment = StringField(
        content['request_form']['fields']['regiment']['label'],
        widget=TnaTextInputWidget(),
        validators=[]
    )

    serviceBranch = RadioField(
        content['request_form']['fields']['service_branch']['label'],
        choices=[(key, value) for key, value in content['request_form']['fields']['service_branch']['options'].items()],
        validators=[
            InputRequired(message=content['request_form']['fields']['service_branch']['messages']['required'])
        ],
        widget=TnaRadiosWidget(),
    )

    modReference = StringField(
        content['request_form']['fields']['mod_reference']['label'],
        description=content['request_form']['fields']['mod_reference']['description'],
        widget=TnaTextInputWidget(),
        validators=[]
    )

    additionalInformation = TextAreaField(
        content['request_form']['fields']['additional_information']['label'],
        description=content['request_form']['fields']['additional_information']['description'],
        validators=[],
        widget=TnaTextareaWidget(),
    )

    evidenceOfDeath = FileField(
        content['request_form']['fields']['evidence_of_death']['label'],
        validators=[
            FileAllowed(
                upload_set=["jpg", "png", "gif"],
                message=content['request_form']['fields']['evidence_of_death']['messages']['file_allowed'],
            ),
            FileSize(max_size=20 * 1024, message=content['request_form']['fields']['evidence_of_death']['messages']['file_size']),
        ],
        widget=TnaFileInputWidget()
    )

    diedInService = RadioField(
        content['request_form']['fields']['died_in_service']['label'],
        choices=[
            ("yes", "Yes"),
            ("no", "No"),
            ("unknown", "Unknown")
        ],
        validators=[
            InputRequired(message=content['request_form']['fields']['died_in_service']['messages']['required'])
        ],
        widget=TnaRadiosWidget()
    )

    caseReferenceNumber = StringField(
        content['request_form']['fields']['case_reference_number']['label'],
        description=content['request_form']['fields']['case_reference_number']['description'],
        widget=TnaTextInputWidget(),
        validators=[]
    )

    requesterTitle = StringField(
        content['request_form']['fields']['requester_title']['label'],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    requesterFirstName = StringField(
        content['request_form']['fields']['requester_first_name']['label'],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    requesterLastName = StringField(
        content['request_form']['fields']['requester_last_name']['label'],
        widget=TnaTextInputWidget(),
        validators=[InputRequired(message=content['request_form']['fields']['requester_last_name']['messages']['required'])],
    )

    requesterContactPreference = RadioField(
        content['request_form']['fields']['contact_preferences']['label'],
        choices=[
            ("email", "Email"),
            ("post", "Post")
        ],
        validators=[
            InputRequired(message=content['request_form']['fields']['contact_preferences']['messages']['required'])
        ],
        widget=TnaRadiosWidget(),
    )

    requesterEmail = EmailField(
        content['request_form']['fields']['requester_email']['label'],
        validators=[
            InputRequired(message=content['request_form']['fields']['requester_email']['messages']['required']),
            Email(message=content['request_form']['fields']['requester_email']['messages']['address_format'])
        ],
        widget=TnaTextInputWidget()
    )

    requesterAddress1 = StringField(
        content['request_form']['fields']['requester_address_line_1']['label'],
        widget=TnaTextInputWidget(),
        validators=[InputRequired(message=content['request_form']['fields']['requester_address_line_1']['messages']['required'])],
    )

    requesterAddress2 = StringField(
        content['request_form']['fields']['requester_address_line_2']['label'],
        widget=TnaTextInputWidget(),
        validators=[],
    )

    requesterTownCity = StringField(
        content['request_form']['fields']['requester_town_city']['label'],
        widget=TnaTextInputWidget(),
        validators=[InputRequired(message=content['request_form']['fields']['requester_town_city']['messages']['required'])],
    )

    requesterCounty = StringField(
        "County (optional)",
        widget=TnaTextInputWidget(),
        validators=[],
    )

    submit = SubmitField("Continue", widget=TnaSubmitWidget())
