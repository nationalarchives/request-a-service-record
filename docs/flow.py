from typing import Optional

from flask_wtf import FlaskForm


class FormPages:
    """
    Represents a collection of form pages in a flow.
    Each page can have requirements for completion and can redirect to another page when complete.
    """

    def __init__(self, pages=["FormPage"]):
        self.pages = pages

    def get_page_by_url(self, url: str) -> Optional["FormPage"]:
        """
        Retrieve a page by its URL.
        """
        for page in self.pages:
            if page.url == url:
                return page
        return None

    def are_all_complete(self) -> bool:
        """
        Check if all pages in the flow are complete.
        """
        return all(page.is_complete() for page in self.pages)


class FormPage:
    """
    Represents a page in the flow that contains a form.
    Each page has requirements for completion.
    """

    name: str
    url: str
    description: str
    requires_completion_of: list["FormPage"] = []
    when_complete: Optional["FormPage"] = None
    form: Optional[FlaskForm] = None
    form_data: dict = {}

    def __init__(
        self, name: str, url: str, description: str, form: Optional[FlaskForm] = None
    ):
        self.name = name
        self.url = url
        self.description = description
        self.form = form

    def require_completion_of(self, *pages: "FormPage"):
        """
        Specify which pages must be completed before this page can be accessed.
        """
        self.requires_completion_of.extend(pages)
        return self

    def redirect_when_complete(self, page: "FormPage"):
        """
        Set the page to redirect to when this page is completed.
        """
        self.when_complete = page
        return self

    def load_form_data(self):
        """
        Load the form data from the session or other storage.
        """
        self.form_data = {}  # This would typically load from session or database

    def start(self):
        """
        Start the flow by loading the form data and checking completion status.
        """
        self.load_form_data()
        if incomplete_requirement := next(
            [form for form in self.requires_completion_of if not form.is_complete()]
        ):
            print(f"Please complete {incomplete_requirement.name} first.")
            # redirect to incomplete_requirement.url
            pass
        else:
            # proceed to render this page and display self.form (if there is one)
            pass

    def save_form_data(self, form_data: dict):
        """
        Save the form data to the session.
        """
        self.form_data = form_data

    def is_complete(self) -> bool:
        """
        Check if the form is complete based on the data provided.
        """
        return self.form(self.form_data).validate()

    def validate_and_redirect(self, form_data: dict):
        """
        Validate the form data when the page is submitted and redirect based on completion status.
        """
        self.save_form_data(form_data)
        if self.is_complete():
            # redirect to self.when_complete
            pass
        else:
            # refresh this page with self.form (if there is one) and show any errors
            pass


# Construct some example pages for a flow
page_1 = FormPage(
    name="Page 1",
    url="/page-1/",
    description="This is the first page of the flow.",
    form=FlaskForm(),  # Replace with actual form class
)

page_2 = FormPage(
    name="Page 2",
    url="/page-2/",
    description="This is the second page of the flow.",
    form=FlaskForm(),  # Replace with actual form class
)

final_page = FormPage(
    name="Final Page",
    url="/final-page/",
    description="This is the final page of the flow. There is no form here.",
)

# Define the flow
page_1.redirect_when_complete(page_2)
page_2.require_completion_of(page_1).redirect_when_complete(final_page)
final_page.require_completion_of(page_1, page_2)

# Create a flow with the pages - we can use this to query for pages
all_pages = FormPages(pages=[page_1, page_2, final_page])


# ----- USAGE IN THE APPLICATION -----

# 1. User visits /request-a-service-record/page-1/

# 2. Get the page by URL
page_requested = all_pages.get_page_by_url("/page-1/")

# 3. Start the flow for that page
if page_requested:
    page_requested.start()  # Get either a redirect or a rendered page to return
else:
    print("Page not found.")
    # Handle the case where the page does not exist, e.g., redirect to an error page
