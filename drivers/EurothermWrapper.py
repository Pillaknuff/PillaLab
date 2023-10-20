import random
import drivers.eurotherm as eurotherm
import drivers.eurotherm3500 as eurotherm35
import numpy as np
import threading
import time

class EurothermWrapper:
    def __init__(self,settings):
        self.settings = settings
        self.interfaces = {}


        for i in range(len(self.settings["growthcontrol.Controlernicknames"])):

            if "growthcontrol.baud" in self.settings.keys():
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

            # create a small lib for the importand controller settings to be transfered
            controllersettings = self.writeControlerSettingsToLib(i)




            # Initialize the actual controller
            if PIDtype == "eurotherm2408":
                try:
                    error = False
                    myeurotherm = eurotherm.eurotherm2408(port,slaveAddress=slavead,baudrate=baud)
                except Exception as e:
                    print("error, while initializing eurotherm at port " + str(port) + " with baud " + str(baud) + " and slave adress " + str(slavead) + ": " + str(e))
                    error = True
            elif PIDtype == "eurotherm3508":
                try:
                    error = False
                    myeurotherm = eurotherm35.Eurotherm3500(port,slaveAddress=slavead)
                except Exception as e:
                    print("error, while initializing eurotherm3500 at port " + str(port) + " and slave adress " + str(slavead) + ": " + str(e))
                    error = True
            else:
                error = True
            #convention: interface, settingslib
            if not error:
                self.interfaces[self.settings["growthcontrol.Controlernicknames"][i]] = [myeurotherm,controllersettings]


            
    # settings update: -> this is not meant to reinitialize everything, only to change things like PID values, ....
    def updateSettingsToDevices(self,settings):
        self.settings = settings
        keylist = self.interfaces.keys()
        for key in keylist:
            try:
                num = self.settings["growthcontrol.Controlernicknames"].index(key)          # find the corresponding number to sort out the settings
                setlist = self.writeControlerSettingsToLib(num)
                self.interfaces[key] = [self.interfaces[key][0],setlist]        # keep interface, update underlying settings
            except Exception as e:
                print("error updating settins for PID " + str(e))

    
    def writeControlerSettingsToLib(self,num):                                  # Function to sort the settings for the individual controlers
        controllersettings = {}
        wordpairs = [["standardramp","growthcontrol.standardramprates"],        # extremely badass notation for sorting wordpairs from settings lib to devices
        ["ControllerType","growthcontrol.type"],
        ["PIDswitchingpoints","growthcontrol.PIDswitchingpoints"],
        ["externalPIDs","growthcontrol.externalPIDs"],
        ["useexternalPIDvals","growthcontrol.useexternalPIDvals"],
        ]
        for wordpair in wordpairs:                                              # do the actual sorting with error catching
            try: 
                controllersettings[wordpair[0]] = self.settings[wordpair[1]][num]
            except Exception as e:
                print("error while pulling controler settings for PID: " + str(e))
        return controllersettings

    def setTemperature(self,PIDname,setp):                                              # simple temperature set with standard ramp
        #ind = self.settings["PIDs.names"].index(PIDname)
        try:
            [controller,settings] = self.interfaces[PIDname]
            controller.ramp = settings["standardramp"]
            if settings["useexternalPIDvals"]:                                          # check, if PID values should be adjusted, if yes..adjust
                self.setPIDsBySetpoint(PIDname,setp)
            controller.setpoint = setp                                                  # set actual setpoint, the PID will now ramp towards this value
        except Exception as e:
            print("error setting temperature " + str(e))
    
    def rampTemperature(self,PIDname,setp,ramp):                                        # function setting a new ramp, then giving the new setpoint
        try:
            [controller,settings] = self.interfaces[PIDname]
            controller.rampRate = ramp                                                  # write desired ramp rate
            if settings["useexternalPIDvals"]:                                          # check, if PID values should be adjusted, if yes..adjust
                self.setPIDsBySetpoint(PIDname,setp)
            controller.setpoint = setp
        except Exception as e:
            print("error ramping temperature " + str(e))

    def setRamp(self,controller,ramp):                                                  # function to set ramps, unused by now
        try:
            controller.rampRate = ramp
        except Exception as e:
            print("error setting ramp " + str(e))

    def readTemperature(self,PIDname):                                                  # read temperature of cell, 
        try:
            [controller,settings] = self.interfaces[PIDname]
            readtemp = controller.temperature
            #print("reading at " + str(PIDname) + " : " + str(readtemp))
        except Exception as e:
            print("Error in Eurotherm Read " + str(e))
            readtemp = 0
        return readtemp


#***********Section used for Autotuning and partial PID adjustment********************************
    def grabAutotuneOnSetpoint(self,PIDname,setp):                                     # function activating autotune on setpoint, checking until it is finished, then pulling the PID's and returning them
        try:
            [controller,settings] = self.interfaces[PIDname]
            self.ActivateAutotuneOnValue(PIDname,setp)
            while controller.Autotune_enable == True:                                        # check every 5s for autotune to end, if it ends grab params
                time.sleep(5)
            # check for used parameter set
            paramset = self.getUsedParameterset(PIDname)
            if paramset == 1:                                                               # pid = tupel of (P,I,D)
                pid = controller.pid
            elif paramset == 2:
                pid = controller.pid2
            error = False
        except Exception as e:
            print("error while Autoadjusting PID's" + str(e))
            pid = (float('nan'),float('nan'),float('nan'))
            error = True
        return pid,error

    def ActivateAutotuneOnValue(self,PIDname,setp):                                     # set setpoint, Activate Autotune
        try:
            [controller,settings] = self.interfaces[PIDname]
            controller.setpoint = setp
            controller.Autotune_enable = True
        except Exception as e:
            print("error setting Autotune " + str(e))
    
    def setPIDValues(self,PIDname,pid):                                                 # set pid values to controler
        try:
            [controller,settings] = self.interfaces[PIDname]
            paramset = self.getUsedParameterset(PIDname)
            if paramset==1:
                controller.pid = pid
            elif paramset == 2:
                controller.pid2 = pid
        except Exception as e:
            print("Error setting pid values" + str(e))

     
    def getUsedParameterset(self,PIDname):
        #[controller,settings] = self.interfaces[PIDname]
        return 1
    
    def setPIDsBySetpoint(self,PIDname,setp):                                          # super neat function used to change the PID set according to the temperature setpoint
        try:
            [controller,settings] = self.interfaces[PIDname]
            T_list = settings["PIDswitchingpoints"]
            T_index = next(i for i, x in enumerate(T_list) if x >= setp)
            pidSet = settings["externalPIDs"][T_index]
            self.setPIDValues(PIDname,pidSet)
        except Exception as e:
            print("error adjusting PID values to setpoint " + str(e))