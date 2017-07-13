import serial
import time
from serial import SerialException
import config


class Micro:
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.port = config.PORT
        self.ser.baudrate = config.BAUD_RATE
        self.ser.timeout = config.TIMEOUT

    def connect(self):
        try:
            self.ser.open()
        except SerialException:
            print("{} not found".format(config.PORT))

    def disconnect(self):
        self.ser.close()

    def flush(self):
        if self.is_connected():
            self.ser.flushInput()
        else:
            print("Serial not Connected")

    def is_connected(self):
        return self.ser.isOpen()

    def ping(self):
        for i in range(0, 3):
            self.flush()
            self.send(config.PING)
            inp = self.read()
            if inp == 'p':
                return True
            print("Failed got: {}".format(inp))
        return False


    def send(self, message):
        if self.is_connected():
            print("sending: {}".format(message))
            self.ser.write(message.encode())
        else:
            print("Serial not Connected")

    def read(self):
        if self.is_connected():
            return self.ser.readline().decode().strip()
        else:
            print("Serial not Connected")
            return ""

    def check_version(self):
        pass

    def set_ir_mode(self, mode):
        if mode:
            self.send(config.SET_MODE_C10)
        else:
            self.send(config.SET_MODE_C10)

    def set_ir_code(self, code):
        if code:
            self.send('C16_MODE')
        else:
            self.send('C10_MODE')

    def ir_transmit(self):
        self.send(config.TRANSMIT)

    def ir_receive_once(self):
        self.send(config.RECIEVE)
        time.sleep(0.2)
        return self.read() == '1'

    def ir_receive_repeat(self, code, mode):
        pass

    def button_check(self):
        self.send(config.GET_BUTTON_PRESS)
        time.sleep(0.2)
        return self.read() == '1'


