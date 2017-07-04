import constants
import time

class Beacon:
    def __init__(self, mode):
        self.mode = mode
        self.code = 0
        self.code_alpha = '0'
        self.split = False
        self.codes_done = [0] * 32


    def new_code(self, code):
        if 0 <= code <= 31:
            self.code = code
            self.set_alpha_split()
            self.codes_done[code] = 1

    def set_alpha_split(self):
        self.split = False
        val = self.code
        if val > 15:
            self.split = True
            val = self.code - 16
        self.code_alpha = "%0.1X" % val


class ExternalRxBeacon(Beacon):
    def __init__(self, mode):
        Beacon.__init__(self, mode)
        self.lap = False
        self.led = False
        self.codes_passed = [0] * 32
        self.current = 0
        self.voltage = 0


class InternalRxBeacon(Beacon):
    def __init__(self, mode):
        Beacon.__init__(self, mode)
        self.stop = False

    def start_receiving(self, micro):
        self.stop = False
        micro.send(constants.RECEIVE_REPEAT)

    def read_code(self, micro):
        input_string = micro.read()
        if input_string == 'x':
            self.stop = True
        print(input_string)
        try:
            i = int(input_string)
            if 0 > i > 31:
                raise ValueError
        except ValueError:
            print('Not Valid Code')
            i = 0
        self.new_code(i)




class InternalTxBeacon(Beacon):
    def __init__(self, mode):
        Beacon.__init__(self, mode)


