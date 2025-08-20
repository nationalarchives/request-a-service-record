from datetime import datetime

from app.lib.cache import cache, cache_key_prefix
from app.lib.content import load_content
from app.lib.db_handler import add_service_record_request
from app.lib.gov_uk_pay import (
    create_payment,
    is_webhook_signature_valid,
    process_webhook_data,
)
from app.main import bp
from app.main.forms.proceed_to_pay import ProceedToPay
from app.main.forms.request_a_service_record import RequestAServiceRecord
from flask import current_app, redirect, render_template, request, session, url_for


@bp.route("/")
@cache.cached(key_prefix=cache_key_prefix)
def index():
    content = load_content()
    return render_template("main/index.html", content=content)


@bp.route("/all-fields-in-one-form/", methods=["GET", "POST"])
def all_fields_in_one_form():
    form = RequestAServiceRecord()
    content = load_content()

    if form.validate_on_submit():
        session["form_data"] = {}
        for field_name, field in form._fields.items():
            if field_name not in ["csrf_token", "submit", "evidence_of_death"]:
                session["form_data"][field_name] = field.data

        return redirect(url_for("main.review"))

    return render_template(
        "main/all-fields-in-one-form.html", content=content, form=form
    )


@bp.route("/review/", methods=["GET", "POST"])
def review():
    content = load_content()
    form = ProceedToPay()
    form_data = session.get("form_data", {})

    if form.validate_on_submit():
        return redirect(url_for("main.send_to_gov_pay"))

    return render_template(
        "main/review.html", form=form, form_data=form_data, content=content
    )


@bp.route("/send-to-gov-uk-pay/")
def send_to_gov_pay():
    content = load_content()
    form_data = session.get("form_data", {})
    requester_email = form_data.get("requester_email", None)

    response = create_payment(
        amount=1000,
        description=content["app"]["title"],
        reference="ServiceRecordRequest",
        email=requester_email,
        return_url=url_for("main.handle_gov_uk_pay_response", _external=True),
    )

    if not response:
        return redirect(url_for("main.payment_link_creation_failed"))
    else:
        payment_url = response.get("_links", {}).get("next_url", "").get("href", "")
        payment_id = response.get("payment_id", "")

        data = {
            **form_data,
            "payment_id": payment_id,
        }

        add_service_record_request(data)

        return redirect(payment_url)


@bp.route("/handle-gov-uk-pay-response/")
def handle_gov_uk_pay_response():
    # This was only temporary logic while we were storing payment_id
    # in session data. Now it's in a DB - we will need a webhook to process
    # the DB item later.
    # payment_id = session.get("payment_id", "")
    # has_paid = check_payment(payment_id)

    # if not has_paid:
    #     return redirect(url_for("main.payment_incomplete"))
    return redirect(url_for("main.confirm_payment_received"))


@bp.route("/payment-link-creation_failed/")
def payment_link_creation_failed():
    content = load_content()
    return render_template("main/payment-link-creation-failed.html", content=content)


@bp.route("/payment-incomplete/")
def payment_incomplete():
    content = load_content()
    return render_template("main/payment-incomplete.html", content=content)


@bp.route("/confirm-payment-received/")
def confirm_payment_received():
    content = load_content()
    return render_template("main/confirm-payment-received.html", content=content)


@bp.route("/gov-uk-pay-webhook/", methods=["POST"])
def gov_uk_pay_webhook():

    if not is_webhook_signature_valid(request):
        return "FAILED", 403

    try:
        process_webhook_data(request.get_json())
    except Exception as e:
        current_app.logger.error(f"Error processing webhook data: {e}")
        return "FAILED", 500

    return "SUCCESS", 200
