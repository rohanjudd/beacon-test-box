import time
import constants
import beacon
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

font_10 = ImageFont.truetype('./Fonts/mono.ttf', 10)
font_13 = ImageFont.truetype('./Fonts/pixel.ttf', 13)
font_16 = ImageFont.truetype('./Fonts/madness.ttf', 16)
font_32 = ImageFont.truetype('./Fonts/madness.ttf', 32)
font_64 = ImageFont.truetype('./Fonts/madness.ttf', 64)

bmp = Image.open("./Images/x.png").convert('1')
bmp2 = Image.open("./Images/grid.png").convert('1')
bmp3 = Image.open("./Images/gridinv.ppm").convert('1')


def get_letter_and_split(code):
    split = False
    if code > 15:
        split = True
        code = code - 16
    letter = "%0.1X" % code
    return letter, split


def width_check(font, text):
    return font.getsize(text)[0] <= constants.WIDTH


def get_line_pos(i):
    return i * constants.MENU_LINE_SPACING + constants.MENU_Y_INDENT


class Hat:
    def __init__(self):

        self.gpio = GPIO.get_platform_gpio()
        self.gpio.setup(constants.STATUS_PIN, GPIO.OUT)
        self.gpio.setup(constants.RED_PIN, GPIO.OUT)
        self.gpio.setup(constants.GREEN_PIN, GPIO.OUT)
        self.gpio.setup(constants.UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.gpio.setup(constants.DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.gpio.setup(constants.BACK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.gpio.setup(constants.SELECT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.lastButtonState = constants.NONE
        
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=24, dc=23, spi=SPI.SpiDev(0, 0, max_speed_hz=8000000))
        self.disp.begin()
        self.image = Image.new('1', (constants.WIDTH, constants.HEIGHT))
        self.draw = ImageDraw.Draw(self.image)

        self.terminal_screen = TerminalScreen(constants.TERMINAL_NUM_LINES, font_13)
        self.disp.display()

    def set_led_states(self, status=False, red=False, green=False):
        self.gpio.output(constants.STATUS_PIN, status)
        self.gpio.output(constants.RED_PIN, red)
        self.gpio.output(constants.GREEN_PIN, green)

    def get_up_state(self):
        return not self.gpio.input(constants.UP_PIN)

    def get_down_state(self):
        return not self.gpio.input(constants.DOWN_PIN)

    def get_back_state(self):
        return not self.gpio.input(constants.BACK_PIN)

    def get_select_state(self):
        return not self.gpio.input(constants.SELECT_PIN)

    def get_button_state(self):
        state = constants.NONE
        if self.get_up_state():
            state = constants.UP
        elif self.get_down_state():
            state = constants.DOWN
        elif self.get_back_state():
            state = constants.BACK
        elif self.get_select_state():
            state = constants.SELECT
        if state == self.lastButtonState:
            self.lastButtonState = state
            return constants.NONE
        self.lastButtonState = state
        return state

    def hat_test(self):
        self.set_led_states(status=True, red=True, green=True)
        time.sleep(0.5)
        self.set_led_states(status=False, red=False, green=False)

    def shutdown(self):
        self.display_notification("Shutting Down")
        time.sleep(1)
        self.blank()
        self.set_led_states(status=False, red=False, green=False)

    def sleep(self):
        self.display_notification("Going to Sleep")
        time.sleep(1)
        self.blank()

    def splash(self):
        self.display_ppm_image('./Images/cosworth.ppm')
        for t in range(2):
            for x in range(255, 0, -1):
                self.disp.set_contrast(x)
                time.sleep(0.002)
            for x in range(255):
                self.disp.set_contrast(x)
                time.sleep(0.002)

    def display_ppm_image(self, ppm):
        self.disp.image(Image.open(ppm).convert('1'))
        self.disp.display()

    def clear(self):
        self.draw.rectangle((0, 0, constants.WIDTH, constants.HEIGHT), outline=0, fill=0)

    def refresh(self):
        self.disp.image(self.image)
        self.disp.display()

    def blank(self):
        self.clear()
        self.refresh()

    def display_terminal(self):
        self.clear()
        x = 0
        for l in self.terminal_screen.get_lines():
            self.draw_text(l, font_13, constants.TERMINAL_X_INDENT, x * constants.TERMINAL_LINE_SPACING +
                           constants.TERMINAL_Y_INDENT)
            x += 1
        self.refresh()

    def start_terminal(self):
        self.terminal_screen.clear()
        self.display_terminal()

    def write(self, text):
        self.terminal_screen.write(text)
        self.display_terminal()

    def write_line(self, text):
        self.terminal_screen.new_line(text)
        self.display_terminal()

    def draw_text(self, text, font, x, y, invert=False):
        if not invert:
            self.draw.text((x, y), text, font=font, fill=255)
        else:
            self.draw.text((x, y), text, font=font, fill=0)

    def display_notification(self, text):
        self.clear()
        self.draw_text(text, font_10, 3, 26)
        self.refresh()
        time.sleep(1)

    def display_circle(self, start, end):
        self.clear()
        self.draw.arc((10, 10, 50, 50), start, end, 1,)
        self.refresh()
        time.sleep(0.1)

    def display_bitmap(self, num):
        self.clear()
        if num == 0:
            self.draw.bitmap((0, 0), bmp2)
        else:
            self.image.paste(bmp3, (0, 0))
        self.refresh()
        time.sleep(0.5)

    def display_rx(self, beac):
        self.clear()
        self.image.paste(bmp3, (0, 0))
        self.draw_text(beac.code_alpha, font_64, 0, -4)
        if beac.split:
            self.draw_text("SPLIT", font_32, 40, -4)
        if beac.lap:
            self.draw_text("LAP", font_32, 40, 16)
        self.draw_codes_done(beac)
        self.refresh()

    def draw_codes_done(self, beac):
        codes_done = beac.codes_done
        y = 56
        x = 0
        for e in codes_done:
            if e == 1:
                if x == 128:
                    y += 4
                    x = 0
                self.draw.rectangle((x, y, x+8, y+4), outline=1, fill=255)
            x += 8

    def display_menu(self, menu):
        self.clear()
        pos = menu.get_screen_pos()
        lines = menu.get_screen_lines()
        i = 0
        for l in lines:
            if i == pos:
                self.draw.rectangle((0, get_line_pos(pos) + 1, constants.WIDTH, get_line_pos(pos) + 1 +
                                     constants.MENU_LINE_SPACING), outline=0, fill=255)
                self.draw_text(l, font_10, constants.MENU_X_INDENT, get_line_pos(i) + 1, invert=True)
            else:
                self.draw_text(l, font_10, constants.MENU_X_INDENT, get_line_pos(i) + 1)
            i += 1
        self.refresh()


class TerminalScreen:
    def __init__(self, num_lines, font):
        self.num_lines = num_lines
        self.font = font
        self.lines = []

    def clear(self):
        self.lines = []

    def is_full(self):
        return len(self.lines) >= self.num_lines

    def new_line(self, text):
        while self.is_full():
            del self.lines[0]
        i = 0
        for i in range(len(text), 0, -1):
            if self.font.getsize(text[:i])[0] < constants.WIDTH:
                self.lines.append(text[:i])
                break
        if i < len(text):
            self.new_line(text[i:])

    def remove_last(self):
        if len(self.lines) > 0:
            del self.lines[-1]

    def write(self, text):
        if len(self.lines) > 0:
            last = self.lines[-1]
            self.remove_last()
            self.new_line(last + text)
        else:
            self.new_line(text)

    def get_lines(self):
        return self.lines
