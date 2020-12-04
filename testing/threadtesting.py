import threading
import time
import sys

class something:
    def __init__(self,num):
        print("initializing")
        self.num = num
    def doit(self): # identifier class
        print(self.num)
    def setstop(self):
        self.stop = True
    def alwaysrun(self):
        self.stop = False
        while not self.stop:
            time.sleep(1)
            print(self.num)
            sys.stdout.flush()

classdict = {}


for i in range(5): # batch create some classes
    myclass = something(i)
    classdict[i] = myclass

myThread = threading.Thread(target=myclass.doit)
myThread.start()

for i in range(5):
    myclass = classdict[i]
    myThread = threading.Thread(target=myclass.alwaysrun)
    myThread.start()

time.sleep(3)
for i in range(5):
    myclass = classdict[i]
    myclass.setstop()
    time.sleep(2)
    #myThread = threading.Thread(target=myclass.alwaysrun)
