# module for communicating with the stepper motors, structure should always be the same, a class and the methods set abs, set abs all, set rel, set rel all, zero, zero all, get , get all
import numpy as np
import serial

class Stepper:
    def __init__(self,names,settings,initial=[0,0,0,0,0,0],baud=19200,bits=7,parity='PARITY_EVEN',stopbits=1,flowcontrol=0,termChar=False,timeout=0.5):
        self.names = names
        self.initial = initial
        self.settings = settings
        self.commandschedule = [] #this is a list of all commands to be executed, convention: append like [commandtype,[options]]

        #open serial connection
        self.com = 'com2'
        ser = serial.Serial()
        ser = serial.Serial(
            #port='/dev/ttyUSB1',
            #baudrate=9600,
            parity=serial.PARITY_EVEN,
            #stopbits=serial.STOPBITS_TWO,
            #bytesize=serial.SEVENBITS
            )
        ser.baudrate = 9600
        ser.port = self.com
        ser.bytesize = bits
        ser.timeout = timeout
        #ser.parity = parity
        ser.stopbits = stopbits
        ser.open()
        self.open = ser.isOpen()
        self.serial = ser
    
    def change_settings(self,settings):
        self.settings = settings

    def set_abs(self,mot,val):
        newstate = 0
        error = False
        return error, newstate
    
    def set_abs_all(self,vals):
        newstate = np.zeros(len(self.names))
        error = False
        return error, newstate

    def set_rel(self,mot,val):
        newstate = 0
        error = False
        return error, newstate
    
    def set_rel_all(self,vals):
        newstate = np.zeros(len(self.names))
        error = False
        return error, newstate

    def setp(self,mot,val=0): #set current motor setpoint and return it
        newstate = 0
        error = False
        return error, newstate
    
    def setp_all(self,vals): # set all motor setpoints and return them
        newstate = np.zeros(len(self.names))
        error = False
        return error, newstate
    
    def get(self,mot):
        newstate = 0
        moving = False
        error = False
        return error, newstate, moving
    
    def get_all(self):
        newstate = np.zeros(len(self.names))
        moving = np.zeros((len(self.names)),dtype=bool)
        error = False
        return error, newstate, moving
    

    def executeJobsUntilEmpty(self):
        while not len(self.commandschedule) ==0:
            comset = self.commandschedule[0]
            self.commandschedule.remove(comset)



    def __makeCommandString__(self,Motor,Command,Data):
        acommand = str(Motor) + Command + str(Data) + '\r'
        return acommand
        # Command List:
        #qp = query positions
        #qs = query speed
        #ap = set actual positoin
        #sv = set velocity
        #ma = move absolute
        #mr = move relative
        #st = stop
        #Oc does whatever

    def executeMovementCommand(self,comtype,mot,whereto):
        try:
            com = "1WP" + "{0:0=4d}".format(mot) +'\r'
        except: #switch to python 2 formalism
            com = "1WP" + str("%04d"%mot) +'\r'
        
        answer = self.__ReadWrite__(com)
        print(answer)

        com = "1" + comtype + str(whereto)
        answer = self.__ReadWrite__(com)
        print(answer)
    



    
    def __ReadWrite__(self,Command):
        #self.serial.open()
        self.serial.write(Command)
        output = ''
        while True:
            answer = self.serial.read() 
            if len(answer) == 0:
                break
            output += answer
        return output


    # short convention: 
    # motor is selected by 1WP000x
    # then something is read
    # then command to move is sent as 1MR/1MA and steps
    # then check and understand the answer