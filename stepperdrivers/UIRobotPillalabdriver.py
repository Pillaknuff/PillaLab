'''
Author: Philipp Kagerer
Driver file for UIRobot stepper controler delivered by Omnivac for their ARPES Cryostat
Developed according to 
'''

import numpy as np
import serial
import time
import threading


class Stepper:
    def __init__(self,settings,initial=[0,0,0,0,0,0]):
        self.serial = serial.Serial()
        self.settings = settings
        
        self.positions = np.zeros(len(self.names))
        
        self.commandschedule = []                                                       #this is a list of all commands to be executed, convention: append like [commandtype,[options]]
        self.lock = False
        self.moving = np.zeros(len(self.names),dtype=bool)
        self.posTimestamps = np.zeros(len(self.names))
        self.run = True                                                                 #marker for running the program, if False while loops will terminate
        

        self.polltime = 1
        self.__connect()



    def __connect(self):
        try:
            self.serial.close()
        except:
            print('serial was not yet open, opening')
        self.__configureSerial()
        try:
            self.serial.open()
            if self.serial.isOpen():
                print("successfully connected to Steppers")
            else:
                print("stepper connection failed")
        except:
            print("serial opening on " + self.settings["steppers.com"] + " failed, try to reconnect if possible")
        self.open = self.serial.isOpen()
        self.error = self.open

    def __configureSerial(self):
        self.serial.baudrate =self.settings['steppers.baud']
        self.serial.port = self.settings['steppers.com']
        self.serial.bytesize = self.settings['steppers.bits']
        self.serial.timeout = self.settings['steppers.timeout']
        self.serial.stopbits = self.settings['steppers.stopbits']
        self.serial.parity = self.settings['steppers.parity']


    def __reconnect(self):
        try:
            self.serial.close()
        except:
            print("closing not possible")
        try:
            self.serial.open()
            success = self.serial.isOpen()
        except:
            success = False
        if not success:
            print("failed to open connection at " + str(self.serial.port) )
        return success

    def change_settings(self,settings):
        self.settings = settings
        self.serial.close()
        self.__configureSerial()
        self.reconnect()

    
