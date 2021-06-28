from threading import Lock
from time import sleep
import vgamepad as vg
from const import buttons, dpad_directions, sticks, triggers


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
        self.gamepad.press_button(buttons[name])

    def dpad(self, name, _):
        self.gamepad.directional_pad(dpad_directions[name])

    def stick(self, name, amount):
        if name in ("r", 'right'):
            self.gamepad.right_joystick_float(*amount)
        else:
            self.gamepad.left_joystick_float(*amount)

    def trigger(self, name, amount):
        if name == "r2":
            self.gamepad.right_trigger_float(amount)
        else:
            self.gamepad.left_trigger_float(amount)

    def single(self, func, **kwargs):
        try:
            with self.lock:
                length = float(kwargs.get("length") or Controller.two_frames)
                func(kwargs.get("name"), kwargs.get("amount", 1))
                self.gamepad.update()
                sleep(length)
                self.release_all()
                self.gamepad.update()
                sleep(Controller.two_frames)
        except Exception as e:
            raise Exception("Unexpected data of some kind in {}".format(kwargs), e)

    def combination(self, funcs, args):
        try:
            with self.lock:
                length = float(
                    max(arg.get("length") or Controller.two_frames for arg in args)
                )
                for func, kwargs in zip(funcs, args):
                    func(kwargs.get("name"), kwargs.get("amount", 1))
                self.gamepad.update()
                sleep(length)
                self.release_all()
                self.gamepad.update()
                sleep(Controller.two_frames)
        except Exception as e:
            raise Exception("Unexpected data of some kind in {}".format(args), e)
