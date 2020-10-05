from tkinter import *
import Utils


class DevBoardRowUI:
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


class DevBoardUI:
    def __init__(self, parent, title):
        self.title = title
        self.labelframe = LabelFrame(parent, text=title, padx=10, pady=10)

        # com port
        Label(self.labelframe, text="COM PORT: ").grid(row = 2, column = 0)
        self.selected_com_port = StringVar()
        self.selected_com_port.set('')
        self.com_ports = Utils.getComPorts()
        option = OptionMenu(self.labelframe, self.selected_com_port, *self.com_ports).grid(row = 2, column = 1)


        #  current temp row
        self.dev_board_temp_row = DevBoardRowUI(self.labelframe, "temperature (C)")
        self.dev_board_temp_row.getDevBoardRow().grid(row=4,column=0)

        # current humidity row
        self.dev_board_humidity_row = DevBoardRowUI(self.labelframe, "Humidity (%)")
        self.dev_board_humidity_row.getDevBoardRow().grid(row=5,column=0)

        # S1 row
        self.dev_board_s1_row = DevBoardRowUI(self.labelframe, "S1")
        self.dev_board_s1_row.getDevBoardRow().grid(row=6,column=0)

        # S2 row
        self.dev_board_s2_row = DevBoardRowUI(self.labelframe, "S2")
        self.dev_board_s2_row.getDevBoardRow().grid(row=7,column=0)

        # S3 row
        self.dev_board_s3_row = DevBoardRowUI(self.labelframe, "S3")
        self.dev_board_s3_row.getDevBoardRow().grid(row=8,column=0)

        # S4 row
        self.dev_board_s4_row = DevBoardRowUI(self.labelframe, "S4")
        self.dev_board_s4_row.getDevBoardRow().grid(row=9,column=0)

        # S5 row
        self.dev_board_s5_row = DevBoardRowUI(self.labelframe, "S5")
        self.dev_board_s5_row.getDevBoardRow().grid(row=10,column=0)

        # S6 row
        self.dev_board_s6_row = DevBoardRowUI(self.labelframe, "S6")
        self.dev_board_s6_row.getDevBoardRow().grid(row=11,column=0)

        # S7 row
        self.dev_board_s7_row = DevBoardRowUI(self.labelframe, "S7")
        self.dev_board_s7_row.getDevBoardRow().grid(row=12,column=0)

        # S8 row
        self.dev_board_s8_row = DevBoardRowUI(self.labelframe, "S8")
        self.dev_board_s8_row.getDevBoardRow().grid(row=13,column=0)

    def getTitle(self):
        return self.title

    def getSelectedComPort(self):
        return self.selected_com_port.get()

    def isEnabled(self):
        return True

    def reset(self):
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

    def getFrame(self):
        return self.labelframe