import serial
import time
import struct

# class to manage the flow Bronhorst flow meter
class FlowMeter:
    def __init__(self):
        self.ser = serial.Serial(
            baudrate=38400,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1000
            )
    def setPort(self, port):
        self.ser.port = port

    def floatToHex(self, f):
        return hex(struct.unpack('<I', struct.pack('<f', f))[0])

    def hexToFloat(self, h):
        return struct.unpack('!f', bytes.fromhex(h))[0]

    # set the flow rate in L/min, rate is a float
    def setFlowRate(self, rate):
        rateInHex = self.floatToHex(rate)[2:]
        req = ':0880012143' + str(rateInHex).upper() + '\r\n'
        req_in_bytes1 = str.encode(req)
        if(self.ser.is_open):
            try:
                written_bytes = self.ser.write(req_in_bytes1)
                return written_bytes
            except:
                return None
        else:
            return None
        


    def readFlowRate(self):
        req_in_bytes2 = str.encode(":06800421402140\r\n")
        if(self.ser.is_open):
            try:
                self.ser.write(req_in_bytes2)
                res = self.ser.readline().decode("utf-8").upper()
                t = self.hexToFloat(res[len(res)-8-2: len(res)-2])
                return t
            except:
                return None
        else:
            return None
       
    def checkCommunication(self):
        req_in_bytes = str.encode(":06800100600139\r\n")
        if(self.ser.is_open):
            try:
                self.ser.write(req_in_bytes)
                res = self.ser.readline()
                if(res == str.encode(":0480000005\r\n")):
                    return True
                else:
                    return False
            except SerialException:
                return False
                
            

