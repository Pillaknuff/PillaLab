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
        message = '*O0' + str(channel) + '\r\n'
        ans,err = self.ReadWrite(message)
        ans = ans.replace('\r','')
        ans = ans.replace('\n','')
        #Place to further process this string!
        print(ans)
        return ans

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