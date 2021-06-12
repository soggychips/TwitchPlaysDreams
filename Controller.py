from enum import IntFlag
from time import sleep
import vgamepad as vg


buttons = {
    # "ps": 1 << 0,
    # "touchpad": 1 << 1,
    "square": 1 << 4,
    "x": 1 << 5,
    "circle": 1 << 6,
    "triangle": 1 << 7,
}

dpad_left = 0x6
dpad_right = 0x2


class Controller:
    def __init__(self):
        self.gamepad = vg.VDS4Gamepad()

    def tap(self, button):
        self.gamepad.press_button(button)
        self.gamepad.update()
        sleep(1 / 30)
        self.gamepad.release_button(button)
        self.gamepad.update()
        sleep(0.08)

    def hold(self, button, time=1):
        self.gamepad.press_button(button)
        self.gamepad.update()
        sleep(time)
        self.gamepad.release_button(button)
        self.gamepad.update()
        sleep(1 / 30)

    def tapall(self):
        for v in buttons.values():
            self.gamepad.press_button(v)
            self.gamepad.update()
        sleep(1 / 30)
        for v in buttons.values():
            self.gamepad.release_button(v)
            self.gamepad.update()
        sleep(0.08)

    def left(self):
        self.gamepad.directional_pad(dpad_left)
        self.gamepad.update()
        sleep(1 / 30)
        self.gamepad.reset()
        self.gamepad.update()
        sleep(0.08)

    def right(self):
        self.gamepad.directional_pad(dpad_right)
        self.gamepad.update()
        sleep(1 / 30)
        self.gamepad.reset()
        self.gamepad.update()
        sleep(0.08)


if __name__ == "__main__":
    from random import choice, seed
    from time import sleep

    controller = Controller()
    print("focus window")
    sleep(3)
    seed()

    # for i in range(10):
    #     random_button = choice(list(buttons.keys()))
    #     print(random_button)
    #     controller.tap(buttons[random_button])
    #     sleep(1)
    controller.left()
    controller.right()
    controller.left()
    controller.right()
    controller.tap(buttons["circle"])
    controller.tap(buttons["square"])
    controller.tap(buttons["x"])
