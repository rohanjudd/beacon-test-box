import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
        
font_small  = ImageFont.truetype('./Fonts/pixelade.ttf', 13)
font_medium = ImageFont.truetype('./Fonts/madness.ttf', 32)
font_large  = ImageFont.truetype('./Fonts/madness.ttf', 64)
font_a  = ImageFont.truetype('./Fonts/rainyhearts.ttf', 16)
font_b  = ImageFont.truetype('./Fonts/mono.ttf', 10)
font_c  = ImageFont.truetype('./Fonts/madness.ttf', 16)

WIDTH = 128
HEIGHT = 64

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
        
        self.terminalScreen = TerminalScreen(self.NUM_LINES, font_small)
        self.menuScreen = MenuScreen(5, self.draw)
        self.disp.display()

    def splash(self):
        self.displayPPM('./Images/cosworth.ppm')
        for t in range(2):
            for x in range(255,0,-1):
                self.disp.set_contrast(x)
                time.sleep(0.002)
            for x in range(255):
                self.disp.set_contrast(x)
                time.sleep(0.002)

    def displayPPM(self, ppm):
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

    def widthCheck(self, font, text):
        return font.getsize(text)[0] <= self.width

    def displayTerminal(self):
        self.clear()
        x = 0
        for l in self.terminalScreen.getLines():
            self.drawText(l, font_small, self.X_INDENT, x*self.LINE_SPACING + self.Y_INDENT)
            x+=1
        self.refresh()
        
    def startTerminal(self):
        self.terminalScreen.clear()
        self.displayTerminal()
            
    def write(self, text):
        self.terminalScreen.write(text)
        self.displayTerminal()

    def writeln(self, text):
        self.terminalScreen.newLine(text)
        self.displayTerminal()
        
    def drawText(self, text, font, x, y):
        self.draw.text((x, y),text , font=font, fill=255)

    def drawInvertedText(self, text, font, x, y):
        self.draw.text((x, y),text , font=font, fill=0)

    def displayTitle(self, title):
        self.drawText(title,INDENT,0)
        self.draw.line((0, 13, WIDTH, 13), fill=255)

    def displayMenu(self, menu):
        self.clear()
        self.menuScreen.display(menu)
        self.refresh()

    def displayNotification(self, text):
        self.clear()
        self.drawText(text, font_b, 3, 26)
        self.refresh()
        time.sleep(1)

    def displayRx(self, code, lap, codes_done):
        self.clear()
        tup = self.getLetterandSplit(code)
        letter = tup[0]
        split = tup[1]
        self.drawText(letter, font_large, 0, -4)
        if split:
            self.drawText("SPLIT", font_medium, 40, -4)
        if lap:
            self.drawText("LAP", font_medium, 40, 16)
        self.drawText("0123456789ABCDEF", font_c, 2, 46)
        self.drawText("{0:b}".format(codes_done), font_c, 2, 54)
        self.refresh()


    def getLetterandSplit(self, code):
        letter = ""
        split = False
        if code > 15:
            split = True
            code = code - 16
        letter = "%0.1X" % code
        return (letter, split)
            
        
    

        
class MenuScreen():
    def __init__(self, num_lines, draw):
        self.num_lines = num_lines
        self.draw = draw
        self.line_spacing = 12
        self.y_indent = -2
        self.x_indent = 2

    def drawText(self, text, font, x, y, invert=False):
        if invert:
            self.draw.text((x, y),text , font=font, fill=0)
        else:
            self.draw.text((x, y),text , font=font, fill=255)     

    def getLinePos(self, i):
        return i * self.line_spacing + self.y_indent

    def display(self, menu):
        pos = menu.getVisiblePos()
        lines = menu.getVisibleLines()
        i = 0
        for l in lines:
            if i == pos:
                self.draw.rectangle((0, self.getLinePos(pos) + 1, WIDTH, self.getLinePos(pos) + 1 + self.line_spacing), outline=0, fill=255)
                self.drawText(l, font_b, self.x_indent, self.getLinePos(i) +1, invert=True)
            else:
                self.drawText(l, font_b, self.x_indent, self.getLinePos(i) +1)
            i+=1

class TerminalScreen:
    def __init__(self, num_lines, font):
        self.num_lines = num_lines
        self.font = font
        self.lines = []
        
    def clear(self):
        self.lines = []

    def isFull(self):
        return len(self.lines) >= self.num_lines
    
    def newLine(self, text):
        while self.isFull():
            del self.lines[0]
        for i in range(len(text),0,-1):
            if self.font.getsize(text[:i])[0] < WIDTH:
                self.lines.append(text[:i])
                break
        if i < len(text):
            self.newLine(text[i:])

    def removeLast(self):
        if len(self.lines) > 0:
            del self.lines[-1]

    def write(self, text):
        if len(self.lines) > 0:
            last = self.lines[-1]
            self.removeLast()
            self.newLine(last + text)
        else:
            self.newLine(text)
        
    def getLines(self):
        return self.lines

        


