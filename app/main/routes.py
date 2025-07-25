import requests
from app.lib.cache import cache, cache_key_prefix
from app.lib.content import load_content
from app.main import bp
from app.main.forms.request_a_service_record import RequestAServiceRecord
from config import Base
from flask import redirect, render_template, session, url_for
from app.lib.gov_uk_pay import create_payment

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

        response = create_payment(
            amount=1000,
            description="Request a Service Record",
            reference="ServiceRecordRequest",
            return_url=url_for("main.submitted", _external=True),
        )

        if not response:
            return render_template(
                "main/request-a-service-record.html",
                content=content,
                form=form,
                error="Payment link creation failed. Please try again.",
            )
        else:
            session["payment_url"] = (
                response.get("_links", {}).get("next_url", "").get("href", "")
            )
            session["payment_id"] = response.get("payment_id", "")
            return redirect(session["payment_url"])

    return render_template(
        "main/request-a-service-record.html", content=content, form=form
    )


@bp.route("/submitted/")
def submitted():
    content = load_content()
    form_data = session.get("form_data", {})
    payment_id = session.get("payment_id", "")
    return render_template("main/submitted.html", form_data=form_data, content=content, payment_id=payment_id)
