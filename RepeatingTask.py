class RepeatingTask:
    def __init__(self, func, args):
        self.running = True
        self.func = func
        self.args = args
        
    def terminate(self):
        self.running = False

    def run(self):
        while(self.running):
            # run function
            self.func(*self.args)