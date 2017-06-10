import serial
import time
from serial import SerialException

PORT = '/dev/ttyUSB1'
BAUD_RATE = 115200
TIMEOUT = 1


class SerialMicro:
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.port = PORT
        self.ser.baud_rate = BAUD_RATE
        self.ser.timeout = TIMEOUT

    def connect(self):
        try:
            self.ser.open()
        except SerialException:
            print("{} not found".format(PORT))

    def disconnect(self):
        self.ser.close()

    def flush(self):
        if self.is_connected():
            self.ser.flushInput()
        else:
            print("Serial not Connected")

    def is_connected(self):
        return self.ser.isOpen()

    def send(self, message):
        if self.is_connected():
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

    def ir_transmit(self, code, mode, repeat):
        message = "TRANSMIT {} {} {}".format(code,mode,repeat)
        print(message)
        self.send(message)

    def ir_receive_once(self, code, mode):
        message = "TRANSMIT {} {} {}".format(code, mode)
        self.send(message)
        time.sleep(0.2)
        return self.read() == "True"

    def ir_receive_repeat(self, code, mode):
        pass

    def button_check(self):
        message = "BUTTON"
        self.send(message)
        time.sleep(0.2)
        return self.read() == "True"


