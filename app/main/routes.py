from app.lib.cache import cache, cache_key_prefix
from app.lib.content import load_content
from app.lib.gov_uk_pay import create_payment
from app.main import bp
from app.main.forms.request_a_service_record import RequestAServiceRecord
from app.main.forms.proceed_to_pay import ProceedToPay
from flask import redirect, render_template, session, url_for


@bp.route("/")
@cache.cached(key_prefix=cache_key_prefix)
def index():
    session["entered_through_index_page"] = True

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

    return render_template("main/review.html", form=form, form_data=form_data, content=content)


@bp.route("/send-to-govuk-pay/")
def send_to_gov_pay():
    return "Send the user to GOV.UK Pay for payment processing."


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
