import random
import string

from fsm import BaseFSM, BaseState, BaseTransition, InvalidStateTransition


class Ready(BaseState):
    ...


class Paused(BaseState):
    ...


class Locked(BaseState):
    ...


class Playing(BaseState):
    ...


class Lock(BaseTransition):
    from_state = [Ready(), Playing(), Paused()]
    to_state = Locked()

    @staticmethod
    def before_state_change(with_fsm: "AudioPlayer"):
        print("Transiting to Locked")

    @staticmethod
    def after_state_change(with_fsm: "AudioPlayer"):
        print("Player is Locked")


class Unlock(BaseTransition):
    from_state = [Locked()]
    to_state = Ready()

    @staticmethod
    def before_state_change(with_fsm: "AudioPlayer"):
        print("Transiting to Ready")

    @staticmethod
    def after_state_change(with_fsm: "AudioPlayer"):
        print("Player is Ready")


class Resume(BaseTransition):
    from_state = [Paused(), Ready()]
    to_state = Playing()

    @staticmethod
    def before_state_change(with_fsm: "AudioPlayer"):
        print("Transiting to Playing")
        with_fsm.start_playback()

    @staticmethod
    def after_state_change(with_fsm: "AudioPlayer"):
        print("Player is Playing")


class Pause(BaseTransition):
    from_state = [Playing()]
    to_state = Paused()

    @staticmethod
    def before_state_change(with_fsm: "AudioPlayer"):
        print("Transiting to Paused")

    @staticmethod
    def after_state_change(with_fsm: "AudioPlayer"):
        print("Player is Paused")


class PlayNext(BaseTransition):
    from_state = [Paused(), Ready(), Playing()]
    to_state = Playing()

    @staticmethod
    def before_state_change(with_fsm: "AudioPlayer"):
        print("Transiting to Playing")
        next_song = with_fsm.get_next_song_name()
        print("About to play", next_song)
        with_fsm.play(next_song)

    @staticmethod
    def after_state_change(with_fsm: "AudioPlayer"):
        print("Player is Playing")


class PlayPrev(BaseTransition):
    from_state = [Paused(), Ready(), Playing()]
    to_state = Playing()

    @staticmethod
    def before_state_change(with_fsm: "AudioPlayer"):
        print("Transiting to Playing")
        prev_song = with_fsm.get_previous_song_name()
        print("About to play", prev_song)
        with_fsm.play(prev_song)

    @staticmethod
    def after_state_change(with_fsm: "AudioPlayer"):
        print("Player is Playing")


class AudioPlayer(BaseFSM):
    # UI Delegate methods
    def click_lock(self):
        if self.curr_state is Locked():
            Unlock()(self)
        else:
            Lock()(self)

    def click_play(self):
        if self.curr_state is Playing():
            Pause()(self)
        else:
            Resume()(self)

    def click_next(self):
        PlayNext()(self)

    def click_previous(self):
        PlayPrev()(self)

    # API
    def start_playback(self):
        ...

    def stop_playback(self):
        ...

    def play(self, sone_name):
        ...

    def lock(self):
        ...

    def get_next_song_name(self):
        return "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(16)
        )

    def get_previous_song_name(self):
        return "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(16)
        )


t = AudioPlayer(Ready())
choices = [t.click_lock, t.click_next, t.click_play, t.click_previous]
while True:
    choice = random.choice(choices)
    print("Before state:", t.curr_state.__class__.__name__)
    try:
        choice()
    except InvalidStateTransition as e:
        print(e)
    print("After state:", t.curr_state.__class__.__name__)
    input()
