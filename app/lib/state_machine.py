from statemachine import StateMachine, State


class RoutingStateMachine(StateMachine):
    # These are our states. Be very careful with naming to ensure they
    # represent a state not an event. For example, "showing_form" is a state,
    # while "show_form" would be an event that triggers a transition to that state.
    # TRUST ME: if you mix these up, it will cause confusion and make you hate working
    # with state machines
    initial = State(initial=True)  # The initial state of our machine
    showing_form = State()
    showing_form_with_errors = State()
    showing_submitted_data = State(value="main.review")
    going_to_payment = State(value="main.send_to_gov_pay")

    # These are our transitions. They define how we move from one state to another.
    # Be very careful with naming to ensure they represent an event that triggers a transition.
    # For example, "valid_form_submitted" is an event that triggers a transition to the
    # "showing_submitted_data" state.
    # TRUST ME: if you mix these up, it will cause confusion and make you hate working
    # with state machines
    show_form = initial.to(showing_form)
    valid_form_submitted = initial.to(showing_submitted_data)
    invalid_form_submitted = initial.to(showing_form_with_errors)
    continue_to_payment = initial.to(going_to_payment)

    def before_transition(self, event, state):
        print(f"Before '{event}', on the '{state.id}' state.")
        return "before_transition_return"

    def on_transition(self, event, state):
        print(f"On '{event}', on the '{state.id}' state.")
        return "on_transition_return"

    def on_exit_state(self, event, state):
        print(f"Exiting '{state.id}' state from '{event}' event.")

    def on_enter_state(self, event, state):
        print(f"Entering '{state.id}' state from '{event}' event.")

    def after_transition(self, event, state):
        print(f"After '{event}', on the '{state.id}' state.")
