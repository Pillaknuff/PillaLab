# module for communicating with the stepper motors, structure should always be the same, a class and the methods set abs, set abs all, set rel, set rel all, zero, zero all, get , get all
import numpy as np
import serial
import time
import threading

'''
structure as follows:
class Stepper with methods:
    go_abs(_all)
    go_rel(_all)
    get_pos(_all)
    
    each of them calling the executeJobsuntilempty Method and scheduling a task
    lock implemented on the RS232 port
    underlying methods for actually running the commands are only called by the executor
'''

class Stepper:
    def __init__(self,settings,initial=[0,0,0,0,0,0]):
        self.serial = serial.Serial()
        self.settings = settings
        self.__set_settings()
        
        self.positions = initial[:len(self.names)]
        
        self.commandschedule = [] #this is a list of all commands to be executed, convention: append like [commandtype,[options]]
        self.lock = False
        self.moving = np.zeros(len(self.names),dtype=bool)
        self.posTimestamps = np.zeros(len(self.names))
        self.run = True #marker for running the program, if False while loops will terminate
        

        self.polltime = 1
        self.__connect()

        if not self.error:
            t = threading.Thread(target=self.__continuous_stability_check)
            t.start()

        #open serial connection
        



    def __del__(self):
        self.run = False
        self.serial.close()
        print("motion driver killed")
    
    def __connect(self):
        try:
            self.serial.close()
        except:
            print('serial was not yet open, opening')
        self.__configureSerial()
        try:
            self.serial.open()
            print("successfull connected")
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


    def reconnect(self):
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
        self.__set_settings()
    
    def __set_settings(self):
        self.names = self.settings['steppers.names']
        self.com = self.settings["steppers.com"]
        self.stepsperunit = self.settings['steppers.stepsperunit']
        self.__configureSerial()

    def go_abs(self,mot,val):
        val = int(round(val /(self.settings["steppers.stepsperunit"][mot])))
        print("abs move requested")
        try:
            newstate = self.positions[mot]
            self.commandschedule.append(["move_absolute",[mot,val]])
            threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        except:
            print("wrong motor selected " + str(mot))
        error = self.error
        return error, newstate
    
    def go_abs_all(self,vals):
        for i in range(len(vals)):
            vals[i] = int(round(vals[i] /(self.settings["steppers.stepsperunit"][i])))
        if len(vals) == len(self.names):
            for i in range(len(vals)):
                mot = self.names[i]
                val = vals[i]
                newstate = self.positions[mot]
                self.commandschedule.append(["move_absolute",[mot,val]])
                threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        else:
            print("wrong motor selected " + str(mot))
        error = self.error
        return error, newstate

    def go_rel(self,mot,val):
        val = int(round(val /(self.settings["steppers.stepsperunit"][mot])))
        print("rel move requested")
        try:
            newstate = self.positions[mot]
            self.commandschedule.append(["move_relative",[mot,val]])
            threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        except:
            print("wrong motor selected " + str(mot))
        error = self.error
        return error, newstate
    
    def go_rel_all(self,vals):
        for i in range(len(vals)):
            vals[i] = int(round(vals[i] /(self.settings["steppers.stepsperunit"][i])))
        if len(vals) == len(self.names):
            for i in range(len(vals)):
                mot = self.names[i]
                val = vals[i]
                newstate = self.positions[mot]
                self.commandschedule.append(["move_relative",[mot,val]])
                threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        else:
            print("wrong motor selected " + str(mot))
        error = self.error
        return error, newstate

    def set_pos(self,mot,val=0): #set current motor setpoint and return it
        try:
            newstate = self.positions[mot]
            self.commandschedule.append(["set_pos",[mot,val]])
            threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        except:
            print("wrong motor selected " + str(mot))
        error = self.error
        return error, newstate
    
    def setp_pos_all(self,vals): # set all motor setpoints and return them
        if len(vals) == len(self.names):
            for i in range(len(vals)):
                mot = self.names[i]
                val = vals[i]
                newstate = self.positions[mot]
                self.commandschedule.append(["set_pos",[mot,val]])
                threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        else:
            print("wrong motor selected " + str(mot))
        error = self.error
        return error, newstate
    
    def get_pos(self,mot):
        oldtime = self.posTimestamps[mot]
        self.commandschedule.append(["get_pos",mot])
        threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        counter = 0
        while True:
            newtime = self.posTimestamps[mot]
            if not (newtime == oldtime).all():
                return False, self.positions[mot], self.moving[mot]
            else:
                counter += 1
                if counter > 10:
                    return True, self.positions[mot],self.moving[mot]
                else:
                    time.sleep(0.1)
    
    def get_pos_all(self):
        oldtime = self.posTimestamps
        for mot in self.names:
            self.commandschedule.append(["get_pos",mot])
        threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        counter = 0
        while True:
            newtime = self.posTimestamps
            if not (newtime == oldtime).all():
                return False, self.positions, self.moving
            else:
                print("get pos all - no changes at run " + str(counter))
                counter += 1
                if counter > 10:
                    return True, self.positions,self.moving
                else:
                    time.sleep(0.1)

        #moving = False
        #error = False
        #return error, newstate, moving
    
    def stop_all(self):
        self.commandschedule = []
        for mot in self.names:
            self.commandschedule.append(["stop",mot])
        threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread


    def __executeJobsUntilEmpty(self): #written in a way to allow multitasking, while blocking double occupation of com port
        while not len(self.commandschedule) ==0:
            if not self.lock: #check if already running
                self.lock = True #set lock, exclusive access to com port now
                comset = self.commandschedule[0]
                self.commandschedule = self.commandschedule[1:]

                if comset[0] == "move_relative":
                    self.__execute_rel_move(comset[1][0],comset[1][1])
                elif comset[0] == "move_absolute":
                    self.__execute_abs_move(comset[1][0],comset[1][1])
                elif comset[0] == "stop":
                    self.__execute_stop(comset[1])
                elif comset[0] == "get_pos":
                    self.__execute_position_call(comset[1])
                
                if not comset[0] == "stop": #allow fast stop shooting if necessary
                    time.sleep(self.serial.timeout)

                self.lock = False #remove lock
            else:
                time.sleep(0.5) #avoid dos attack if channel blocked


    
    def __execute_rel_move(self,mot,where):
        print("moving")
        message = self.__make_message(4,1,mot,where)
        try:
            ans = self.__ReadWrite(message)
            error = False
            print(ans)
        except Exception as exc:
            error = True
            print(exc)
        self.moving[mot] = True

        return error, ans

    def __execute_abs_move(self,mot,where):
        print("moving")
        message = self.__make_message(4,1,mot,where)
        try:
            ans = self.__ReadWrite(message)
            error = False
            print(ans)
        except Exception as exc:
            error = True
            print(exc)
        self.moving[mot] = True

        return error, ans
    


    def __execute_stop(self,mot):
        print("stopping")
        message = self.__make_message(3,0,mot,0)
        try:
            ans = self.__ReadWrite(message)
            error = False
            print(ans)
        except Exception as exc:
            error = True
            print(exc)
        return error, ans
    
    def __execute_setp(self,mot,val): #a little bit weird way to do that: first set the point, the stop an move back, otherwise it would try to move to original position in new coordinate system
        message = self.__make_message(5,1,mot,val)
        self.__ReadWrite(message)
        self.__execute_stop(mot)
        self.__execute_abs_move(mot,val)

    
    def __execute_position_call(self,mot):
        message = self.__make_message(6,1,mot,0)
        out, err = self.__ReadWrite(message)
        if not err:
            num, message = self.__decode_message(out)
            self.positions[mot] = num
            self.posTimestamps[mot] = time.time()
    
    def __continuous_stability_check(self):
        oldpos = self.positions
        oldtime = self.posTimestamps
        while self.run:
            for i in self.names:
                self.commandschedule.append(["get_pos",i])
            self.__executeJobsUntilEmpty()
            time.sleep(self.polltime)

            for i in range(len(oldpos)):
                if not (self.posTimestamps[i] == oldtime[i]): #check, whether there is any new entry
                    if oldpos[i] == self.positions[i] :
                        self.moving[i] = False
                    else:
                        self.moving[i] = True





    def __make_message(self,instr,ctype,mot,val):
        nums = [1,instr,ctype,mot]
        #number convention:
        #absolute 1 - 4 - 0 - x
        #relative 1 - 4 - 1 - x
        #stop     1 - 3 - 0 - x

        nbits = 32
        hexnum = self.__intTo8digithex(val,nbits)
        #print(hexnum)
        hexnum = hexnum[(len(hexnum)-8):len(hexnum)] #only look at last 8 (for safety, ignore 0x)
        hexnumarr = [int(hexnum[0:2],16),int(hexnum[2:4],16),int(hexnum[4:6],16),int(hexnum[6:8],16)] #necessary for control count

        nums += hexnumarr #append in the right order, e.g. nums, 4-val numbers (8 bit)
        hexnumarr = nums
        controlcount = 0

        for num in hexnumarr:
            controlcount += num
        controlcount = controlcount%256 #add up and modulo 1 byte
        hexnumarr.append(controlcount)
        outstr = ''

        for num in hexnumarr:
            outstr += chr(num) #conversion to unicode character (should be ascii)
        return outstr

    def __decode_message(self,message):
        out = '0x'
        for char in message:
            out += hex(ord(char))[2:]
        message = out[(len(out)-10):(len(out)-2)]
        num = self.__twos_complement(message,32)
        print("decoding" + message + " as " +  out + " with num =  " + str(num))
        return num, message
        


    def __ReadWrite(self,Command):
        #self.serial.open()
        print("attempting to write " + Command)
        

        try:
            self.serial.write(Command.encode())
            #self.serial.write(Command)
            #print("written")
            output = ''
            while True:
                answer = self.serial.read() 
                if len(answer) == 0:
                    break
                output += answer
            return output, False
        except:
            return '', True

    #helpers and conversion
    def __twos_complement(self,hexstr,bits):
        value = int(hexstr,16)
        if value & (1 << (bits-1)):
            value -= 1 << bits
        return value
    
    def __intTo8digithex(self,num,nbits):
        num =hex((num + (1 << nbits)) % (1 << nbits))
        head = num[0:2]
        num = num[2:]
        interlen = 8 - len(num)
        med = ''
        if interlen > 0:
            for i in range(interlen):
                med += '0'
        return head + med + num



    



    



