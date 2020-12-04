try:
    from PyTango import DeviceProxy as dp
    forceddummymode = False # forces random number generation
except Exception as e:
    print("Error in PyTangoImport - starting PyTango in forced dummy mode: " + str(e))
    forceddummymode = True
import random
# d = dp('hassppa3control:1000/asphere/test/keithley6517a')
# print(d.Current)

'''
Driver for PyTango reading of Keithley Devices
Written 12.08.2020
'''

class PyTangoWrapper:
    def __init__(self,settings):
        self.settings = settings
        print(self.settings)
        if forceddummymode:                                             # avoid malfuction during PyTango Import and make GUI function anyway...will only return random numbers of course
            self.settings["PyTango.dummymode"] = True

        self.devices = self.settings["PyTango.deviceadresses"]
        self.devicetypes = self.settings["PyTango.devicetypes"]         # relevant types for now: Keithley_standard
        self.devicereferers = self.settings["PyTango.devicename"]

        self.devicelist = {}
        if not self.settings["PyTango.dummymode"]:
            for device,devicetype,devicereferer in zip(self.devices,self.devicetypes,self.devicereferers):
                err, d = self.connectDevice(device)
                if not err:
                    self.devicelist[devicereferer] = [d,devicetype]
        


    def connectDevice(self,adress):
        err = False
        try:
            d = dp(adress)
        except Exception as e:
            err = True
            print(e)
        
        return err, d
    
    def ReadDeviceByName(self,name,what='standard'):
        if not self.settings["PyTango.dummymode"]:
            err = False
            try:
                [device,devicetype] = self.devicelist['name']
                if what == 'standard':
                    if devicetype == 'Keithley_standard':
                        retval = float(device.Current)
                else:
                    retval = float(0)
            except Exception as e:
                err = True
                retval = 0
                print("error in PyTangoDriver Read: " + str(e))
            
            return err, retval
        else:
            return False, random.random()
            