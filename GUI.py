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



class GUI():
    def __init__(self, master):

        self.RUNNING = False
        self.data = []
        self.connected_devices = []

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

        # reset dev board values
        self.dev_board.reset()
        # clear data
        self.data = []

        # check user inputs
        self.user_inputs_success = (self.temperature_chamber_1_ui.checkInputs() 
            and self.flow_controller_1_ui.checkInputs()
            and self.control_panel.checkInputs())
        print("user inputs success: " + str(self.user_inputs_success))

        self.checkPeripherals()
        self.start_test()
        # self.flow_controller = FlowMeter("COM6")
        # print(self.flow_controller.checkCommunication())
 
    def checkPeripherals(self):
        check_mark = u'\u2713'
        x_mark = u'\u2717'
        # for enabled peripherals, check connection
        message = "checking peripherals...\n"
        self.control_panel.setMessage(message)
        for peripheral in self.peripherals:
            # todo: change the below so that it checks the connection
            if(peripheral.isEnabled()):
                message = message + peripheral.getTitle() + " " + check_mark + '\n'
                self.add_connected_device(peripheral)
            else:
                message = message + peripheral.getTitle() + " " + x_mark + '\n'
            self.control_panel.setMessage(message)
        
        print(self.connected_devices)

    def add_connected_device(self, device):
        name = device.getTitle()
        com_port = device.getSelectedComPort()
        print(com_port)
        if(not com_port == ""):
            if(name == temp_chamber1_name):
                self.connected_devices.append(TemperatureChamber(com_port))
            elif(name == flow_controller1_name):
                self.connected_devices.append(FlowMeter(com_port))
            elif(name == flow_controller2_name):
                self.connected_devices.append(FlowMeter(com_port))
            elif(name == usb_interface_name):
                self.connected_devices.append(USBInterface(com_port))
            else:
                print("not a valid device")
        else:
            print("not a valid com port")
        
    def start_test(self):
        self.RUNNING = True
        self.running_devices = []
        sample_interval = self.control_panel.getSampleInterval()
        print(sample_interval)
        # self.bgTask = DataController(sample_interval, self.connected_devices[0].getData)
        # self.bgTask.start()
        self.timer = Timer()
        self.timer.startTimer()
            # self.bgTask.printQueue()
        self.updateUI()
        # self.bgTask.stop()

    def updateUI(self):
        timer = self.timer.getTimerValue()
        if(timer == 10):
            return
        else:
            print(timer)
            root.after(1000, self.updateUI)


    def stop_pressed(self):
        self.RUNNING = False
        # save data to csv file
        # self.saveToCsv()
        # self.result_text.set("Test completed successfully")

    # def retrieveData(self):
    #     while (self.RUNNING):

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
    root.geometry("800x900")
    GUI(root)
    root.mainloop()