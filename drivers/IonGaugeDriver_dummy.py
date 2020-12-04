import random
import drivers.aSimpleRS232 as RSInterface
import numpy as np

class IonGaugeTalker:
    def __init__(self,settings):
        self.settings = settings
        self.interfaces = {}
        self.controllers = np.zeros(max(self.settings["pressures.controllers"])+1).tolist()

        for i in range(len(self.settings["pressures.names"])):
            conum = settings["pressures.controllers"][i]
            if self.controllers[conum] == 0: #then init, otherwise just enter
                settingsRs = {}
                settingsRs['rs232.baud'] = self.settings["pressures.baud"][conum]
                settingsRs['rs232.com'] = self.settings["pressures.com"][conum]
                settingsRs['rs232.bits'] = self.settings["pressures.bits"][conum]
                settingsRs['rs232.timeout'] = self.settings["pressures.timeout"][conum]
                settingsRs['rs232.stopbits'] = self.settings["pressures.stopbits"][conum]
                settingsRs['rs232.parity'] = self.settings["pressures.parity"][conum]

                rs232connector = 1#RSInterface.aSerial(settingsRs)
                #convention: interface, channel, type
                self.interfaces[self.settings["pressures.names"][i]] = [rs232connector,self.settings["pressures.channels"][i],self.settings["pressures.types"][i]]
                self.controllers[conum] = rs232connector
            else:
                rs232connector = self.controllers[conum]
                self.interfaces[self.settings["pressures.names"][i]] = [rs232connector,self.settings["pressures.channels"][i],self.settings["pressures.types"][i]]
            
        print (self.interfaces)



            



    def readone(self,name):
        return random.random()

    def readall(self):
        names = []
        pressures = []
        for name in self.settings["pressures.names"]:
        #     arr = self.interfaces[name]
        #     interf = arr[0]
        #     channel = arr[1]
        #     tp = arr[2]
            
        #     if tp == "VarianBA":
        #         p = interf.ReadVarianGaugeSingle(channel)
        #         if p == '':
        #             p = str(random.random())#'0'
        #     else:
        #         p = "0"
            p = str(random.random())
            names.append(name)
            pressures.append(p)
        return names,pressures
            


    
    def checkstatus(self):
        a = []
        for name in self.settings["pressures.names"]:
            a.append(1)
        return a