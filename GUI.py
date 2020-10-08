# Use Tkinter for python 2, tkinter for python 3
from tkinter import *
import time
import threading
import csv
from datetime import datetime
import math

from UIComponents import *
from Classes import *

temp_chamber1_name = "temperature chamber 1"
flow_controller1_name = "flow controller 1"
flow_controller2_name = "flow controller 2"
usb_interface_name = "Dev board"


temp_chamber1 = TemperatureChamber()
flow_controller1 = FlowMeter()
flow_controller2 = FlowMeter()
usb_interface = USBInterface()

class GUI():
    def __init__(self, master):

        self.RUNNING = False
        self.data = []
        self.connected_devices = []
        self.user_inputs_success = False

        self.temp_chamber_1_data_interface = DataInterface(temp_chamber1.getTempAndTimeRemaining)
        self.flow_controller1_data_interface = DataInterface(flow_controller1.readFlowRate)
        self.flow_controller2_data_interface = DataInterface(flow_controller2.readFlowRate)
        self.usb_interface_data_interface = DataInterface(usb_interface.getData)

        # ---------------------------------
        # Dev board
        # ---------------------------------
        self.dev_board = DevBoardUI(master, usb_interface_name)
        self.dev_board.getFrame().grid(row=1, column=0, sticky=W)

        # ---------------------------------
        # temp chamber
        # ---------------------------------
        self.temperature_chamber_1_ui = TemperatureChamberUI(master, temp_chamber1_name)
        self.temperature_chamber_1_ui.getFrame().grid(row=13, column=0, sticky=W)
        
        # ---------------------------------
        # Flow 1
        # ---------------------------------
        self.flow_controller_1_ui = FlowControllerUI(master, flow_controller1_name)
        self.flow_controller_1_ui.getFrame().grid(row=21, column=0, sticky=W)

        # ---------------------------------
        # Flow 2
        # ---------------------------------
        self.flow_controller_2_ui = FlowControllerUI(master, flow_controller2_name)
        self.flow_controller_2_ui.getFrame().grid(row=22, column=0, sticky=W)

        # ---------------------------------
        # Control Panel
        # ---------------------------------
        self.control_panel = ControlPanelUI(master, "Control Panel", self.start_pressed, self.stop_pressed)
        self.control_panel.getFrame().grid(row = 23, column = 0, sticky=W)

        self.peripherals = [self.dev_board, self.temperature_chamber_1_ui, self.flow_controller_1_ui, self.flow_controller_2_ui]
        
    def start_pressed(self):
        # clear data
        self.data = []

        self.checkPeripherals()
        self.setup_test()
 
    def checkPeripherals(self):
        check_mark = u'\u2713'
        x_mark = u'\u2717'
        # for enabled peripherals, check connection
        message = "checking peripherals...\n"
        self.control_panel.setMessage(message)
        for peripheral in self.peripherals:
            # todo: change the below so that it checks the connection of the peripheral
            if(peripheral.isEnabled()):
                message = message + peripheral.getTitle() + " " + check_mark + '\n'
                self.add_connected_device(peripheral)
                # if(peripheral.checkInputs() == False):
                #     self.user_inputs_success = False
                #     break
                # else:
                #     self.user_inputs_success = True
                self.user_inputs_success = True # TESTING -> REMOVE THIS LINE
            else:
                message = message + peripheral.getTitle() + " " + x_mark + '\n'
            self.control_panel.setMessage(message)
        
        print("connected devices: " + str(self.connected_devices))

    def add_connected_device(self, device):
        name = device.getTitle()
        com_port = device.getSelectedComPort()
        sample_interval = self.control_panel.getSampleInterval()
        if(not com_port == ""):
            if(name == temp_chamber1_name):
                temp_chamber1.setPort(com_port)
                self.connected_devices.append(BackgroundTask(sample_interval,self.temp_chamber_1_data_interface.queue, self.temp_chamber_1_data_interface.getDataFunc()))
            elif(name == flow_controller1_name):
                flow_controller1.setPort(com_port)
                self.connected_devices.append(BackgroundTask(sample_interval,self.flow_controller1_data_interface.queue, self.flow_controller1_data_interface.getDataFunc()))
            elif(name == flow_controller2_name):
                flow_controller2.setPort(com_port)
                self.connected_devices.append(BackgroundTask(sample_interval,self.flow_controller2_data_interface.queue, self.flow_controller2_data_interface.getDataFunc()))
            elif(name == usb_interface_name):
                usb_interface.setPort(com_port)
                self.connected_devices.append(BackgroundTask(sample_interval,self.usb_interface_data_interface.queue, self.usb_interface_data_interface.getDataFunc()))
            else:
                print("not a valid device")
        else:
            print("not a valid com port")
        
    def setup_test(self):
        self.RUNNING = True
        self.running_devices = []

        # set flow meter values
        # flow_controller1.setFlowRate(self.flow_controller_1_ui.getFlowRate())
        # time.sleep(3)
        
        # wait for flow rates to reach set flow rates

        # check if temp chamber is enabled
        if(self.temperature_chamber_1_ui.isEnabled()):
            # set temperature set point
            temp_chamber1.setPoint(round(self.temperature_chamber_1_ui.getStartTemp(),1))
            print("temperature chamber set point set...")
            # wait for temperature set point to reach starting temp
            self.waitForTempChamberSetup()

        # print("TEST: is this called after waitForTempChamberSetup() finishes?") # nope it doesnt

        

    def waitForTempChamberSetup(self):
        message = "waiting for temperature chamber to reach start temperature...\n"
        self.control_panel.setMessage(message)
        if(not round(temp_chamber1.currentChamberTemperature(), 1) == round(self.temperature_chamber_1_ui.getStartTemp(), 1)):
            print("...")
            root.after(round(self.control_panel.getSampleInterval()*1000), self.waitForTempChamberSetup)
        else:
            self.start_test()

    def start_test(self):
        print("starting test...")
        message = "starting test..."
        self.control_panel.setMessage(message)
        # go through the connected devices and start them
        for device in self.connected_devices:
            device.start()

        self.updateData()

    def updateData(self):
        # timer = self.timer.getTimerValue()

        if(self.RUNNING):
            message = "test running..."
            self.control_panel.setMessage(message)
            # get new data from queues

            # update ui with new data
            control_panel = self.control_panel
            control_panel.setTimeElapsed(control_panel.getTimeElapsed() + control_panel.getSampleInterval())

            latest_usb_data = self.usb_interface_data_interface.getLastQueueItem()
            latest_temp_chamber1_data = self.temp_chamber_1_data_interface.getLastQueueItem()
            latest_flow_controller1_data = self.flow_controller1_data_interface.getLastQueueItem()
            latest_flow_controller2_data = self.flow_controller2_data_interface.getLastQueueItem()

            if(latest_usb_data):
                self.dev_board.updateData(latest_usb_data['temperature'], latest_usb_data['humidity'], latest_usb_data['S1'], latest_usb_data['S2'], latest_usb_data['S3'], latest_usb_data['S4'], latest_usb_data['S5'], latest_usb_data['S6'], latest_usb_data['S7'], latest_usb_data['S8'])

            print(latest_temp_chamber1_data)
            if(latest_temp_chamber1_data):
                temp, hours, minutes, seconds = latest_temp_chamber1_data
                self.temperature_chamber_1_ui.setTimeRemaining(hours, minutes, seconds)
                self.temperature_chamber_1_ui.setCurrentTemperature(temp)

            if(latest_flow_controller1_data):
                self.flow_controller_1_ui.setFlowRate(latest_flow_controller1_data)
            # if(latest_flow_controller2_data):

            root.after(round(self.control_panel.getSampleInterval()*1000), self.updateData)


    def stop_pressed(self):
        self.RUNNING = False

        # go through the connected devices and stop them
        for device in self.connected_devices:
            device.stop()

        # save data to csv file
        # file_name = self.saveToCsv()
        
        # update messages that test was successful
        # message = "testing complete.\n file saved to: " + str(file_name)
        # self.control_panel.setMessage(message)

        # reset board values
        self.dev_board.reset()
        self.temperature_chamber_1_ui.reset()
        self.flow_controller_1_ui.reset()
        self.flow_controller_2_ui.reset()

    def saveToCsv(self):
        now = datetime.now()
        csv_file_name = str(now.day) + '-' + str(now.month) + '-' + str(now.year) + '-' + str(now.hour) + '-' + str(now.minute) + '-' + str(now.second) + '.csv'
        with open(csv_file_name, mode='w', newline='') as data_file:
            data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            data_writer.writerow(['time', 'temperature', 'humidity', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8'])
            time_interval = self.sample_rate_text.get()
            time = 0
            for dataPoint in self.data:
                data_writer.writerow([time, dataPoint["temperature"], dataPoint["humidity"],dataPoint["S1"],dataPoint["S2"],dataPoint["S3"],dataPoint["S4"],dataPoint["S5"],dataPoint["S6"],dataPoint["S7"],dataPoint["S8"]])
                time+=time_interval
        return csv_file_name

    def updateGUI(self, data):
        self.current_temp_text.set(data["temperature"])
        self.current_hum_text.set(data["humidity"])
        self.S1_text.set((data["S1"]))
        self.S2_text.set((data["S2"]))
        self.S3_text.set((data["S3"]))
        self.S4_text.set((data["S4"]))
        self.S5_text.set((data["S5"]))
        self.S6_text.set((data["S6"]))
        self.S7_text.set((data["S7"]))
        self.S8_text.set((data["S8"]))



if __name__ == "__main__":
    root = Tk()
    root.geometry("800x1000")
    GUI(root)
    root.mainloop()