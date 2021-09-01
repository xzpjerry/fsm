from fsm import BaseFSM, BaseState, BaseTransition, InvalidStateTransition
import random
import string

class Ready(BaseState):
    def setup(self, with_fsm: "AudioPlayer"):
        print("Player is ready")

    def teardown(self):
        print("Player is about to end being ready")


class Paused(BaseState):
    def setup(self, with_fsm: "AudioPlayer"):
        print("Player is about to pause")
        with_fsm.stop_playback()

    def teardown(self):
        print("Player is about to end pause")


class Locked(BaseState):
    def setup(self, with_fsm: "AudioPlayer"):
        print("Player is about to lock")
        with_fsm.lock()

    def teardown(self):
        print("Player is about to end being locked")


class Playing(BaseState):
    def setup(self, with_fsm: "AudioPlayer"):
        print("Player is about to play songs")

    def teardown(self):
        print("Player is about to end playing")


class Lock(BaseTransition):
    from_state = [Ready(), Playing(), Paused()]
    to_state = Locked()

    @staticmethod
    def transition_action(fsm: "AudioPlayer"):
        print("Transiting to Locked")


class Unlock(BaseTransition):
    from_state = [Locked()]
    to_state = Ready()

    @staticmethod
    def transition_action(fsm: "AudioPlayer"):
        print("Transiting to Ready")


class Resume(BaseTransition):
    from_state = [Paused(), Ready()]
    to_state = Playing()

    @staticmethod
    def transition_action(fsm: "AudioPlayer"):
        print("Transiting to Playing")
        fsm.start_playback()


class Pause(BaseTransition):
    from_state = [Playing()]
    to_state = Paused()

    @staticmethod
    def transition_action(fsm: "AudioPlayer"):
        print("Transiting to Paused")


class PlayNext(BaseTransition):
    from_state = [Paused(), Ready(), Playing()]
    to_state = Playing()

    @staticmethod
    def transition_action(fsm: "AudioPlayer"):
        print("Transiting to Playing")
        next_song = fsm.get_next_song_name()
        print("About to play", next_song)
        fsm.play(next_song)


class PlayPrev(BaseTransition):
    from_state = [Paused(), Ready(), Playing()]
    to_state = Playing()

    @staticmethod
    def transition_action(fsm: "AudioPlayer"):
        print("Transiting to Playing")
        prev_song = fsm.get_previous_song_name()
        print("About to play", prev_song)
        fsm.play(prev_song)


class AudioPlayer(BaseFSM):
    # UI Delegate methods
    def click_lock(self):
        try:
            Lock()(self)
        except InvalidStateTransition:
            Unlock()(self)

    def click_play(self):
        try:
            Resume()(self)
        except InvalidStateTransition:
            Pause()(self)

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

i = 0
choices = [t.click_lock, t.click_next, t.click_play, t.click_previous]
while True:
    choice = random.choice(choices)
    print("Before state:", t.curr_state.__class__.__name__)
    try:
        choice()
    except Exception as e:
        print(e)
    print("After state:", t.curr_state.__class__.__name__)
    input()
