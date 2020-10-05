from queue import Queue
import threading
import time


class DataController:
    def __init__(self, sampleInterval, __taskFuncPointer_):
        self.isRunning = False
        self.sampleInterval = sampleInterval
        self.__taskFuncPointer_ = __taskFuncPointer_
        self.queue = Queue()
        self.thread = threading.Thread(target=self.workerThread)
        
    def start(self):
        self.isRunning = True
        self.thread.start()

    def stop(self):
        self.isRunning = False

    def printQueue(self):
        print(list(self.queue.queue))

    def workerThread(self):
        while(self.isRunning):
            res = self.__taskFuncPointer_()
            self.queue.put(res)
            time.sleep(self.sampleInterval)


# flowMeterController = FlowMeter("COM6")
# usbinterface = USBInterface("COM3")

# flowmeter1Task = DataController(flowMeterController.readFlowRate, [])
# usbinterfaceTask = DataController(usbinterface.getData, [])


# def main():
#     flowmeter1Task.start()
#     time.sleep(5)
#     usbinterfaceTask.start()
#     time.sleep(20)
#     flowmeter1Task.terminate()
#     usbinterfaceTask.terminate()


# main()