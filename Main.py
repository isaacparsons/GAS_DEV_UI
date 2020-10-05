from queue import Queue
import threading
import time

from TemperatureChamber import TemperatureChamber
from FlowMeter import FlowMeter
from RepeatingTask import RepeatingTask


def threadFunction(func, queue, *args):
    response = func(*args)
    queue.put(response)
    print(list(queue.queue))


flowMeterController = FlowMeter()

flowmeter1Queue = Queue()
flowmeter2Queue = Queue()
TemperatureChamberQueue = Queue()
flowmeter1Task = RepeatingTask(threadFunction, [fakeComm, flowmeter1Queue, "COM3"])


def main():

    # set up applicable peripherals

    # start peripherals 

    # wait 1/sample rate seconds, get data from queue, then clear queue

    # stop when stop is pressed or temp chamber countdown completes
    
    x = threading.Thread(target=flowmeter1Task.run)
    x.start()
    time.sleep(10)
    flowmeter1Task.terminate()
    x.join()
    print(list(flowmeter1Queue.queue))


main()