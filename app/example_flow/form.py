from app.forms import FormPage, FormPages
from app.forms.pizza_brand import PizzaBrand
from app.forms.pizza_or_chocolcate import PizzaOrChocolate
from app.forms.pizza_topping import PizzaToppings
from app.forms.type_of_chocolate import TypeOfChocolate

# Set up all the required pages
pizza_or_chocolate = FormPage(
    name="Pizza or Chocolate", slug="pizza-or-chocolate", form=PizzaOrChocolate
)
pizza_topping = FormPage(
    name="Pizza toppings", slug="pizza-topping", form=PizzaToppings
)
pizza_brand = FormPage(name="Pizza brand", slug="pizza-brand", form=PizzaBrand)
type_of_chocolate = FormPage(
    name="Type of Chocolate", slug="type-of-chocolate", form=TypeOfChocolate
)
final_page = FormPage(
    name="Final Page",
    slug="final-page",
    description="This is the final page of the flow.",
    template="example_flow/final_page.html",
)

# Handle the flow logic for different options
pizza_or_chocolate.redirect_when_complete(
    page=pizza_topping,
    condition=lambda form_data: form_data.get("food") == "pizza",
)
pizza_or_chocolate.redirect_when_complete(
    page=type_of_chocolate,
    condition=lambda form_data: form_data.get("food") == "chocolate",
)
pizza_or_chocolate.redirect_when_complete(
    flask_method="example_flow.fail",
    condition=lambda form_data: form_data.get("food") == "neither",
)
pizza_or_chocolate.redirect_when_complete(
    url="https://www.reddit.com/r/catpictures/",
    condition=lambda form_data: form_data.get("food") == "cats",
)

# Require certain responses before proceeding
pizza_topping.require_response(
    pizza_or_chocolate, "food", "pizza"
).redirect_when_complete(page=pizza_brand)
type_of_chocolate.require_response(
    pizza_or_chocolate, "food", "chocolate"
).redirect_when_complete(page=final_page)

# Require the completion of previous pages
pizza_brand.redirect_when_complete(page=final_page).require_completion_of(
    pizza_topping
).redirect_when_complete(page=final_page)

# Require completion of any of the previous pages
final_page.require_completion_of_any(
    [pizza_brand, type_of_chocolate], pizza_or_chocolate
)

# Put everything together in a FormPages instance so we can handle all the logic
example_form_flow = FormPages(
    pages=[
        pizza_or_chocolate,
        pizza_topping,
        pizza_brand,
        type_of_chocolate,
        final_page,
    ],
    starting_page=pizza_or_chocolate,
)
