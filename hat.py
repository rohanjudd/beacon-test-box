import Adafruit_GPIO as GPIO
import time
import hat_constants
from oled import Oled


class Hat:
    def __init__(self):
        self.oled = Oled()
        self.gpio = GPIO.get_platform_gpio()

        self.gpio.setup(hat_constants.STATUS_PIN, GPIO.OUT)
        self.gpio.setup(hat_constants.RED_PIN, GPIO.OUT)
        self.gpio.setup(hat_constants.GREEN_PIN, GPIO.OUT)

        self.gpio.setup(hat_constants.UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.gpio.setup(hat_constants.DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.gpio.setup(hat_constants.BACK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.gpio.setup(hat_constants.SELECT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.lastButtonState = hat_constants.NONE

    def set_led_states(self, status=False, red=False, green=False):
        self.gpio.output(hat_constants.STATUS_PIN, status)
        self.gpio.output(hat_constants.RED_PIN, red)
        self.gpio.output(hat_constants.GREEN_PIN, green)

    def get_up_state(self):
        return not self.gpio.input(hat_constants.UP_PIN)

    def get_down_state(self):
        return not self.gpio.input(hat_constants.DOWN_PIN)

    def get_back_state(self):
        return not self.gpio.input(hat_constants.BACK_PIN)

    def get_select_state(self):
        return not self.gpio.input(hat_constants.SELECT_PIN)

    def get_button_state(self):
        state = hat_constants.NONE
        if self.get_up_state():
            state = hat_constants.UP
        elif self.get_down_state():
            state = hat_constants.DOWN
        elif self.get_back_state():
            state = hat_constants.BACK
        elif self.get_select_state():
            state = hat_constants.SELECT
        if state == self.lastButtonState:
            self.lastButtonState = state
            return hat_constants.NONE
        self.lastButtonState = state
        return state

    def hat_test(self):
        self.set_led_states(status=True, red=True, green=True)
        time.sleep(0.5)
        self.set_led_states(status=False, red=False, green=False)

    def shutdown(self):
        self.oled.display_notification("Shutting Down")
        time.sleep(1)
        self.oled.blank()
        self.set_led_states(status=False, red=False, green=False)

    def sleep(self):
        self.oled.display_notification("Going to Sleep")
        time.sleep(1)
        self.oled.blank()
