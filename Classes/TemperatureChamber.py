# temp chamber protocol is Modbus RTU

import minimalmodbus
import time
import serial

class TemperatureChamber:
    def __init__(self):
        self.steps = 1
        self.set_point = None

    def setPort(self, port):
        self.instrument = minimalmodbus.Instrument(port, 1)  # port name, slave address (in decimal)
        self.instrument.serial.baudrate = 9600
        self.instrument.close_port_after_each_call = True


    # sometimes the chamber is slow to respond 
    def writeReg(self, regNum, val, decimals):
        self.instrument.write_register(regNum, val, decimals, 6, True)
        time.sleep(0.01)

    def writeRegNoResponse(self, regNum, val, decimals):
        try:
            self.instrument.write_register(regNum, val, decimals, 6, True)
        except IOError:
            print("Failed to read from instrument")

    def createProfile(self):
        # create profile
        self.writeReg(4002,1,0)
        self.profileNumber = self.instrument.read_register(4000, 0)

    def nameProfile(self):
        if(self.profileNumber):
            profileNameStartReg = 3500 + (self.profileNumber - 1) * 10
            profileName = [71,65,83,84,69,83,84,32,32,32] # decimal equivalent of ascii characters GASTEST 
            # write each character  
            for i in range(10):
                self.writeReg(profileNameStartReg + i, profileName[i], 0)
            return True
        else:
            return False

    def deleteProfile(self):
        # if the profile has been created then we can delete it
        if(self.profileNumber):
            self.writeReg(4001, 1, 0)
            self.writeReg(4002, 3,0)
            return True
        else:
            return False
       
    def startProfile(self):
        if(self.profileNumber):
            self.writeReg(4001, 1, 0) # set step number
            self.writeRegNoResponse(4002, 5, 0) # start profile
        else:
            return False

    # def stopProfile(self):

    def readRemainingProfileTime(self):
        hours = self.instrument.read_register(4119) # hours
        minutes = self.instrument.read_register(4120) # minutes
        seconds = self.instrument.read_register(4121) # seconds
        return hours, minutes, seconds

    # for ramp do (1, 0, 0,0,0,0,0,0,0,0,x,x,x,x,1,0)
    def addStep(self, stepType, inputWait, eo1, eo2, eo3, eo4, eo5, eo6, eo7, eo8, hours, mins, secs, sp, pid, gs):
        self.writeReg(4002,2,0) # insert step
        self.writeReg(4001,1,0) # set current step number
        self.writeReg(4003,stepType,0) # set step type to "ramp time"
        self.writeReg(4012,inputWait,0) # set "wait for" flag to 0 since we dont want to wait for input
        self.writeReg(4030,eo1,0) # we dont want any event outputs so we set those to off
        self.writeReg(4031,eo2,0)
        self.writeReg(4032,eo3,0)
        self.writeReg(4033,eo4,0)
        self.writeReg(4034,eo5,0)
        self.writeReg(4035,eo6,0)
        self.writeReg(4036,eo7,0)
        self.writeReg(4037,eo8,0)
        self.writeReg(4009,hours,0) # enter the ramp time hours
        self.writeReg(4010,mins,0) # enter the ramp time minutes
        self.writeReg(4011,secs,0) # enter the ramp time seconds
        self.writeReg(4044, sp, 1) # enter set point channel 1
        self.writeReg(4046, pid, 0) # enter PID set channel 1
        self.writeReg(4048, gs, 0) # enable Guaranteed Soak for channel 1
        self.steps = self.steps + 1

    def addEndStep(self):
        self.writeReg(4001,self.steps,0)  # set current step number
        self.writeReg(4060, 0, 0) # set end step to hold
    
    def setPoint(self, pt):
        # set set point
        self.writeReg(300, pt, 1)
        self.set_point = pt

    def currentChamberTemperature(self):
        return self.instrument.read_register(100, 1, 3, True)


# tempChamber = TemperatureChamber("COM9")
# tempChamber.createProfile()
# tempChamber.addStep(1,0,0,0,0,0,0,0,0,0,0,10,0,40,1,0) # ramp step
# tempChamber.addEndStep()

# time.sleep(3)
# print("setting set point...")
# tempChamber.setPoint(-10.2)
# # tempChamber.startProfile()
# for i in range(20):
#     time.sleep(10)
#     t = tempChamber.currentChamberTemperature()
#     # h, m, s = tempChamber.readRemainingProfileTime()
#     print(t)
#     # print(str(h)+":"+str(m)+":"+str(s))
