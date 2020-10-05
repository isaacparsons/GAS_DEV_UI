import pyb
from BME280 import BME280
import ujson

bme = BME280()

adcall = pyb.ADCAll(12, 0x70000)
vref = adcall.read_vref()

adc0 = pyb.ADC(pyb.Pin.board.A0) 
adc1 = pyb.ADC(pyb.Pin.board.A1) 
adc2 = pyb.ADC(pyb.Pin.board.A2) 
adc3 = pyb.ADC(pyb.Pin.board.A3) 
adc4 = pyb.ADC(pyb.Pin.board.A4) 
adc5 = pyb.ADC(pyb.Pin.board.A5) 
adc6 = pyb.ADC(pyb.Pin.board.B1) # AIN0 or 6 on pyduino 
adc7 = pyb.ADC(pyb.Pin.board.B0) # AIN1 or 5 on pyduino


usb = pyb.USB_VCP()
myLed = pyb.LED(1)
myLed.on()
pyb.LED(2).on()
pyb.LED(3).on()

def convertToVoltage(adcVal, vref):
    return round((adcVal/4095) * vref, 3)

while(True):
    if(usb.any()):
        req = usb.read()
        if(req == b'GET_DATA'):

            # get temp/ humidity/ pressure readings from the BME280
            data = bme.read_values()

            # get the adc readings
            data.S1 = convertToVoltage(adc0.read(), vref)
            data.S2 = convertToVoltage(adc1.read(), vref)
            data.S3 = convertToVoltage(adc2.read(), vref)
            data.S4 = convertToVoltage(adc3.read(), vref)
            data.S5 = convertToVoltage(adc4.read(), vref)
            data.S6 = convertToVoltage(adc5.read(), vref)
            data.S7 = convertToVoltage(adc6.read(), vref)
            data.S8 = convertToVoltage(adc7.read(), vref)


            # serialize the data to send over serial
            serialzedData = ujson.dumps(data.__dict__) + '\n'
            usb.write(serialzedData)


