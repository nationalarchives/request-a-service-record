from app.lib.cache import cache, cache_key_prefix
from app.lib.content import load_content
from app.main import bp
from app.main.forms.request_a_service_record import RequestAServiceRecord
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

        return redirect(url_for("main.submitted"))

    return render_template(
        "main/all-fields-in-one-form.html", content=content, form=form
    )


@bp.route("/submitted/")
def submitted():
    content = load_content()
    form_data = session.get("form_data", {})
    return render_template("main/submitted.html", form_data=form_data, content=content)
