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

    def setStatusLED(self, state):
        self.gpio.output(self.STATUS_PIN, state)

    def setFailLED(self, state):
        self.gpio.output(self.FAIL_PIN, state)

    def setPassLED(self, state):
        self.gpio.output(self.PASS_PIN, state)

    def getUPstate(self):
        return not self.gpio.input(self.UP_PIN)

    def getDOWNstate(self):
        return not self.gpio.input(self.DOWN_PIN)

    def getBACKstate(self):
        return not self.gpio.input(self.BACK_PIN)

    def getSELECTstate(self):
        return not self.gpio.input(self.SELECT_PIN)

    def getButtonState(self):
        state = self.NONE
        if self.getUPstate():
            state = self.UP
        elif self.getDOWNstate():
            state = self.DOWN
        elif self.getBACKstate():
            state = self.BACK
        elif self.getSELECTstate():
            state = self.SELECT
        if state == self.lastButtonState:
            self.lastButtonState = state
            return self.NONE
        self.lastButtonState = state
        return state

    def testHat(self):
        self.setLEDs(True)
        time.sleep(0.5)
        self.setLEDs(False)

    def setLEDs(self, state):
        self.setStatusLED(state)
        self.setFailLED(state)
        self.setPassLED(state)
        
    def flashStatus(self):
        self.setStatusLED(True)
        time.sleep(0.2)
        self.setStatusLED(False)

    def flashFail(self):
        self.setFailLED(True)
        time.sleep(0.2)
        self.setFailLED(False)

    def flashPass(self):
        self.setPassLED(True)
        time.sleep(0.2)
        self.setPassLED(False)

    def splash(self):
        self.oled.splash()

    def clear(self):
        self.oled.clear()
            
    def refresh(self):
        self.oled.refresh()

    def widthCheck(self, text):
        return self.oled.widthCheck(text)

    def displayTerminal(self):
        self.oled.displayTerminal()
        
    def newTerminal(self):
        self.oled.startTerminal()
            
    def write(self, text):
        self.oled.write(text)

    def writeln(self, text):
        self.oled.writeln(text)

    def displayMenu(self, menu):
        self.oled.displayMenu(menu)

    def displayNotification(self, text):
        self.oled.displayNotification(text)

    def displayRx(self, code, split, lap):
        self.oled.displayRx(code, lap)

    def shutdown(self):
        self.oled.startTerminal()
        self.oled.displayNotification("Shutting Down")
        time.sleep(1)
        self.oled.blank()
        self.setLEDs(False)

    def sleep(self):
        self.oled.startTerminal()
        self.oled.displayNotification("Going to Sleep")
        time.sleep(1)
        self.oled.blank()
    

        
        

        








