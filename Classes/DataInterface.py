from queue import Queue


# this class is needed to manage the queue for each peripheral
# and the function that retrieves the data to populate the queue

class DataInterface:
    def __init__(self, func):
        self.queue = Queue()
        self.func = func

    def getDataFunc(self):
        return self.func

    def getLastQueueItem(self):
        item = None
        while(not self.queue.empty()):
            item = self.queue.get()
        return item
