import serial
import time
import struct


class FlowMeter:
    def __init__(self, port):
        self.ser = serial.Serial(
            port=port,
            baudrate=38400,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            )
    def float_to_hex(self, f):
        return hex(struct.unpack('<I', struct.pack('<f', f))[0])

    def hex_to_float(self, h):
        return struct.unpack('!f', bytes.fromhex(h))[0]

    # set the flow rate in L/min, rate is a float
    def setFlowRate(self, rate):
        rateInHex = self.float_to_hex(rate)[2:]
        req = ':0880012143' + str(rateInHex).upper() + '\r\n'
        req_in_bytes = str.encode(req)
        self.ser.write(req_in_bytes)

    def readFlowRate(self):
        req_in_bytes = str.encode(":06800421402140\r\n")
        self.ser.write(req_in_bytes)
        res = self.ser.readline().decode("utf-8").upper()
        t = self.hex_to_float(res[len(res)-8-2: len(res)-2])
        return t

    def checkCommunication(self):
        req_in_bytes = str.encode(":06800100600139\r\n")
        try:
            self.ser.write(req_in_bytes)
            res = self.ser.readline()
            if(res == str.encode(":0480000005\r\n")):
                return True
            else:
                return False
        except SerialException:
            return False
            

