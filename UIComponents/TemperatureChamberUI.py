from tkinter import *
import Utils


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
        self.com_ports = Utils.getComPorts()
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
    def getFrame(self):
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