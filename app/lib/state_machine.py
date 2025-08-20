from statemachine import StateMachine, State


class RoutingStateMachine(StateMachine):
    """
    _route_for_current_state is updated by entering_* methods to indicate the route to be used for the current state
    It is then used by the route handlers to redirect to the correct page after a state transition
    """
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
    For example, "service_person_alive_form" is a State, while "continue_from_initial" 
    would be an Event that triggers a transition to that State. 
    """
    initial = State(initial=True)  # The initial state of our machine
    service_person_alive_form = State(enter="entering_service_person_alive_form", final=True)

    """
    These are our Events. We call these in route methods to trigger transitions between States.

    Be very careful with naming to ensure they are described as an Event.
    For example, "continue_from_initial" is an Event that triggers a transition
    from the "start" State to the "service_person_alive_form" State.
    """
    continue_to_service_person_alive_form = initial.to(service_person_alive_form)

    def entering_service_person_alive_form(self, event, state):
        self.route_for_current_state = "main.is_service_person_alive"
        print(f"State machine: Entering '{state.id}' state in response to '{event}' event. The next route is set to: '{self.route_for_current_state}'")

    def on_exit_state(self, event, state):
        """This method is called when exiting any state."""
        self.route_for_current_state = None
        print(f"State machine: Exiting '{state.id}' state in response to '{event}' event.")
