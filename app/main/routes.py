from app.lib.cache import cache, cache_key_prefix
from app.lib.content import load_content
from app.main import bp
from app.main.forms.request_a_service_record import RequestAServiceRecord
from flask import redirect, render_template, session, url_for
from config import Base
import requests


@bp.route("/")
@cache.cached(key_prefix=cache_key_prefix)
def index():
    content = load_content()
    return render_template("main/index.html", content=content)


@bp.route("/all-fields-form", methods=["GET", "POST"])
def request_form():
    form = RequestAServiceRecord()
    content = load_content()

    if form.validate_on_submit():
        session["form_data"] = {}
        for field_name, field in form._fields.items():
            if field_name not in ["csrf_token", "submit", "evidence_of_death"]:
                session["form_data"][field_name] = field.data

        headers = {
            "Authorization": f"Bearer {Base.GOV_UK_PAY_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "amount": 1000,
            "description": "Request a Service Record",
            "reference": "ServiceRecordRequest", # TODO: Investigate the dynamic reference that other/current services use (TNA-xxxxx?)
            "return_url": url_for("main.submitted", _external=True),
        }

        response = requests.post(
            Base.GOV_UK_PAY_API_URL,
            json=payload,
            headers=headers
        )

        if response.status_code != 201:
            print("Error creating payment:", response.status_code, response.json())
            return render_template("main/request-a-service-record.html", content=content, form=form, error="Payment creation failed. Please try again.")
        else:
            session["payment_url"] = response.json().get("_links", {}).get("next_url", "").get("href", "")
            session["payment_id"] = response.json().get("payment_id", "")
            return redirect(session["payment_url"])

    return render_template(
        "main/request-a-service-record.html", content=content, form=form
    )


@bp.route("/submitted/")
def submitted():
    content = load_content()
    form_data = session.get("form_data", {})
    return render_template("main/submitted.html", form_data=form_data, content=content)
