import time

class Programm:
    def __init__(self,theController):
        self.theController = theController
        self.running = False
        self.paused = False


    def run(self):
        if not self.running:
            self.running = True
            self.paused = False
            self.mainProgram()
        else:
            self.paused = False
        
    def pause(self):
        self.paused = True
    
    def stop(self):
        self.running = True

    def mainProgram(self):
        i = 0
        while self.running:
            if not self.paused:
                print("still alive " + str(i))
                time.sleep(2)
                i += 1
