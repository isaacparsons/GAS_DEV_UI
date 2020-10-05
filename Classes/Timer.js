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
