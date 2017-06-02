import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

font_10 = ImageFont.truetype('./Fonts/mono.ttf', 10)
font_13 = ImageFont.truetype('./Fonts/pixel.ttf', 13)
font_16 = ImageFont.truetype('./Fonts/madness.ttf', 16)
font_32 = ImageFont.truetype('./Fonts/madness.ttf', 32)
font_64 = ImageFont.truetype('./Fonts/madness.ttf', 64)


WIDTH = 128
HEIGHT = 64


def get_letter_and_split(code):
    split = False
    if code > 15:
        split = True
        code = code - 16
    letter = "%0.1X" % code
    return letter, split


def width_check(font, text):
    return font.getsize(text)[0] <= WIDTH


class Oled:
    LINE_SPACING = 11
    X_INDENT = 2
    Y_INDENT = -2
    NUM_LINES = 6

    def __init__(self):
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=24, dc=23, spi=SPI.SpiDev(0, 0, max_speed_hz=8000000))
        self.disp.begin()

        self.image = Image.new('1', (WIDTH, HEIGHT))
        self.draw = ImageDraw.Draw(self.image)

        self.terminal_screen = TerminalScreen(self.NUM_LINES, font_13)
        self.menu_Screen = MenuScreen(5, self.draw)
        self.disp.display()

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
        self.draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

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
            self.draw_text(l, font_13, self.X_INDENT, x * self.LINE_SPACING + self.Y_INDENT)
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

    def display_menu(self, menu):
        self.clear()
        self.menu_Screen.display(menu)
        self.refresh()

    def display_notification(self, text):
        self.clear()
        self.draw_text(text, font_10, 3, 26)
        self.refresh()
        time.sleep(1)

    def display_rx(self, code, lap, codes_done):
        self.clear()
        tup = get_letter_and_split(code)
        letter = tup[0]
        split = tup[1]
        self.draw_text(letter, font_64, 0, -4)
        if split:
            self.draw_text("SPLIT", font_32, 40, -4)
        if lap:
            self.draw_text("LAP", font_32, 40, 16)
        self.draw_text("0123456789ABCDEF", font_16, 2, 46)
        self.draw_text("{0:b}".format(codes_done), font_16, 2, 54)
        self.refresh()


class MenuScreen:
    def __init__(self, num_lines, draw):
        self.num_lines = num_lines
        self.draw = draw
        self.line_spacing = 12
        self.y_indent = -2
        self.x_indent = 2

    def draw_text(self, text, font, x, y, invert=False):
        if invert:
            self.draw.text((x, y), text, font=font, fill=0)
        else:
            self.draw.text((x, y), text, font=font, fill=255)

    def get_line_pos(self, i):
        return i * self.line_spacing + self.y_indent

    def display(self, menu):
        pos = menu.get_visible_pos()
        lines = menu.get_visible_lines()
        i = 0
        for l in lines:
            if i == pos:
                self.draw.rectangle((0, self.get_line_pos(pos) + 1, WIDTH, self.get_line_pos(pos) + 1 +
                                     self.line_spacing), outline=0, fill=255)
                self.draw_text(l, font_10, self.x_indent, self.get_line_pos(i) + 1, invert=True)
            else:
                self.draw_text(l, font_10, self.x_indent, self.get_line_pos(i) + 1)
            i += 1


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
            if self.font.getsize(text[:i])[0] < WIDTH:
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
