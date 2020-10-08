from tkinter import *
import Utils


class DevBoardRowUI:
    def __init__(self, parent, title):
        self.frame = Frame(parent)
        Label(self.frame, text=title).grid(row = 0, column = 0)
        self.value = DoubleVar()
        self.value.set(0.0)
        Label(self.frame, textvariable=self.value).grid(row = 1, column = 0)


    def getDevBoardRow(self):
        return self.frame

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value.set(round(value,2))


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
        self.dev_board_humidity_row.getDevBoardRow().grid(row=4,column=1)

        # S1 row
        self.dev_board_s1_row = DevBoardRowUI(self.labelframe, "S1")
        self.dev_board_s1_row.getDevBoardRow().grid(row=4,column=2)

        # S2 row
        self.dev_board_s2_row = DevBoardRowUI(self.labelframe, "S2")
        self.dev_board_s2_row.getDevBoardRow().grid(row=4,column=3)

        # S3 row
        self.dev_board_s3_row = DevBoardRowUI(self.labelframe, "S3")
        self.dev_board_s3_row.getDevBoardRow().grid(row=4,column=4)

        # S4 row
        self.dev_board_s4_row = DevBoardRowUI(self.labelframe, "S4")
        self.dev_board_s4_row.getDevBoardRow().grid(row=4,column=5)

        # S5 row
        self.dev_board_s5_row = DevBoardRowUI(self.labelframe, "S5")
        self.dev_board_s5_row.getDevBoardRow().grid(row=4,column=6)

        # S6 row
        self.dev_board_s6_row = DevBoardRowUI(self.labelframe, "S6")
        self.dev_board_s6_row.getDevBoardRow().grid(row=4,column=7)

        # S7 row
        self.dev_board_s7_row = DevBoardRowUI(self.labelframe, "S7")
        self.dev_board_s7_row.getDevBoardRow().grid(row=4,column=8)

        # S8 row
        self.dev_board_s8_row = DevBoardRowUI(self.labelframe, "S8")
        self.dev_board_s8_row.getDevBoardRow().grid(row=4,column=9)

    def getTitle(self):
        return self.title

    def getSelectedComPort(self):
        return self.selected_com_port.get()

    def isEnabled(self):
        return True

    def reset(self):
        self.updateData(0,0,0,0,0,0,0,0,0,0)

    def checkInputs(self):
        if(self.getSelectedComPort() ==""):
            return False
        else:
            return True

    def updateData(self, temp, hum, s1, s2, s3, s4, s5, s6, s7, s8):
        self.dev_board_temp_row.setValue(temp)
        self.dev_board_humidity_row.setValue(hum)
        self.dev_board_s1_row.setValue(s1)
        self.dev_board_s2_row.setValue(s2)
        self.dev_board_s3_row.setValue(s3)
        self.dev_board_s4_row.setValue(s4)
        self.dev_board_s5_row.setValue(s5)
        self.dev_board_s6_row.setValue(s6)
        self.dev_board_s7_row.setValue(s7)
        self.dev_board_s8_row.setValue(s8)

    def getFrame(self):
        return self.labelframe