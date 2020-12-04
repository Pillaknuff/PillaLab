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

        # if not self.error:
        #     t = threading.Thread(target=self.__continuous_stability_check)
        #     t.start()
        for mot in self.names:
            self.__execute_position_call(mot)
        print("motors initialized with positions "+ str(self.positions))
        print("moving array: " + str(self.moving) )
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
        for i in range(len(self.stepsperunit)): #prevent 0 division error
            if self.stepsperunit[i] ==0:
                self.stepsperunit[i] = 1
        self.__configureSerial()

    def go_abs(self,mot,val):
        val = int(round(val *(self.settings["steppers.stepsperunit"][mot])))
        mot = self.settings["steppers.names"][mot]
        print("abs move requested")
        try:
            newstate = self.positions[self.names.index(mot)]
            self.commandschedule.append(["move_absolute",[mot,val]])
            threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        except:
            print("wrong motor selected " + str(mot))
            newstate = 0
        error = self.error
        return error, newstate
    
    def go_abs_all(self,vals):
        for i in range(len(vals)):
            vals[i] = int(round(vals[i] *(self.settings["steppers.stepsperunit"][i])))
        if len(vals) == len(self.names):
            for i in range(len(vals)):
                mot = self.names[i]
                val = vals[i]
                newstate = self.positions[self.names.index(mot)]
                self.commandschedule.append(["move_absolute",[mot,val]])
                threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        else:
            print("wrong motor selected " + str(mot))
            newstate = 0
        error = self.error
        return error, newstate

    def go_rel(self,mot,val):
        val = int(round(val *(self.settings["steppers.stepsperunit"][mot])))
        mot = self.settings["steppers.names"][mot]
        print("rel move requested")
        try:
            newstate = self.positions[self.names.index(mot)]
            self.commandschedule.append(["move_relative",[mot,val]])
            threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        except:
            print("wrong motor selected " + str(mot))
            newstate = 0
        error = self.error
        return error, newstate
    
    def go_rel_all(self,vals):
        for i in range(len(vals)):
            vals[i] = int(round(vals[i] *(self.settings["steppers.stepsperunit"][i])))
        if len(vals) == len(self.names):
            for i in range(len(vals)):
                mot = self.names[i]
                val = vals[i]
                newstate = self.positions[self.names.index(mot)]
                self.commandschedule.append(["move_relative",[mot,val]])
                threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        else:
            print("wrong motor selected " + str(mot))
            newstate = 0
        error = self.error
        return error, newstate

    def set_pos(self,mot,val=0): #set current motor setpoint and return it
        val = int(round(val /(self.settings["steppers.stepsperunit"][mot])))
        try:
            newstate = self.positions[self.names.index(mot)]
            self.commandschedule.append(["set_pos",[mot,val]])
            threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        except:
            print("wrong motor selected " + str(mot))
            newstate = 0
        error = self.error
        return error, newstate
    
    def setp_pos_all(self,vals): # set all motor setpoints and return them
        for i in range(len(vals)):
            vals[i] = int(round(vals[i] /(self.settings["steppers.stepsperunit"][i])))
        if len(vals) == len(self.names):
            for i in range(len(vals)):
                mot = self.names[i]
                val = vals[i]
                newstate = self.positions[self.names.index(mot)]
                self.commandschedule.append(["set_pos",[mot,val]])
                threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        else:
            print("wrong motor selected " + str(mot))
            newstate = 0
        error = self.error
        return error, newstate
    
    def get_pos(self,mot):
        oldtime = self.posTimestamps[mot]
        self.commandschedule.append(["get_pos",mot])
        threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        return False, self.positions[mot], self.moving[mot]
        # counter = 0
        # while True:
        #     newtime = self.posTimestamps[mot]
        #     if not (newtime == oldtime).all():
        #         return False, self.positions[mot], self.moving[mot]
        #     else:
        #         counter += 1
        #         if counter > 10:
        #             return True, self.positions[mot],self.moving[mot]
        #         else:
        #             time.sleep(0.1)
    
    def get_pos_all(self):
        oldtime = self.posTimestamps
        for mot in self.names:
            self.commandschedule.append(["get_pos",mot])
        threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        return False, self.positions, self.moving
        # counter = 0
        # while True:
        #     newtime = self.posTimestamps
        #     if not (newtime == oldtime).all():
        #         return False, self.positions, self.moving
        #     else:
        #         print("get pos all - no changes at run " + str(counter))
        #         counter += 1
        #         if counter > 10:
        #             return True, self.positions,self.moving
        #         else:
        #             time.sleep(1)

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
                elif comset[0] =="set_pos":
                    self.__execute_setp(comset[1][0],comset[1][1])

                if not comset[0] == "stop": #allow fast stop shooting if necessary
                    time.sleep(self.serial.timeout)

                self.lock = False #remove lock
            else:
                time.sleep(0.5) #avoid dos attack if channel blocked


    
    def __execute_rel_move(self,mot,where):
        print("moving")
        message = self.__make_message("MR",mot,where)
        ans=''

        try:
            ans,err = self.__ReadWrite(message[0])
            error = False
            print(ans)


            if "OK" in ans:
                ans,err = self.__ReadWrite(message[1])
                self.moving[mot] = True
            else:
                print("error while moving")
        
        except Exception as exc:
            error = True
            print(exc)

        return error, ans

    def __execute_abs_move(self,mot,where):
        print("moving")
        message = self.__make_message("MR",mot,where)
        ans=''

        try:
            ans,err = self.__ReadWrite(message[0])
            error = False
            print(ans)


            if "OK" in ans:
                ans,err = self.__ReadWrite(message[1])
                self.moving[mot] = True
            else:
                print("error while moving")
        
        except Exception as exc:
            error = True
            print(exc)

        return error, ans
    


    def __execute_stop(self,mot):
        print("stopping")
        message = self.__make_message("ST",mot,0)
        try:
            ans = self.__ReadWrite(message[0])
            ans = self.__ReadWrite(message[1])
            error = False
            print(ans)
        except Exception as exc:
            error = True
            print(exc)
        return error, ans
    
    def __execute_setp(self,mot,val): 
        message = self.__make_message('AP',mot,val)
        self.__ReadWrite(message[0])
        self.__ReadWrite(message[1])

    
    def __execute_position_call(self,mot):
        message = self.__make_message("OC",mot,0)
        out, err = self.__ReadWrite(message[0])
        out2, err = self.__ReadWrite(message[1])
        if not err:
            print(out2)
            out2 = out2.strip()
            num = out2[3:]
            num = int(num)

            motindex = self.names.index(mot)
            oldpos = self.positions[motindex]
            self.positions[motindex] = num/self.stepsperunit[motindex]
            self.posTimestamps[motindex] = time.time()

            if oldpos == num:
                self.moving[motindex] = False
            else: 
                self.moving[motindex] = True
        else:
            print("error getting position")
    
    # def __continuous_stability_check(self):
    #     oldpos = self.positions
    #     oldtime = self.posTimestamps
    #     while self.run:
    #         for i in self.names:
    #             self.commandschedule.append(["get_pos",i])
    #         self.__executeJobsUntilEmpty()
    #         time.sleep(self.polltime)

    #         for i in range(len(oldpos)):
    #             if not (self.posTimestamps[i] == oldtime[i]): #check, whether there is any new entry
    #                 if oldpos[i] == self.positions[i] :
    #                     self.moving[i] = False
    #                 else:
    #                     self.moving[i] = True





    def __make_message(self,what,mot,where):
        message = []
        message.append("1WP"+"{0:0=4d}".format(mot) +'\r')

        where = round(where)
        if "M" in what:
            com = "1" + what + str(where) +"\r"
        else:
            com = "1" + what +"\r"
        
        message.append(com)
        return message

        


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
                answer = answer.decode()

                if len(answer) == 0:
                    break
                output += answer
                if "\r" in answer:
                    break
            print("communication result" + answer.strip())
            return output, False
        except:
            return '', True

    #helpers and conversion



    



    



