# Use Tkinter for python 2, tkinter for python 3
import time
import threading
import math


class Timer:
    def __init__(self):
        self.timer = 0
        self.is_running = False
        self.thread = threading.Thread(target=self.runTimer)

    def startTimer(self):
        self.is_running = True
        self.start_time = time.time()
        self.thread.start()
        

    def runTimer(self):
        while(self.is_running):
            if(math.floor(time.time() - self.start_time) > self.timer):
                self.timer = math.floor(time.time() - self.start_time)

    def stopTimer(self):
        self.is_running = False

    
    def getTimerValue(self):
        return self.timer



def main():
    t = Timer()
    t.startTimer()
    for i in range(20):
        print(t.getTimerValue())
        time.sleep(2)

    t.stopTimer()



main()