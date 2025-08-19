from app.lib.cache import cache, cache_key_prefix
from app.lib.content import load_content
from app.main import bp
from app.main.forms.start_now import StartNow
from flask import redirect, render_template, session, url_for


@bp.route("/start/", methods=["GET", "POST"])
@cache.cached(key_prefix=cache_key_prefix)
def start():
    content = load_content()
    form = StartNow()

    if form.validate_on_submit():
        #TODO: Redirect to next step in the multi-page journey
        pass

    return render_template(
        "main/multi-page-journey/start.html", form=form, content=content
    )
