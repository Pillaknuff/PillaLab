import random
import drivers.eurotherm as eurotherm
import numpy as np
import threading
class EurothermWrapper:
    def __init__(self,settings):
        self.settings = settings
        self.interfaces = {}


        for i in range(len(self.settings["growthcontrol.Controlernicknames"])):

            if "PIDs.baud" in self.settings.keys():
                baud = self.settings["growthcontrol.baud"][i]
            else:
                baud = 9600
                print("eurotherm standardbaud")
            
            if "growthcontrol.slaveadress" in self.settings.keys():
                slavead = self.settings["growthcontrol.slaveadress"][i]
            else:
                slavead = 1
                print("eurotherm standardslave")

            port = self.settings["growthcontrol.com"][i]
            PIDtype = self.settings["growthcontrol.type"][i]
            
            if PIDtype == "eurotherm2408":
                try:
                    error = False
                    myeurotherm = eurotherm.eurotherm2408(port,slaveAddress=slavead,baudrate=baud)
                except Exception as e:
                    print("error, while initializing eurotherm: " + str(e))
                    error = True
            else:
                error = True
            #convention: interface, channel, type
            if not error:
                self.interfaces[self.settings["growthcontrol.Controlernicknames"][i]] = [myeurotherm,PIDtype]


            


    def setTemperature(self,PIDname,setp):
        #ind = self.settings["PIDs.names"].index(PIDname)
        try:
            [controller,ctype] = self.interfaces[PIDname]
            controller.setpoint = setp
        except Exception as e:
            print(e)
    
    def rampTemperature(self,PIDname,setp,ramp): # function setting a new ramp, then giving the new setpoint and creating a timer to reset the ramprate, try not to doubly set a ramp!
        try:
            [controller,ctype] = self.interfaces[PIDname]
            oldramp = controller.rampRate
            controller.rampRate = ramp
            print("ramping")
            neededtime = float(abs((setp-controller.temperature)/ramp)) + float(20) # give time offset!
            controller.setpoint = setp
            recallthread = threading.Timer(neededtime,self.setRamp,[controller,oldramp])
            recallthread.start()
        except Exception as e:
            print(e)

    def setRamp(self,controller,ramp):
        print("ramp reset to " + str(ramp))
        controller.rampRate = ramp
    
    def readTemperature(self,PIDname):
        try:
            [controller,ctype] = self.interfaces[PIDname]
            readtemp = controller.temperature
        except Exception as e:
            print(e)
            readtemp = 0
        return readtemp

