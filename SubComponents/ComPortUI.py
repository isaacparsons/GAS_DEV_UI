from tkinter import *
import Utils
import os
from PIL import Image, ImageTk


class ComPortUI:
    def __init__(self, parent):
        self.frame = Frame(parent)
        Label(self.frame, text="COM PORT").grid(row = 0, column = 0)
        self.selected_com_port = StringVar()
        self.selected_com_port.set('')
        self.refresh()
        fn = os.path.join(os.path.dirname(__file__), 'refresh.png')
        image = Image.open(fn)
        image = image.resize((15, 15), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(image)
        self.refresh_btn = Button(self.frame, text="refresh", image=self.photo, command=self.refresh).grid(row=0, column = 2)

    def getSelectedComPort(self):
        return self.selected_com_port.get()

    def refresh(self):
        self.selected_com_port.set('')
        self.option = OptionMenu(self.frame, self.selected_com_port, *Utils.getComPorts()).grid(row = 0, column = 1)

    def getFrame(self):
        return self.frame