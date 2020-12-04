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

                rs232connector = RSInterface.aSerial(settingsRs)
                #convention: interface, channel, type
                self.interfaces[self.settings["pressures.names"][i]] = [rs232connector,self.settings["pressures.channels"][i],self.settings["pressures.types"][i]]
                self.controllers[conum] = rs232connector
            else:
                rs232connector = self.controllers[conum]
                self.interfaces[self.settings["pressures.names"][i]] = [rs232connector,self.settings["pressures.channels"][i],self.settings["pressures.types"][i]]
            



    def readone(self,name):             # read one pressure, interface for multi read
        arr = self.interfaces[name]     # grab right element of pre initialized interfaces
        interf = arr[0]                 # RS232 interface
        channel = arr[1]                # channel to read
        tp = arr[2]                     # type of gauge to select reading procedure

        error = False

        if tp == "VarianBA":            # reader for varian gauges
            p = interf.ReadVarianGaugeSingle(channel)
            if p == '':
                p = str(random.random())#'0'
        elif tp == "AML_weird":
            p = interf.ReadWeirdAMLGaugeSingle(channel)
        else:                           # include aml here later
            p = "0"

                                        # convert what you read to float
        if "E03" in p:                  # Varian underrange error
            p = '1E-11'
        try:                            # multi step try and error conversion
            p = float(p)                
        except:
            try:
                p= p.rstrip()
                p = p.replace('>','')
                p = float(p)
            except Exception as e:
                print("error converting " + str(p) + " to float")
                print(e)
                p = float(0)
                error = True
            

        return p, error

    def readall(self):
        names = []
        pressures = []
        errors = []
        for name in self.settings["pressures.names"]:
            p = self.readone(name)
            names.append(name)
            pressures.append(p[0])
            errors.append(p[1])
        return names,pressures,errors
    
    
    def checkstatus(self):
        a = []
        for name in self.settings["pressures.names"]:
            a.append(1)
        return a