from tkinter import *

class ControlPanelUI:
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

        # time elapsed row
        self.time_elapsed_text = DoubleVar()
        Label(self.labelframe, text="Time Elapsed: ").grid(row=0, column=2, sticky=W)
        Label(self.labelframe, textvariable=self.time_elapsed_text).grid(row=0, column=3, sticky=W)

        Label(self.labelframe, text="Messages").grid(row = 1, column = 2, sticky=W)
        self.message_text = StringVar()

        self.message_text.set("To begin, select peripherals you want, insert sample rate and press start")
        Label(self.labelframe, textvariable=self.message_text).grid(row = 1, column = 2, columnspan=2, rowspan=2)

    def checkInputs(self):
        if(self.sample_rate_text.get() < self.min_sample_interval):
            return False
        else:
            return True

    def getSampleInterval(self):
        return self.sample_rate_text.get()

    def setSampleRateIntervale(self, sampleInterval):
        self.sample_rate_text.set(sampleInterval)

    def setMessage(self, msg):
        self.message_text.set(msg)

    def getTimeElapsed(self):
        return self.time_elapsed_text.get()

    def setTimeElapsed(self, time):
        self.time_elapsed_text.set(time)

    def getFrame(self):
        return self.labelframe