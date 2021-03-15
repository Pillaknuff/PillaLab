import numpy as np
import serial
import time
import threading

class aSerial:
    def __init__(self,settings):
        self.settings = settings
        self.serial = serial.Serial()
        self.configureSerial()
        self.connect()
        print(settings)
        self.storage={}


    def connect(self):
        try:
            self.serial.close()
        except:
            print('serial was not yet open, opening')
        self.configureSerial()
        try:
            self.serial.open()
            if self.serial.isOpen():
                print("successfull connected")
            else:
                print("serial opening not successfull")

        except:
            print("serial opening on " + self.settings["rs232.com"] + " failed, try to reconnect if possible")
        self.open = self.serial.isOpen()
        self.error = self.open

    def configureSerial(self):
        try:
            self.serial.baudrate =self.settings['rs232.baud']
            self.serial.port = self.settings['rs232.com']
            self.serial.bytesize = self.settings['rs232.bits']
            self.serial.timeout = self.settings['rs232.timeout']
            self.serial.stopbits = self.settings['rs232.stopbits']
            self.serial.parity = self.settings['rs232.parity']
        except:
            self.serial.baudrate =9600
            self.serial.port = 'com10'
            self.serial.bytesize = 8
            self.serial.timeout = 200
            self.serial.stopbits = 1
            self.serial.parity = serial.PARITY_NONE
            print("calling rs232 settings from default")
            #self.serial.parity = self.settings['rs232.parity']

    
    def ReadWrite(self,Command):
        #self.serial.open()
        print("attempting to write " + Command)
        

        try:
            self.serial.write(Command.encode())
            #self.serial.write(Command)
            #print("written")
            output = ''
            while True:
                answer = self.serial.readline() 
                if len(answer) == 0:
                    break
                output += answer.decode()
            return output, False
        except:
            print("error writing")
            return '', True
        
    def ReadLine(self):

        try:
            self.serial.flushInput()
            answer = self.serial.readline()
            answer = answer[5:90]
            answer = answer.decode()
            error = False
        except:
            print("error reading line")
            answer = ""
            error = True
        return answer,error


    
    def ReadVarianGaugeSingle(self,channel):
            message = '#0002I' + str(channel) + '\r'
            ans,err = self.ReadWrite(message)
            ans = ans.replace('\r','')
            print(ans)
            return ans
    
    def ReadAMLGaugeSingle(self,channel):
        message = '*S0' + str(channel) + '\r\n'
        ans,err = self.ReadWrite(message)
        ans = ans.replace('\r','')
        ans = ans.replace('\n','')
        #Place to further process this string!
        if channel == 0:
            try:
                p1 = ans.split(",")[0].split("@")[3]
            except Exception as e:
                print("Error in AML readings conversion p1")
                p1 = 'nan'
            return p1
        elif channel == 1:
            try:
                p2 = ans.split(",")[1].split("@")[1]
            except Exception as e:
                print("Error in AML readings conversion p2")
                p2 = 'nan'
            return p2
        else:
            return 'nan'

    def ReadWeirdAMLGaugeSingle(self,channel,recursion=0):
        # function for reading this AML gauge in screaming mode
        # does not need any requests, simply always screams the pressure into the channel...
        reading_freq = 0.5
        try: 
            [time,ans,err] = self.storage["amlweird"]
            if not abs(time - time.time())<reading_freq:
                ans,err = self.ReadLine()
                self.storage["amlweird"] = [time.time(),ans,err]
        except:
            ans,err = self.ReadLine()
            self.storage["amlweird"] = [time.time(),ans,err]



        if not err:
            myline2 = ans.replace("-","e-")
            mypressurearray = myline2.split(" ")
            myps = []
            for i in range(len(mypressurearray)):
                try:
                    myps.append(float(mypressurearray[i]))
                except:
                    myps.append(float("nan"))
            try:
                if channel == 0:
                    return str(myps[1])
                else:
                    return str(myps[7])
            except:                                                                         # complicated construct to avoid double-reading errors
                if not recursion > 20:
                    time.sleep(0.2+0.1*np.random.rand())                                    # randomized waiting before return to avoid synchronized error repeating
                    return self.ReadWeirdAMLGaugeSingle(channel,recursion=(recursion+1))    # recurse until either limit is reached or valid result is given
                else:
                    return 'nan'
        else:
            return "nan"

    """
    A short note on using the EpiMax interfaces
    Two comm-ways are possible, Modbus (complete overkill here) and QueBUS
    We are going to use QueBUS with a simple CheckSum
    -> Ascii based protocol
    -> special characters:
        > start of new message
        < start of response
        ! end of message
        ? start of data request/answer
        # start of parameter write request
        * Error in parameter set
    -> allowed signs: A-Z, a-z, 0-9, .,+,-, space

    A typical message (request) would look like:
    1 Startb, 2 Adressb, 1-n param requests, 1 terminationb, 2 chksumb 
    >           99       ?REQUESTTEXT           !               99 

    response:
    1 Startb, 2 Adressb, 1-n param answers, 1 terminationb, 2 chksumb
    <           99       RESPONSETEXT          !               99

    From the manual:
    As an example of using the protocol, consider wanting to read the measured ion gauge and Slot pressures, change the
    state of Trip 4 to override and read the states of all trips and digital inputs:
    >01?Iv?Xv?Yv#TV5?ZT?ZD!
    If check-sum (section 3.4) or CRC (section 2.3) are required, append.
    Sample response is:
    <01?Iv5.04E-09?Xv3.59E+00?Yv1.11E-04#TV?ZTx0100111?ZDxxxx0011!
    followed by the check-sum or CRC if required.

    Important parameter values:
    Xv, Yv -> Extension slot 1/2 reading (=Pirani)
    Iv, Jv -> Ion Gauge 1/2 reading
    Ev, Fv -> Emission current of IonGauge 1/2
    EE, FE -> Emission set value (0=OFF; 1=0.06mA; 2=0.1mA; 3=0.15mA; 4=0.25mA; 5=0.4mA; 6=0.6mA; 7=1mA; 8=1.5mA; 9=2.5mA; 10=4mA; 11=6mA; 12=10mA; 13=Degas Low; 14=Degas Medium; 15= Degas High; 16=Auto-emission.)
    Kv     -> Thermocouple reading
    """
