from abc import ABC , abstractmethod
from enum import StrEnum


class OrderStatus(StrEnum):
    PENDING = "PENDING"
    IN_REVIEW  = "IN_REVIEW"
    ACCEPTED = "ACCEPTED"
    WAIT_FOR_PROCESSING = "WAIT_FOR_PROCESSING"
    PROCESSING = "PROCESSING" 
    PROCESSED = "PROCESSED"
    READY_FOR_DELIVERY = "READY_FOR_DELIVERY"     
    DELIVRED = "DELIVRED"   
    PAIED = "PAIED"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED" 
    REJECTED = "REJECTED"

class StateManager(ABC):
    @abstractmethod
    def get_valid_transitions(self , current_state : str)->set :
        raise NotImplementedError("get valid transitions not implementned")
    

    @abstractmethod
    def is_valid_transition(self , current_state : str , next_state : str)->bool:
        raise NotImplementedError("is valid transition needs to be implemented")

    @abstractmethod
    def validate_transition(self , current_state : str , next_state : str):
        return




class OrderStateManager(StateManager):
    
    VALID_TRANSITIONS: Dict[OrderStatus, Set[OrderStatus]] = {
        OrderStatus.PENDING: {OrderStatus.IN_REVIEW, OrderStatus.CANCELLED},
        OrderStatus.IN_REVIEW: {OrderStatus.ACCEPTED, OrderStatus.REJECTED},
        OrderStatus.ACCEPTED: {OrderStatus.WAIT_FOR_PROCESSING},
        OrderStatus.WAIT_FOR_PROCESSING: {OrderStatus.PROCESSING},
        OrderStatus.PROCESSING: {OrderStatus.PROCESSED},
        OrderStatus.PROCESSED: {OrderStatus.READY_FOR_DELIVERY, OrderStatus.PAID},
        OrderStatus.PAID: {OrderStatus.FINISHED},
        OrderStatus.READY_FOR_DELIVERY: {OrderStatus.DELIVERED},  
    }

    TERMINAL_STATES = {OrderStatus.CANCELLED, OrderStatus.FINISHED, OrderStatus.DELIVERED}

    @classmethod
    def get_valid_transitions(cls, current_state: OrderStatus) -> Set[OrderStatus]:
        if current_state in cls.TERMINAL_STATES:
            return set()
        
        if current_state not in cls.VALID_TRANSITIONS:
            raise InvalidStateError(f"Unknown order status: {current_state}")
        
        return cls.VALID_TRANSITIONS[current_state]

    @classmethod
    def is_valid_transition(cls, current_state: OrderStatus, next_state: OrderStatus) -> bool:
        if current_state is None:
            raise ValueError("Current state is required")
        if next_state is None:
            raise ValueError("Next state is required")

        return next_state in cls.get_valid_transitions(current_state)

    @classmethod
    def validate_transition(cls, current_state: OrderStatus, next_state: OrderStatus) -> None:
        if not cls.is_valid_transition(current_state, next_state):
            valid = cls.get_valid_transitions(current_state)
            raise InvalidTransitionError(
                f"Cannot transition from {current_state.value} to {next_state.value}. "
                f"Valid transitions: {[s.value for s in valid]}"
            )


class TransitionManager : 

    def __init__(self):
        self.order_state_manager = OrderStateManager()

    def transition(self , current_state : str , next_state : str):
        
        OrderState




def test_transition(current_state , next_state):

    transition = TransitionManager()

    if transition.transition(current_state , next_state):
        print(f"transitiong from {current_state} -----> {next_state}")
    else : 
        print("Invalid transition")



if __name__ == "__main__" : 
    test_transition(OrderStatus.PENDING , OrderStatus.IN_REVIEW)
    test_transition(OrderStatus.IN_REVIEW , OrderStatus.ACCEPTED)
    test_transition(OrderStatus.ACCEPTED , OrderStatus.PROCESSING)







