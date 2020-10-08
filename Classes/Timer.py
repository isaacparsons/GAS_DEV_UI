import threading
import time

class Timer:
    def __init__(self, sample_interval):
        self.timer = 0
        self.sample_rate_intervals_count = 1
        self.sample_interval = sample_interval
        self.is_running = False
        self.thread = threading.Thread(target=self.runTimer)

    def startTimer(self):
        self.is_running = True
        self.start_time = time.time()
        self.thread.start()
        

    def runTimer(self):
        while(self.is_running):
            next_interval = self.sample_rate_intervals_count * self.sample_interval
            if((time.time() - self.start_time) > next_interval):
                self.timer = next_interval
                self.sample_rate_intervals_count = self.sample_rate_intervals_count + 1

    def stopTimer(self):
        self.is_running = False

    
    def getTimerValue(self):
        return round(self.timer, 1)
