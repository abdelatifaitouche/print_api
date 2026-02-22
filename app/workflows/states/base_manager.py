from .interface import IStateManager


class BaseManager(IStateManager):
    def get_valid_transitions(self, current_state: str) -> dict:
        if not current_state:
            return None

        if current_state not in self.TRANSITIONS.keys():
            raise KeyError("Invalid State")

        return self.TRANSITIONS[current_state]

    def is_valid_transition(self, current_state: str) -> bool:
        valid_transitions: dict = self.get_valid_transitions(current_state)

        if not valid_transitions:
            return False

        return True

    def transition(self, current_state: str):
        if not self.is_valid_transition(current_state):
            return None

        return self.get_valid_transitions(current_state)
