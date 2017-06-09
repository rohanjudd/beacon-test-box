C10 = 0
C16 = 1


class Beacon:
    def __init__(self, mode):
        self.mode = mode
        self.code = 0
        self.split = False
        self.codes_done = [0] * 32

    def new_code(self, code):
        if code > 0 and code < 32:
            self.code = code
            self.codes_done[code] = 1


class ExternalRxBeacon(Beacon):
    def __init__(self, mode):
        Beacon.__init__(mode)
        self.lap = False
        self.led = False
        self.codes_passed = [0] * 32
        self.current = 0
        self.voltage = 0


class InternalRxBeacon(Beacon):
    def __init__(self, mode):
        Beacon.__init__(mode)


class InternalTxBeacon(Beacon):
    def __init__(self, mode):
        Beacon.__init__(mode)


class ExternalTxBeacon(Beacon):
    def __init__(self, mode):
        Beacon.__init__(mode)


