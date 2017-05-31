import Adafruit_GPIO as GPIO
import time

status_pin = 5
fail_pin = 6
pass_pin = 13

up_pin = 17
down_pin = 18
back_pin = 27
select_pin = 22

class LED:
    def __init__(self, pin):
        self.pin = pin
        self.isOn = False
        gpio.setup(self.pin, GPIO.OUT)
        gpio.output(self.pin,GPIO.LOW)

    def turnOn(self):
        self.isOn = True
        gpio.output(self.pin,GPIO.HIGH)

    def turnOff(self):
        self.isOn = False
        gpio.output(self.pin,GPIO.LOW)

    def flash(self, duration):
        self.turnOn()
        time.sleep(duration)
        self.turnOff()
    
class Button:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        gpio.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def isPressed(self):
        return not gpio.input(self.pin)

    def getName(self):
        return self.name
    
gpio = GPIO.get_platform_gpio()

#gpio.setup(status_led,GPIO.OUT)
#gpio.setup(fail_led,GPIO.OUT)
#gpio.setup(pass_led,GPIO.OUT)

status_led = LED(status_pin)
fail_led = LED(fail_pin)
pass_led = LED(pass_pin)

up_button = Button("up",up_pin)
down_button = Button("down", down_pin)
back_button = Button("back", back_pin)
select_button = Button("select", select_pin)

while not back_button.isPressed():
    if up_button.isPressed():
        status_led.flash(0.3)
    if down_button.isPressed():
        fail_led.flash(0.3)
    if select_button.isPressed():
        pass_led.flash(0.3)
    time.sleep(0.1)









    









