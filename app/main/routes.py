from app.lib.cache import cache, cache_key_prefix
from app.lib.content import load_content
from app.main import bp
from app.main.forms.request_a_service_record import RequestAServiceRecord
from flask import redirect, render_template, session, url_for
import boto3
from dicttoxml import dicttoxml
from config import Base

sqs = boto3.client('sqs', region_name=Base.AWS_DEFAULT_REGION)


@bp.route("/")
@cache.cached(key_prefix=cache_key_prefix)
def index():
    content = load_content()
    return render_template("main/index.html", content=content)


@bp.route("/all-fields-form/", methods=["GET", "POST"])
def request_form():
    form = RequestAServiceRecord()
    content = load_content()

    if form.validate_on_submit():
        session["form_data"] = {}
        for field_name, field in form._fields.items():
            if field_name not in ["csrf_token", "submit", "evidence_of_death"]:
                session["form_data"][field_name] = field.data

        return redirect(url_for("main.submitted"))

    return render_template(
        "main/request-a-service-record.html", content=content, form=form
    )


@bp.route("/submitted/")
def submitted():
    content = load_content()
    form_data = session.get("form_data", {})
    xml_bytes = dicttoxml(form_data, custom_root='Request', attr_type=False)
    xml_str = xml_bytes.decode()
    queue_url = Base.SQS_QUEUE_URL

    message = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=xml_str
    )
    print(message)
    return render_template("main/submitted.html", form_data=form_data, content=content)
