from threading import Lock
from time import sleep
import vgamepad as vg


class Controller:

    one_frame = 1 / 30
    two_frames = 2 / 30

    def __init__(self):
        self.gamepad = vg.VDS4Gamepad()
        self.lock = Lock()

    def tap(self, button):
        """Emulates button tap"""
        with self.lock:
            self.gamepad.press_button(button)
            self.gamepad.update()
            sleep(Controller.one_frame)
            self.gamepad.release_button(button)
            self.gamepad.update()
            sleep(Controller.two_frames)

    def hold(self, button, seconds=1):
        """Emulates button hold for amount given in seconds"""
        with self.lock:
            self.gamepad.press_button(button)
            self.gamepad.update()
            sleep(seconds)
            self.gamepad.release_button(button)
            self.gamepad.update()
            sleep(Controller.two_frames)

    def dpad(self, direction):
        """Emulates tapping of a dpad direction"""
        with self.lock:
            self.gamepad.directional_pad(direction)
            self.gamepad.update()
            sleep(Controller.one_frame)
            self.gamepad.directional_pad(0x8)  # dpad None
            self.gamepad.update()
            sleep(Controller.two_frames)

    def trigger(self, which_trigger, amount=1.0):
        """Emulates a trigger pull (and release) for given amount"""
        trigger_pull = (
            self.gamepad.right_trigger_float
            if which_trigger == "r2"
            else self.gamepad.left_trigger_float
            if which_trigger == "l2"
            else None
        )
        if trigger_pull is None:
            raise Exception()
        with self.lock:
            trigger_pull(value_float=amount)
            sleep(Controller.one_frame)
            trigger_pull(value_float=0.0)
            sleep(Controller.two_frames)


if __name__ == "__main__":
    from const import buttons

    controller = Controller()
    sleep(Controller.two_frames)

    controller.left()
    controller.right()
    controller.left()
    controller.right()
    controller.tap(buttons["circle"])
    controller.tap(buttons["square"])
    controller.tap(buttons["x"])
