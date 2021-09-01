from abc import abstractmethod, abstractstaticmethod
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
    @abstractmethod
    def setup(self, with_fsm: "BaseFSM"):
        raise NotImplementedError

    @abstractmethod
    def teardown(self):
        raise NotImplementedError


class BaseFSM:
    curr_state: BaseState = None

    def __init__(self, init_state: BaseState, *args, **kwargs) -> None:
        self.curr_state = init_state


class BaseTransition(metaclass=Singleton):
    from_state: List[BaseState] = None
    to_state: BaseState = None

    @abstractstaticmethod
    def transition_action(fsm: BaseFSM):
        raise NotImplementedError

    def __call__(self, fsm: BaseFSM):
        if fsm.curr_state in self.from_state:
            try:
                self.transition_action(fsm)
                fsm.curr_state.teardown()
                self.to_state.setup(with_fsm=fsm)
            except Exception as e:
                raise InvalidStateTransition(
                    f"Unable to perform the transition from {fsm.curr_state.__class__.__name__} to {self.to_state.__class__.__name__}: {e}"
                )
            else:
                fsm.curr_state = self.to_state
                return
        raise InvalidStateTransition(
            f"Unable to perform the transition from {fsm.curr_state.__class__.__name__} to {self.to_state.__class__.__name__}: is not in from_state"
        )
