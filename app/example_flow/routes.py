from app.example_flow import bp
from flask import abort, redirect, render_template, session, url_for

from .form import example_form_flow


@bp.route("/")
def start():
    session.clear()
    starting_page = example_form_flow.get_starting_page()
    print(f"Starting page slug: {starting_page.slug}")
    return redirect(url_for("example_flow.page", page_slug=starting_page.slug))


@bp.route("/fail/")
def fail():
    return render_template("example_flow/fail_page.html")


@bp.route("/<string:page_slug>/", methods=["GET", "POST"])
def page(page_slug):
    if form_page := example_form_flow.get_page_by_slug(page_slug):
        return form_page.serve(pages=example_form_flow.get_all_pages())
    abort(404)
