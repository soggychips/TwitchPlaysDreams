from threading import Lock
from time import sleep
import vgamepad as vg


class Controller:

    one_frame = 1 / 30
    two_frames = 2 / 30

    def __init__(self):
        self.gamepad = vg.VDS4Gamepad()
        self.lock = Lock()

    def release_all(self):
        self.gamepad.reset()
        self.gamepad.update()

    def button(self, name, _):
        self.gamepad.press_button(name)

    def dpad(self, name, _):
        self.gamepad.directional_pad(name)

    def stick(self, name, amount):
        if name == "right":
            self.gamepad.right_joystick_float(*amount)
        else:
            self.gamepad.left_joystick_float(*amount)

    def trigger(self, name, amount):
        if name == "r2":
            self.gamepad.right_trigger_float(amount)
        else:
            self.gamepad.left_trigger_float(amount)

    def single(self, func, **kwargs):
        length = kwargs.get("length", Controller.one_frame)
        with self.lock:
            func(kwargs.get("name"), kwargs.get("amount", 1))
            self.gamepad.update()
            sleep(length)
            self.release_all()
            self.gamepad.update()
            sleep(Controller.two_frames)

    def combination(self, funcs, args):
        with self.lock:
            length = max(arg.get("length", Controller.one_frame) for arg in args)
            for func, kwargs in zip(funcs, args):
                func(kwargs.get("name"), kwargs.get("amount"))
            self.gamepad.update()
            sleep(length)
            self.release_all()
            self.gamepad.update()
            sleep(Controller.two_frames)
