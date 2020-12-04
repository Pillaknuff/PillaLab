
import drivers.PyTangoReader as TangoRead
from misc.txtLinelogger as Logger
from datetime import datetime
import time

now = datetime.now() # current date and time

date_time = now.strftime("%m_%d_%Y_%H_%M_%S")

settings = {}

settings["PyTango.deviceadresses"] = 'hassppa3control:1000/asphere/test/keithley6517a'
settings["PyTango.devicetypes"]  = 'Keithley_standard'
settings["PyTango.devicename"] = 'Keithley1'


Loggingobject = Logger.txtLinelogger('Currentlog_'+str(date_time),['time','I_Beamline'],'.', firstcolumn='' )

myDriver = TangoRead.PyTangoWrapper(settings)
while True:
    err,val = myDriver.ReadDeviceByName('Keithley1')
    print(val)
    Loggingobject.writeLine([datetime.now().timestamp(),val])
    time.sleep(0.1)
print(val)