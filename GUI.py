# Use Tkinter for python 2, tkinter for python 3
from tkinter import *
import time
import threading
from queue import Queue
import csv
import serial
from datetime import datetime

from TemperatureChamber import TemperatureChamber
from FlowMeter import FlowMeter
from RepeatingTask import RepeatingTask

from USBInterface import Interface


def getComPorts():
    ports = ['COM%s' % (i + 1) for i in range(256)]
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    if(len(result) == 0):
        return ['']
    else:
        return result

def threadFunction(func, queue, *args):
    response = func(*args)
    queue.put(response)

class UIComponent:
    def __init__(self, parent, title)
        self.title = title
        self.labelframe = LabelFrame(parent, text=title,width=600, padx=10, pady=10 )

        # com port
        Label(self.labelframe, text="COM PORT: ").grid(row = 2, column = 0)
        self.selected_com_port = StringVar()
        self.com_ports = getComPorts()
        option = OptionMenu(self.labelframe, self.selected_com_port, *self.com_ports).grid(row = 2, column = 1)


    def getTitle(self):
        return self.title

    def getFrame(self):
        return self.labelframe
        
    def getSelectedComPort(self):
        return self.selected_com_port

class FlowControllerUI:
    def __init__(self, parent, title):
        self.max_flow_rate = 10.0

        self.queue = Queue()

        self.title = title
        self.labelframe = LabelFrame(parent, text=title,width=600, padx=10, pady=10 )
        # enable flow controller checkbox
        self.flow_controller_enabled = BooleanVar()
        Checkbutton(self.labelframe, text="enable", variable=self.flow_controller_enabled).grid(row=1)

        # com port
        Label(self.labelframe, text="COM PORT: ").grid(row = 2, column = 0)
        self.selected_com_port = StringVar()
        self.com_ports = getComPorts()
        option = OptionMenu(self.labelframe, self.selected_com_port, *self.com_ports).grid(row = 2, column = 1)

        # gas type
        Label(self.labelframe, text="Gas type: ").grid(row = 3, column = 0)
        self.gas_type = StringVar()
        self.gas_type_input = Entry(self.labelframe, textvariable=self.gas_type).grid(row = 3, column = 1)

        # flow controller 1 flow rate
        Label(self.labelframe, text="Flow rate (ml/min)").grid(row = 4, column = 0)
        self.flow_rate = DoubleVar()
        self.flow_rate_input = Entry(self.labelframe, textvariable=self.flow_rate).grid(row = 4, column = 1)

    def getTitle(self):
        return self.title

    def startTask(self):
        flowmeter_task = RepeatingTask(threadFunction, [fakeComm, self.queue, "COM3"])

    def setController(self):
        self.flow_meter_controller = FlowMeter(self.selected_com_port)

    def getFlowController(self):
        return self.labelframe

    def getSelectedComPort(self):
        return self.selected_com_port

    def getGasType(self):
        return self.gas_type

    def getFlowRate(self):
        return self.flow_rate

    def checkInputs(self):
        if(self.selected_com_port.get() == "" or self.gas_type.get() == "" or self.flow_rate.get() > self.max_flow_rate):
            return False
        else:
            return True

    def isEnabled(self):
        return self.flow_controller_enabled.get()

    def reset(self):
        self.selected_com_port.set("")
        self.gas_type.set("")
        self.flow_rate.set(0.0)


class TemperatureChamberUI:
    def __init__(self, parent, title):
        self.min_temp = -55.0
        self.max_temp = 120.0

        self.title = title
        self.labelframe = LabelFrame(parent, text=title, padx=10, pady=10)

        # enable flow controller checkbox
        self.temperature_chamber_enable = BooleanVar()
        Checkbutton(self.labelframe, text="enable", variable=self.temperature_chamber_enable).grid(row=1)

        # Com port
        Label(self.labelframe, text="COM PORT: ").grid(row = 2, column = 0)
        self.selected_com_port = StringVar()
        self.com_ports = getComPorts()
        option = OptionMenu(self.labelframe, self.selected_com_port, *self.com_ports).grid(row = 2, column = 1)

        # start temp
        Label(self.labelframe, text="Starting Temperature (degrees celius): ").grid(row = 3, column = 0)
        self.start_temp = DoubleVar()
        self.start_temp_input = Entry(self.labelframe, textvariable=self.start_temp).grid(row = 3, column = 1)
        # end temp
        Label(self.labelframe, text="Ending Temperature (degrees celsius): ").grid(row = 4, column = 0)
        self.end_temp = DoubleVar()
        self.end_temp_input = Entry(self.labelframe, textvariable=self.end_temp).grid(row = 4, column = 1)

        # time
        Label(self.labelframe, text="Duration: ").grid(row = 5, column = 0)
        self.temp_duration_hours = DoubleVar()
        self.temp_duration_minutes = DoubleVar()
        self.temp_duration_seconds = DoubleVar()
        Label(self.labelframe, text="Hours: ").grid(row = 5, column = 1)
        self.temp_duration_hours_input = Entry(self.labelframe, textvariable=self.temp_duration_hours).grid(row = 5, column = 2)
        Label(self.labelframe, text="Minutes: ").grid(row = 6, column = 1)
        self.temp_duration_minutes_input = Entry(self.labelframe, textvariable=self.temp_duration_minutes).grid(row = 6, column = 2)
        Label(self.labelframe, text="Seconds: ").grid(row = 7, column = 1)
        self.temp_duration_seconds_input = Entry(self.labelframe, textvariable=self.temp_duration_seconds).grid(row = 7, column = 2)

    def getTitle(self):
        return self.title
    def getTemperatureChamber(self):
        return self.labelframe

    def getSelectedComPort(self):
        return self.selected_com_port

    def getStartTemp(self):
        return self.start_temp
    
    def getEndTemp(self):
        return self.end_temp

    def getDurationHours(self):
        return self.temp_duration_hours

    def getDurationMinutes(self):
        return self.temp_duration_minutes

    def getDurationSeconds(self):
        return self.temp_duration_seconds

    def checkInputs(self):
        if(self.start_temp.get() > self.max_temp 
            or self.start_temp.get() < self.min_temp
            or self.end_temp.get() > self.max_temp
            or self.end_temp.get() < self.min_temp
            or self.temp_duration_hours.get() + self.temp_duration_minutes.get() + self.temp_duration_seconds.get() == 0
            or self.selected_com_port.get() == ""):
            return False
        else:
            return True

    def isEnabled(self):
        return self.temperature_chamber_enable.get()

    def reset(self):
        self.start_temp.set(0.0)
        self.end_temp.set(0.0)
        self.temp_duration_hours.set(0.0)
        self.temp_duration_minutes.set(0.0)
        self.temp_duration_seconds.set(0.0)
        

class DevBoardRow:
    def __init__(self, parent, title):
        self.frame = Frame(parent)
        Label(self.frame, text=title).grid(row = 1, column = 0)
        self.value = DoubleVar()
        self.value.set(0.0)
        Label(self.frame, textvariable=self.value).grid(row = 1, column = 1)

    def getDevBoardRow(self):
        return self.frame

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value


class DevBoard:
    def __init__(self, parent, title):
        self.labelframe = LabelFrame(parent, text=title, padx=10, pady=10)

        # time elapsed row
        self.time_elapsed_row = DevBoardRow(self.labelframe, "time elapsed (sec)")
        self.time_elapsed_row.getDevBoardRow().grid(row=1,column=0)

        #  current temp row
        self.dev_board_temp_row = DevBoardRow(self.labelframe, "temperature (C)")
        self.dev_board_temp_row.getDevBoardRow().grid(row=2,column=0)

        # current humidity row
        self.dev_board_humidity_row = DevBoardRow(self.labelframe, "Humidity (%)")
        self.dev_board_humidity_row.getDevBoardRow().grid(row=3,column=0)

        # S1 row
        self.dev_board_s1_row = DevBoardRow(self.labelframe, "S1")
        self.dev_board_s1_row.getDevBoardRow().grid(row=4,column=0)

        # S2 row
        self.dev_board_s2_row = DevBoardRow(self.labelframe, "S2")
        self.dev_board_s2_row.getDevBoardRow().grid(row=5,column=0)

        # S3 row
        self.dev_board_s3_row = DevBoardRow(self.labelframe, "S3")
        self.dev_board_s3_row.getDevBoardRow().grid(row=6,column=0)

        # S4 row
        self.dev_board_s4_row = DevBoardRow(self.labelframe, "S4")
        self.dev_board_s4_row.getDevBoardRow().grid(row=7,column=0)

        # S5 row
        self.dev_board_s5_row = DevBoardRow(self.labelframe, "S5")
        self.dev_board_s5_row.getDevBoardRow().grid(row=8,column=0)

        # S6 row
        self.dev_board_s6_row = DevBoardRow(self.labelframe, "S6")
        self.dev_board_s6_row.getDevBoardRow().grid(row=9,column=0)

        # S7 row
        self.dev_board_s7_row = DevBoardRow(self.labelframe, "S7")
        self.dev_board_s7_row.getDevBoardRow().grid(row=10,column=0)

        # S8 row
        self.dev_board_s8_row = DevBoardRow(self.labelframe, "S8")
        self.dev_board_s8_row.getDevBoardRow().grid(row=11,column=0)

    def reset(self):
        self.time_elapsed_row.setValue(0.0)
        self.dev_board_temp_row.setValue(0.0)
        self.dev_board_humidity_row.setValue(0.0)
        self.dev_board_s1_row.setValue(0.0)
        self.dev_board_s2_row.setValue(0.0)
        self.dev_board_s3_row.setValue(0.0)
        self.dev_board_s4_row.setValue(0.0)
        self.dev_board_s5_row.setValue(0.0)
        self.dev_board_s6_row.setValue(0.0)
        self.dev_board_s7_row.setValue(0.0)
        self.dev_board_s8_row.setValue(0.0)

    def getDevBoard(self):
        return self.labelframe


class ControlPanel:
    def __init__(self, parent, title, start_pressed, stop_pressed):
        self.min_sample_interval = 0.1
        self.labelframe = LabelFrame(parent, text=title, padx=10, pady=10, width=600)
        Label(self.labelframe, text="Sample Interval (secs)").grid(row = 0, column = 0)
        self.sample_rate_text = DoubleVar()
        self.sample_rate_input = Entry(self.labelframe, textvariable=self.sample_rate_text)
        self.sample_rate_input.grid(row=0, column=1)

        self.start = Button(self.labelframe, text="START", command=start_pressed)
        self.start.grid(row=1, column=0, sticky=W, padx=5, pady=5)

        self.stop = Button(self.labelframe, text="STOP", command=stop_pressed)
        self.stop.grid(row=2, column = 0, sticky=W, padx=5, pady=5)

        Label(self.labelframe, text="Messages").grid(row = 0, column = 2, sticky=W)
        self.message_text = StringVar()

        self.message_text.set("To begin, select peripherals you want, insert sample rate and press start")
        Label(self.labelframe, textvariable=self.message_text).grid(row = 1, column = 2, columnspan=2, rowspan=2)

    def checkInputs(self):
        if(self.sample_rate_text.get() < self.min_sample_interval):
            return False
        else:
            return True

    def setMessage(self, msg):
        self.message_text.set(msg)

    def getControlPanel(self):
        return self.labelframe

class GUI():

    def __init__(self, master):

        self.RUNNING = False
        self.data = []

        # ---------------------------------
        # Dev board
        # ---------------------------------
        self.dev_board = DevBoard(master, "Dev board")
        self.dev_board.getDevBoard().grid(row=1, column=0, sticky=W)

        # ---------------------------------
        # temp chamber
        # ---------------------------------
        self.temperature_chamber_1_ui = TemperatureChamberUI(master, "temperature chamber 1")
        self.temperature_chamber_1_ui.getTemperatureChamber().grid(row=13, column=0, sticky=W)
        # ---------------------------------
        # Flow 1
        # ---------------------------------
        self.flow_controller_1_ui = FlowControllerUI(master, "flow controller 1")
        self.flow_controller_1_ui.getFlowController().grid(row=21, column=0, sticky=W)
        # ---------------------------------
        # Flow 2
        # ---------------------------------
        self.flow_controller_2_ui = FlowControllerUI(master, "flow controller 2")
        self.flow_controller_2_ui.getFlowController().grid(row=22, column=0, sticky=W)
        # ---------------------------------
        # Control Panel
        # ---------------------------------
        self.control_panel = ControlPanel(master, "Control Panel", self.start_pressed, self.stop_pressed)
        self.control_panel.getControlPanel().grid(row = 23, column = 0, sticky=W)

        self.peripherals = [self.temperature_chamber_1_ui, self.flow_controller_1_ui, self.flow_controller_2_ui]

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
            else:
                message = message + peripheral.getTitle() + " " + x_mark + '\n'
            self.control_panel.setMessage(message)

    def stop_pressed(self):
        self.RUNNING = False
        # save data to csv file
        self.saveToCsv()
        self.result_text.set("Test completed successfully")


    def retrieveData(self):
        interface = Interface("COM3")
        while (self.RUNNING):
            response, error = interface.getData()
            if(error):
                self.RUNNING = False
                self.result_text.set("Error: timed out trying to get response from pyduino")
                break
            else:
                self.data.append(response)
                time.sleep(self.sample_rate_text.get())
                newTime = round(self.time_elapsed_text.get() + 0.1, 1)
                self.time_elapsed_text.set(newTime)
                self.updateGUI(response)

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