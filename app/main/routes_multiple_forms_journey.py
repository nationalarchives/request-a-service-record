from app.lib.cache import cache, cache_key_prefix
from app.lib.content import load_content
from app.main import bp
from flask import redirect, render_template, session, url_for


@bp.route("/start/")
@cache.cached(key_prefix=cache_key_prefix)
def start():
    content = load_content()
    return render_template("main/multi-page-journey/start.html", content=content)
