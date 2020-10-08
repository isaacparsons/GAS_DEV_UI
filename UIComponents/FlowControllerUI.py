from tkinter import *
import Utils
from SubComponents import *



class FlowControllerUI:
    def __init__(self, parent, title):
        self.max_flow_rate = 10.0

        self.title = title
        self.labelframe = LabelFrame(parent, text=title,width=600, padx=10, pady=10 )
        
        # enable flow controller checkbox
        self.flow_controller_enabled = BooleanVar()
        Checkbutton(self.labelframe, text="enable", variable=self.flow_controller_enabled).grid(row=1)

        # com port
        self.com_port_ui = ComPortUI(self.labelframe)
        self.com_port_ui.getFrame().grid(row=2, column=0)

        # gas type
        Label(self.labelframe, text="Gas type: ").grid(row = 3, column = 0)
        self.gas_type = StringVar()
        self.gas_type_input = Entry(self.labelframe, textvariable=self.gas_type).grid(row = 3, column = 1)

        # flow controller 1 flow rate
        Label(self.labelframe, text="Flow rate (L/min)").grid(row = 4, column = 0)
        self.flow_rate = DoubleVar()
        self.flow_rate_input = Entry(self.labelframe, textvariable=self.flow_rate).grid(row = 4, column = 1)

        # flow controller 1 current rate
        Label(self.labelframe, text="Current flow rate (L/min").grid(row = 5, column = 0)
        self.current_flow_rate = DoubleVar()
        Label(self.labelframe, textvariable=self.current_flow_rate).grid(row = 5, column = 1)

    def getTitle(self):
        return self.title

    def getFrame(self):
        return self.labelframe

    def getSelectedComPort(self):
        return self.com_port_ui.getSelectedComPort()

    def getGasType(self):
        return self.gas_type.get()

    def setGasType(self, gas_type):
        self.gas_type.set(gas_type)

    def getFlowRate(self):
        return self.flow_rate.get()

    def setFlowRate(self, flow_rate):
        self.flow_rate.set(round(flow_rate, 2))

    def checkInputs(self):
        if(self.com_port_ui.getSelectedComPort() == "" or self.gas_type.get() == "" or self.flow_rate.get() > self.max_flow_rate):
            return False
        else:
            return True

    def isEnabled(self):
        return self.flow_controller_enabled.get()

    def reset(self):
        self.gas_type.set("")
        self.flow_rate.set(0.0)