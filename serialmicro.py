import serial
from serial import SerialException

PORT = '/dev/ttyUSB1'
BAUDRATE = 115200
TIMEOUT = 1

class SerialMicro:
    def __init__(self):
        self.ser = serial.Serial()
        self.ser.port = PORT
        self.ser.baudrate = BAUDRATE
        self.ser.timeout = TIMEOUT

    def connect(self):
        try:
            self.ser.open()
        except SerialException:
            print("{} not found".format(PORT))
        

    def disconnect(self):
        self.ser.close()

    def flush(self):
        if self.isConnected():
            self.ser.flushInput()
        else:
            print("Serial not Connected")

    def isConnected(self):
        return self.ser.isOpen()
        
    def send(self, message):
        if self.isConnected():
            self.ser.write(message.encode())
        else:
            print("Serial not Connected")

    def read(self):
        if self.isConnected():
            return self.ser.readline().decode().strip()
        else:
            print("Serial not Connected")
            return ""

    def checkVersion(self):
        pass

