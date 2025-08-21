from app.lib.cache import cache, cache_key_prefix
from app.lib.content import load_content
from app.lib.state_machine.state_machine_decorator import with_state_machine
from app.main import bp
from app.main.forms.start_now import StartNow
from app.main.forms.is_service_person_alive import IsServicePersonAlive
from flask import redirect, render_template, session, url_for

@cache.cached(key_prefix=cache_key_prefix)
@bp.route("/start/", methods=["GET"])
def start():
    content = load_content()
    form = StartNow()

    return render_template(
        "main/multi-page-journey/start.html", form=form, content=content
    )

@bp.route("/start/", methods=["POST"])
@cache.cached(key_prefix=cache_key_prefix)
@with_state_machine
def start_post(state_machine):
    content = load_content()
    form = StartNow()

    if form.validate_on_submit():
        state_machine.continue_to_service_person_alive_form()
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/multi-page-journey/start.html", form=form, content=content
    )

@bp.route("/is-service-person-alive/", methods=["GET", "POST"])
@cache.cached(key_prefix=cache_key_prefix)
@with_state_machine
def is_service_person_alive(state_machine):
    content = load_content()
    form = IsServicePersonAlive()

    if form.validate_on_submit():
        state_machine.continue_from_is_service_person_alive()
        return redirect(url_for(state_machine.route_for_current_state))

    return render_template(
        "main/multi-page-journey/is-service-person-alive.html", form=form, content=content
    )
