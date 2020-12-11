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
            if self.controllers[conum] == 0:                                                            # then init, otherwise just enter
                settingsRs = self.sortoutsettings(conum)                                                # call sorting function with error catching
                rs232connector, error = self.createConnection(settingsRs,self.settings["pressures.types"][i])
                                                                                                        # convention: interface, channel, type
                self.interfaces[self.settings["pressures.names"][i]] = [rs232connector,self.settings["pressures.channels"][i],self.settings["pressures.types"][i],error]
                self.controllers[conum] = rs232connector
            else:
                rs232connector = self.controllers[conum]
                self.interfaces[self.settings["pressures.names"][i]] = [rs232connector,self.settings["pressures.channels"][i],self.settings["pressures.types"][i]]
            


    def createConnection(self,settingsRs,crtype):                                                       # Function sorting out what driver to use for the connection
        connector = ""                                                                                  # empty standard object
        error = False
        if crtype in  ["VarianBA", "AML_weird", "AML"]:                                                 # simple rs232 question-answer ascii communication
            try:
                connector = RSInterface.aSerial(settingsRs)
            except Exception as e:
                print("Error connecting to gauge with settings " + str(settingsRs) + " Error: " + str(e))
                error = True
        elif crtype in ["epiMaxUni"]:                                                                   # epimax Modbus communication
            try:
                import drivers.epiMaxDriver as epiMaxDriver
                connector = epiMaxDriver.PVCi(settingsRs["rs232.com"])
            except Exception as e:
                print("Error connecting to epimax gauge with settings " + str(settingsRs) + " Error: " + str(e))
                error = True
        else:
            print("Ion gauge type " + str(crtype) + " not supported!")
            error = True
        
        return connector,error

    def sortoutsettings(self,conum):                                                                    # Function sorting the respective entries from the main settings file and creating settings for each driver device
        settingsRs = {}
        wordpairlist = [
            ['rs232.baud',"pressures.baud"],
            ['rs232.com',"pressures.com"],
            ['rs232.bits',"pressures.bits"],
            ['rs232.timeout',"pressures.timeout"],
            ['rs232.stopbits',"pressures.stopbits"],
            ['rs232.parity',"pressures.parity"],
            ]
        for wordpair in wordpairlist:
            try:
                settingsRs[wordpair[0]] = self.settings[[wordpair[1]]][conum]
            except Exception as e:
                print("Error while sorting Pressure gauge settings: " + str(e))
        return settingsRs

    def readone(self,name):             # read one pressure, interface for multi read
        arr = self.interfaces[name]     # grab right element of pre initialized interfaces
        interf = arr[0]                 # RS232 interface
        channel = arr[1]                # channel to read
        tp = arr[2]                     # type of gauge to select reading procedure

        error = arr[3]

        if not error:                       # check for initialisation error
            if tp == "VarianBA":            # reader for varian gauges
                p = interf.ReadVarianGaugeSingle(channel)
                if p == '':
                    p = str(random.random())#'0'
            elif tp == "AML_weird":
                p = interf.ReadWeirdAMLGaugeSingle(channel)
            elif tp == "epiMaxUni":         # read special epi-max driver
                if channel == 1:
                    p = interf.ion_gauge_1_pressure
                elif channel == 2:
                    p = interf.slot_a_value_1
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
        else:
            p = float("nan")
            

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