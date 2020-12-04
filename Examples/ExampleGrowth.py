import time

class Programm:
    def __init__(self,controller):
        self.controller = controller
    def run(self):
        self.running = 2
        print("yo")
        time.sleep(5)
        print("hobo")
        self.controller.SetTSubsandStabilize(222)
    def pause(self):
        self.running = 1
    def stop(self):
        self.running = 0
    def printit(self):
        print("hi")
    