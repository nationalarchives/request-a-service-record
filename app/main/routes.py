from app.lib.cache import cache, cache_key_prefix
from app.main import bp
from flask import render_template
from app.lib.content import load_content


@bp.route("/")
@cache.cached(key_prefix=cache_key_prefix)
def index():
    content = load_content()
    return render_template("main/index.html", content=content)


@bp.route("/cookies/")
@cache.cached(key_prefix=cache_key_prefix)
def cookies():
    return render_template("main/cookies.html")
