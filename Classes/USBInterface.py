import serial
import time
import json
import sys

# class that retrieves data from the pyduino has a custom
# protocol (in the file DAQ.py) that responds to the 
# request 'GET_DATA'

class USBInterface():
    def __init__(self):
        self.is_running = False
        self.data = []

    def setPort(self, port):
        # configure the serial connections (the parameters differs on the device you are connecting to)
        self.ser = serial.Serial(
            port=port,
            baudrate=9600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS,
            timeout=1000
        )

    def getData(self):
        if(self.ser.is_open):
            try:
                # request data from pyduino
                self.ser.write(b'GET_DATA')
                # read data that is sent back from pyduino
                d = self.ser.readline()
                parsedD = json.loads(d)
                return parsedD
            except:
                return None
        else:
            return None
        