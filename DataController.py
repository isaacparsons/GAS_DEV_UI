from queue import Queue
import threading
import time

from TemperatureChamber import TemperatureChamber
from FlowMeter import FlowMeter
from USBInterface import USBInterface

class DataController:
    def __init__(self, func, args):
        self.running = True
        self.func = func
        self.args = args
        self.queue = Queue()
        self.thread = threading.Thread(target=self.run)
        
    def start(self):
        self.thread.start()

    def terminate(self):
        self.running = False
        self.thread.join()

    def run(self):
        while(self.running):
            # run function
            response = self.func(*self.args)
            self.queue.put(response)
            print(list(self.queue.queue))
            time.sleep(5)


flowMeterController = FlowMeter("COM6")
usbinterface = USBInterface("COM3")

flowmeter1Task = DataController(flowMeterController.readFlowRate, [])
usbinterfaceTask = DataController(usbinterface.getData, [])


def main():
    flowmeter1Task.start()
    time.sleep(5)
    usbinterfaceTask.start()
    time.sleep(20)
    flowmeter1Task.terminate()
    usbinterfaceTask.terminate()


main()