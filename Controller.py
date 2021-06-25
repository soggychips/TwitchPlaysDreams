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

    def button(self, button, seconds=0.0):
        with self.lock:
            self.gamepad.press_button(button)
            self.gamepad.update()
            sleep(Controller.one_frame if seconds == 0.0 else seconds)
            self.gamepad.release_button(button)
            self.gamepad.update()
            sleep(Controller.two_frames)

    def dpad(self, direction, seconds=0.0):
        """Emulates tapping of a dpad direction"""
        with self.lock:
            self.gamepad.directional_pad(direction)
            self.gamepad.update()
            sleep(Controller.one_frame if seconds == 0.0 else seconds)
            self.gamepad.directional_pad(0x8)  # dpad None
            self.gamepad.update()
            sleep(Controller.two_frames)

    def stick(self, stick, x_value_float=0.0, y_value_float=0.0, seconds=0.0):
        stick = (
            self.gamepad.left_joystick_float
            if stick == "l"
            else self.gamepad.right_joystick_float
            if stick == "r"
            else None
        )
        if stick is None:
            raise Exception()
        with self.lock:
            stick(x_value_float=x_value_float, y_value_float=y_value_float)
            self.gamepad.update()
            sleep(Controller.one_frame if seconds == 0.0 else seconds)
            stick(x_value_float=0.0, y_value_float=0.0)
            self.gamepad.update()
            sleep(Controller.two_frames)

    def sticks(self, left_amounts=[0.0, 0.0], right_amounts=[0.0, 0.0], seconds=0.0):
        zeros = [0.0, 0.0]
        with self.lock:
            self.gamepad.left_joystick_float(*left_amounts)
            self.gamepad.right_joystick_float(*right_amounts)
            self.gamepad.update()
            sleep(Controller.one_frame if seconds == 0.0 else seconds)
            self.gamepad.left_joystick_float(*zeros)
            self.gamepad.right_joystick_float(*zeros)
            self.gamepad.update()
            sleep(Controller.two_frames)

    def trigger(self, which_trigger, amount=1.0, seconds=0.0):
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
            self.gamepad.update()
            sleep(Controller.one_frame if seconds == 0.0 else seconds)
            trigger_pull(value_float=0.0)
            self.gamepad.update()
            sleep(Controller.two_frames)
