from abc import ABC, abstractmethod


class IStateManager(ABC):
    TRANSITIONS: dict
    TERMINAL_TRANSITIONS: dict

    @abstractmethod
    def get_valid_transitions(self, current_state: str):
        raise NotImplementedError("Valid transitions must be implemented")

    @abstractmethod
    def is_valid_transition(self, next_state: str):
        raise NotImplementedError("Is Valid transition must be implemented")

    @abstractmethod
    def transition(self, current_state: str, next_state: str):
        raise NotImplementedError("Transition must be implemented")
