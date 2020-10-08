import threading
import time

# creates a thread that repeats every 'sampleInterval' seconds.
# the thread runs '__taskFuncPointer_' and adds the result to 
# 'queue'
class BackgroundTask:
    def __init__(self, sampleInterval, queue, __taskFuncPointer_):
        self.isRunning = False
        self.queue = queue
        self.sampleInterval = sampleInterval
        self.__taskFuncPointer_ = __taskFuncPointer_
        self.thread = threading.Thread(target=self.workerThread)
        
    def start(self):
        self.isRunning = True
        self.thread.start()

    def stop(self):
        self.isRunning = False
        self.thread.join()

    def workerThread(self):
        while(self.isRunning):
            res = self.__taskFuncPointer_()
            if(not res == None):
                self.queue.put(res)
            time.sleep(self.sampleInterval)
