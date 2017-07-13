import config
import time


class Beacon:
    def __init__(self, mode, micro):
        self.micro = micro
        self.mode = mode
        self.external = True
        self.type = config.TYPE_RX
        self.code = 0
        self.code_alpha = '0'
        self.split = False
        self.lap = False
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

    def get_codes_done_string(self):
        output = ''
        for e in self.codes_done:
            if e == 1:
                output += 'X'
            else:
                output += '_'
            #output += str(e)
        return output

    def get_mode_text(self):
        return config.MODE_TEXT[self.mode]

    def get_type_text(self):
        return config.TYPE_TEXT[self.type]

    def get_external_text(self):
        if self.external:
            return 'EXT'
        else:
            return 'INT'


class ExternalRxBeacon(Beacon):
    def __init__(self, mode, micro):
        Beacon.__init__(self, mode, micro)
        self.lap = False
        self.led = False
        self.codes_passed = [0] * 32
        self.current = 0
        self.voltage = 0


class InternalRxBeacon(Beacon):
    def __init__(self, mode, micro):
        Beacon.__init__(self, mode, micro)
        self.external = False
        self.stop = False
        self.lap = True

    def start_receiving(self):
        self.micro.flush()
        self.stop = False
        self.micro.send(config.RECEIVE_REPEAT)

    def stop_receiving(self):
        self.micro.send(config.STOP)

    def read_code(self):
        input_string = self.micro.read()
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
    def __init__(self, mode, micro):
        Beacon.__init__(self, mode, micro)
