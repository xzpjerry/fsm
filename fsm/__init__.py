from abc import abstractstaticmethod
from typing import List


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FSMError(Exception):
    ...


class InvalidStateTransition(FSMError):
    ...


class BaseState(metaclass=Singleton):
    def __str__(self) -> str:
        return self.__class__.__name__


class BaseFSM:
    """
    FSM stores a concrete state recording its current
    state
    """

    curr_state: BaseState = None

    def __init__(self, init_state: BaseState, *args, **kwargs) -> None:
        self.curr_state = init_state


class BaseTransition(metaclass=Singleton):
    """
    A Transition checks for the FSM's current state
    and decide whether to perform the transition or not.
    """

    from_state: List[BaseState] = None
    to_state: BaseState = None

    @abstractstaticmethod
    def before_state_change(with_fsm: BaseFSM):
        raise NotImplementedError

    @abstractstaticmethod
    def after_state_change(with_fsm: "BaseFSM"):
        raise NotImplementedError

    def __call__(self, fsm: BaseFSM):
        if fsm.curr_state in self.from_state:
            try:
                # actions before state-change
                self.before_state_change(with_fsm=fsm)
            except Exception as e:
                raise InvalidStateTransition(
                    f"Unable to perform the transition from {fsm.curr_state} to {self.to_state}: {e}"
                )

        if fsm.curr_state in self.from_state:
            # state-change
            fsm.curr_state = self.to_state
            # actions after state-change
            try:
                self.after_state_change(with_fsm=fsm)
            except Exception as e:
                raise InvalidStateTransition(
                    f"Unable to perform the transition from {fsm.curr_state} to {self.to_state}: {e}"
                )
            else:
                return
        raise InvalidStateTransition(
            f"Unable to perform the transition from {fsm.curr_state} to {self.to_state}: src state is not in {[str(state) for state in self.from_state]}"
        )
