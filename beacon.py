class Beacon:
    def __init__(self):
        self.code = 0
        self.split = False
        self.code_array = [0] * 32

    def new_code(self, code):
        self.code = code
