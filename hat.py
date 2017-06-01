import Adafruit_GPIO as GPIO
import time
from oled import Oled


class Hat:
    STATUS_PIN = 5
    FAIL_PIN = 6
    PASS_PIN = 13
    UP_PIN = 17
    DOWN_PIN = 18
    BACK_PIN = 27
    SELECT_PIN = 22

    NONE = 0
    UP = 1
    DOWN = 2
    BACK = 3
    SELECT = 4

    DEFAULT_FLASH = 0.2

    def __init__(self):
        self.oled = Oled()
        self.gpio = GPIO.get_platform_gpio()

        self.gpio.setup(self.STATUS_PIN, GPIO.OUT)
        self.gpio.setup(self.FAIL_PIN, GPIO.OUT)
        self.gpio.setup(self.PASS_PIN, GPIO.OUT)

        self.gpio.setup(self.UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.gpio.setup(self.DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.gpio.setup(self.BACK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.gpio.setup(self.SELECT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.lastButtonState = self.NONE

    def set_status_led(self, state):
        self.gpio.output(self.STATUS_PIN, state)

    def set_fail_led(self, state):
        self.gpio.output(self.FAIL_PIN, state)

    def set_pass_led(self, state):
        self.gpio.output(self.PASS_PIN, state)

    def get_up_state(self):
        return not self.gpio.input(self.UP_PIN)

    def get_down_state(self):
        return not self.gpio.input(self.DOWN_PIN)

    def get_back_state(self):
        return not self.gpio.input(self.BACK_PIN)

    def get_select_state(self):
        return not self.gpio.input(self.SELECT_PIN)

    def get_button_state(self):
        state = self.NONE
        if self.get_up_state():
            state = self.UP
        elif self.get_down_state():
            state = self.DOWN
        elif self.get_back_state():
            state = self.BACK
        elif self.get_select_state():
            state = self.SELECT
        if state == self.lastButtonState:
            self.lastButtonState = state
            return self.NONE
        self.lastButtonState = state
        return state

    def hat_test(self):
        self.set_leds(True)
        time.sleep(0.5)
        self.set_leds(False)

    def set_leds(self, state):
        self.set_status_led(state)
        self.set_fail_led(state)
        self.set_pass_led(state)

    def flash_status(self):
        self.set_status_led(True)
        time.sleep(0.2)
        self.set_status_led(False)

    def flash_fail(self):
        self.set_fail_led(True)
        time.sleep(0.2)
        self.set_fail_led(False)

    def flash_pass(self):
        self.set_pass_led(True)
        time.sleep(0.2)
        self.set_pass_led(False)

    def shutdown(self):
        self.oled.start_terminal()
        self.oled.display_notification("Shutting Down")
        time.sleep(1)
        self.oled.blank()
        self.set_leds(False)

    def sleep(self):
        self.oled.start_terminal()
        self.oled.display_notification("Going to Sleep")
        time.sleep(1)
        self.oled.blank()
