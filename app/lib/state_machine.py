from statemachine import StateMachine, State


class RoutingStateMachine(StateMachine):
    # _route_for_current_state is updated by entering_* methods to indicate the route to be used for the current state
    # It is used by the route handlers to redirect to the correct page after a state transition
    _route_for_current_state = None

    @property
    def route_for_current_state(self):
        return self._route_for_current_state

    @route_for_current_state.setter
    def route_for_current_state(self, value):
        self._route_for_current_state = value

    """
    These are our States. They represent the different stages of our process.
    
    We call callbacks when entering these States to set the attributes that will be used
    in the route methods.
    
    Be very careful with naming to ensure they are described a State, not an Event. 
    For example, "showing_form" is a State, while "show_form" would be an Event that 
    triggers a transition to that State. 
    
    TRUST ME: if you mix these up, it will cause confusion and make you hate working
    with state machines
    """
    initial = State(initial=True)  # The initial state of our machine
    showing_form = State()
    showing_form_with_errors = State()
    showing_submitted_data = State(enter="entering_showing_submitted_data")
    going_to_payment = State(enter="entering_going_to_payment")

    """
    These are our Events. We call these in route methods to trigger transitions between States.
    
    Be very careful with naming to ensure they are described as an Event.
    For example, "valid_form_submitted" is an Event that triggers a transition
    from the "initial" State to the "showing_submitted_data" State.
    
    TRUST ME: if you have States described to sound like Events (or vice versa), it will 
    cause confusion and make you hate working with state machines
    """
    show_form = initial.to(showing_form)
    valid_form_submitted = initial.to(showing_submitted_data)
    invalid_form_submitted = initial.to(showing_form_with_errors)
    continue_to_payment = initial.to(going_to_payment)

    def entering_showing_submitted_data(self):
        self.route_for_current_state = "main.review"
        print(f"Entering showing_submitted_data state. The next route is set to: {self.route_for_current_state}")

    def entering_going_to_payment(self):
        self.route_for_current_state = "main.send_to_gov_pay"
        print(f"Entering going_to_payment state. The next route is set to: {self.route_for_current_state}")

    def on_exit_state(self, event, state):
        """This method is called when exiting any state."""
        self.route_for_current_state = None
        print(f"Exiting '{state.id}' state from '{event}' event.")

