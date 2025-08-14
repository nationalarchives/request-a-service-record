from collections.abc import Callable
from typing import Optional, TypedDict

from flask import current_app, redirect, render_template, request, session, url_for
from flask_wtf import FlaskForm


class FormPages:
    """
    Represents a collection of form pages in a flow.
    Each page can have requirements for completion and can redirect to another page when complete.
    """

    pages: list["FormPage"] = []
    starting_page: "FormPage"

    def __init__(self, pages: list["FormPage"], starting_page: "FormPage"):
        self.pages = pages
        self.starting_page = starting_page

    def get_all_pages(self) -> list["FormPage"]:
        """
        Retrieve all pages in the flow.
        """
        return self.pages

    def get_page_by_slug(self, slug: str) -> Optional["FormPage"]:
        """
        Retrieve a page by its slug.
        """
        return next((page for page in self.pages if page.slug == slug), None)

    def get_starting_page(self) -> "FormPage":
        """
        Get the starting page of the flow.
        """
        return self.starting_page


class PageCompletionRuleFormPage(TypedDict):
    page: "FormPage"
    condition: Optional[Callable]


class PageCompletionRuleFlaskMethod(TypedDict):
    flask_method: str
    condition: Optional[Callable]


class PageCompletionRuleURL(TypedDict):
    url: str
    condition: Optional[Callable]


class FormPage:
    """
    Represents a page in the flow that contains a form.
    Each page has requirements for completion.
    """

    name: str
    slug: str
    description: str
    template: str = "example_flow/form_page.html"
    requires_completion_of: list["FormPage"] = []
    requires_completion_of_any: list["FormPage"] = []
    requires_completion_of_any_fallback: Optional["FormPage"] = None
    requires_responses: tuple["FormPage", str, str] = []
    when_complete: list[
        PageCompletionRuleFormPage
        | PageCompletionRuleFlaskMethod
        | PageCompletionRuleURL
    ] = []
    form: Optional[FlaskForm] = None
    form_class: Optional[FlaskForm] = None

    def __init__(
        self,
        name: str,
        slug: str,
        description: str = None,
        template: str = None,
        form: Optional[FlaskForm] = None,
    ):
        self.name = name
        self.slug = slug
        self.description = description
        if template is not None:
            self.template = template
        if form is not None:
            self.form_class = form

    def require_completion_of(self, *pages: "FormPage"):
        """
        Specify which pages must be completed before this page can be accessed.
        """
        self.requires_completion_of = pages
        return self

    def require_completion_of_any(
        self, pages: list["FormPage"], fallback_page: Optional["FormPage"] = None
    ):
        """
        Specify that at least one of the provided pages must be completed before this page can be accessed.
        If none are completed, redirect to the fallback page.
        """
        self.requires_completion_of_any = pages
        self.requires_completion_of_any_fallback = fallback_page
        return self

    def require_response(self, page: "FormPage", key: str, response: str):
        """
        Specify that a response from the given page is required before this page can be accessed.
        """
        self.requires_responses = (page, key, response)
        return self

    def redirect_when_complete(
        self,
        page: "FormPage" = None,
        flask_method: str = None,
        url: str = None,
        condition: Optional[Callable] = None,
    ):
        """
        Set the page to redirect to when this page is completed.
        """
        if not (page or flask_method or url):
            raise ValueError("Either 'page', 'url' or 'flask_method' must be provided.")
        self.when_complete.append(
            {
                "page": page,
                "url": url,
                "flask_method": flask_method,
                "condition": condition,
            }
        )
        return self

    def get_saved_form_data(self):
        """
        Get the form data from the session or other storage.
        """
        return session[self.slug] if self.slug in session else {}

    def save_form_data(self, form_data: dict):
        """
        Save the form data to the session.
        """
        session[self.slug] = form_data

    def is_complete(self) -> bool:
        """
        Check if the form is complete based on the data provided.
        """
        if self.form:
            return self.form.validate()
        elif self.form_class:
            return self.form_class(obj=self.get_saved_form_data()).validate()
        return True

    def serve(self, **kwargs):
        """
        Start the flow by loading the form data and checking completion status.
        """
        if self.form_class:
            self.form = self.form_class(obj=self.get_saved_form_data())

        for page in self.requires_completion_of:
            print(
                f"Checking completion for required page: {page.slug} as part of {self.slug} - {page.is_complete()}"
            )
            if not page.is_complete():
                current_app.logger.warning(
                    f"Required page '{page.slug}' is not complete."
                )
                return redirect(url_for("example_flow.page", page_slug=page.slug))

        if len(self.requires_completion_of_any):
            any_complete = False
            for page in self.requires_completion_of_any:
                print(
                    f"Checking completion for required page as part of requires_completion_of_any: {page.slug} as part of {self.slug} - {page.is_complete()}"
                )
                if page.is_complete():
                    any_complete = True
                    break
            if not any_complete:
                current_app.logger.warning(
                    "None of the any required pages are complete."
                )
                if self.requires_completion_of_any_fallback:
                    return redirect(
                        url_for(
                            "example_flow.page",
                            page_slug=self.requires_completion_of_any_fallback.slug,
                        )
                    )
                else:
                    return redirect(
                        url_for(
                            "example_flow.page",
                            page_slug=self.requires_completion_of_any[0].slug,
                        )
                    )

        if self.requires_responses:
            (page, key, required_response) = self.requires_responses
            data = page.get_saved_form_data()
            if data.get(key, None) != required_response:
                current_app.logger.warning(
                    f"Required response '{required_response}' not found for key '{key}' in page '{page.slug}'."
                )
                return redirect(url_for("example_flow.page", page_slug=page.slug))

        return self.validate_and_redirect(**kwargs)

    def validate_and_redirect(self, **kwargs):
        """
        Validate the form data when the page is submitted and redirect based on completion status.
        """
        if request.method == "POST" and self.is_complete():
            form_data = self.form.data
            form_data.pop("csrf_token")
            form_data.pop("submit")
            self.save_form_data(form_data)
            if matching_rule := next(
                (
                    rule
                    for rule in self.when_complete
                    if rule["condition"] is None or rule["condition"](form_data)
                ),
                None,
            ):
                if matching_rule["page"]:
                    return redirect(
                        url_for(
                            "example_flow.page", page_slug=matching_rule["page"].slug
                        )
                    )
                if matching_rule["flask_method"]:
                    return redirect(url_for(matching_rule["flask_method"]))
                if matching_rule["url"]:
                    return redirect(matching_rule["url"])
            raise Exception("No matching completion rule found.")
        return render_template(self.template, page=self, form=self.form, **kwargs)
