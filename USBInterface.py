import serial
import time
import json

class Interface():
    def __init__(self, port):
        # configure the serial connections (the parameters differs on the device you are connecting to)
        self.ser = serial.Serial(
            port=port,
            baudrate=9600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        self.is_running = False
        self.data = []
        self.timeout = 1000

    def getData(self):
        timeoutCount = 0
        # request data from pyduino
        self.ser.write(b'GET_DATA')
        # read data that is sent back from pyduino
        if(self.ser.is_open):
            while(self.ser.inWaiting() == 0):
                if(timeoutCount == 10):
                    return None, "error: timed out getting data from pyduino"
                else:
                    time.sleep(0.001)
                    timeoutCount+=1

            d = self.ser.readline()
            parsedD = json.loads(d)
            return parsedD, None
        else: 
            return None, "error: serial port not open"
