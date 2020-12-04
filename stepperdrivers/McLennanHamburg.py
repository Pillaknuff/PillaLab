# module for communicating with the stepper motors, structure should always be the same, a class and the methods set abs, set abs all, set rel, set rel all, zero, zero all, get , get all
import numpy as np
import serial
import time
import threading
import re

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
        print(settings)
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
        # for mot in self.names:
        #     self.__execute_position_call(mot)
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
        self.channels = self.settings['steppers.channels']
        self.com = self.settings["steppers.com"]
        self.stepsperunit = self.settings['steppers.stepsperunit']
        for i in range(len(self.stepsperunit)): #prevent 0 division error
            if self.stepsperunit[i] ==0:
                self.stepsperunit[i] = 1
        self.__configureSerial()

    def go_abs(self,mot,val):
        try:
            val = int(round(val *(self.settings["steppers.stepsperunit"][mot])))
        except:
            return True, 0
        #val = int(round(val *(self.settings["steppers.stepsperunit"][mot])))
        #val = val-self.positions[mot]
        mot = self.settings["steppers.channels"][mot]
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
        if len(vals) == len(self.names):
            for i in range(len(vals)):
                try:
                    vals[i] = int(round(vals[i] *(self.settings["steppers.stepsperunit"][i])))
                    nonnumeric = False
                except:
                    nonnumeric = True
                if not nonnumeric:
                    mot = self.channels[i]
                    val = vals[i]#-self.positions[i]
                    newstate = self.positions[self.channels.index(mot)]
                    self.commandschedule.append(["move_absolute",[mot,val]])
                    threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        else:
            print("wrong motor selected " + str(mot))
            newstate = 0
        error = self.error
        return error, newstate

    def go_rel(self,mot,val):
        try:
            val = int(round(val *(self.settings["steppers.stepsperunit"][mot])))
        except:
            return True, 0
        
        mot = self.settings["steppers.names"][mot]
        print("rel move requested")
        try:
            newstate = self.positions[self.channels.index(mot)]
            self.commandschedule.append(["move_relative",[mot,val]])
            threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
            newstate = 0
        except:
            print("wrong motor selected " + str(mot))
            newstate = 0
        error = self.error
        return error, newstate
    
    def go_rel_all(self,vals):

        if len(vals) == len(self.names):
            for i in range(len(vals)):
                try:
                    vals[i] = int(round(vals[i] *(self.settings["steppers.stepsperunit"][i])))
                    nonnumeric = False
                except:
                    nonnumeric = True
                if not nonnumeric:
                    mot = self.channels[i]
                    val = vals[i]
                    newstate = self.positions[self.channels.index(mot)]
                    self.commandschedule.append(["move_relative",[mot,val]])
                    threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
                    newstate = 0
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
        motindex = self.settings["steppers.names"].index(mot)
        print("queried: " + str(mot))
        oldtime = self.posTimestamps[motindex]
        self.commandschedule.append(["get_pos",mot])
        threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
        
        
        counter = 0
        while True:
            newtime = self.posTimestamps[motindex]
            if not (newtime == oldtime).all():
                print("good")
                return False, self.positions[motindex], self.moving[motindex]
            else:
                counter += 1
                if counter > 10:
                    print("bad")
                    return True, self.positions[motindex],self.moving[motindex]
                else:
                    time.sleep(0.1)
        return False, self.positions[motindex], self.moving[motindex]
    
    def get_pos_all(self):
        #oldtime = self.posTimestamps
        #for mot in self.names:
        #    self.commandschedule.append(["get_pos",mot])
        #threading.Thread(target=self.__executeJobsUntilEmpty).start() #call job runner in seperate thread
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
        for mot in self.channels:
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
                #elif comset[0] =="set_pos":
                #    self.__execute_setp(comset[1][0],comset[1][1])

                if not comset[0] == "stop": #allow fast stop shooting if necessary
                    time.sleep(self.serial.timeout)

                self.lock = False #remove lock
            else:
                time.sleep(0.5) #avoid dos attack if channel blocked


    
    def __execute_rel_move(self,mot,where):
        print("moving")
        message = self.__make_message("MR",mot,where)
        ans=''
        motindex = self.channels.index(mot)
        try:
            ans,err = self.__ReadWrite(message)
            #self.moving[motindex] = True
            # if "OK" in ans:
            #     self.positions[motindex] += where/self.stepsperunit[motindex]
            # else:
            #     print("error while moving")
            
        
        except Exception as exc:
            err = True
            print(exc)

        return err, ans

    def __execute_abs_move(self,mot,where):
        motindex = self.channels.index(mot)
        isposition = self.positions[motindex]*self.stepsperunit[motindex]
        print("moving to abs " + str(where) + " from " + str(isposition) + " on motor " + str(mot))
        where = where - isposition 

        message = self.__make_message("MR",mot,where)
        ans=''
        
        try:
            ans,err = self.__ReadWrite(message)

            if "OK" in ans:
                self.positions[motindex] = where/self.stepsperunit[motindex]
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
            ans = self.__ReadWrite(message)
            error = False
            print(ans)
        except Exception as exc:
            error = True
            print(exc)
        return error, ans
    
    def __execute_setp(self,mot,val): 
        message = self.__make_message('AP',mot,val)
        self.__ReadWrite(message)

    
    def __execute_position_call(self,mot):
        pos = self.positions
        message = self.__make_message("qp",mot,0)
        posstring, err = self.__ReadWrite(message)
        if not err:
            try:
                found = re.search('CP = (.+?)AP', posstring).group(1)
                found = found.strip()
            except Exception as e:
                # AAA, ZZZ not found in the original string
                print('Error in Read: ' + str(e))
                found = 'did not work' # apply your error handling
            avalue = found


            try:
                posval = float(found)
                posval/self.stepsperunit[motindex]
            except:
                posval = float('1')

            motindex = self.settings["steppers.names"].index(mot)
            if pos[motindex] == posval: # position is stable if no change between two calls
                self.moving[motindex] = 0


            print("position read: " + str(posval))
            self.positions[motindex] = posval/self.stepsperunit[motindex]
            self.posTimestamps[motindex] = time.time()

            # if oldpos == num:
            #     self.moving[motindex] = False
            # else: 
            #     self.moving[motindex] = True
        else:
            print("error getting position")





    # def __make_message(self,what,mot,where):
    #     message = []
    #     message.append("1WP"+"{0:0=4d}".format(mot) +'\r')

    #     where = round(where)
    #     if "M" in what:
    #         com = "1" + what + str(where) +"\r"
    #     else:
    #         com = "1" + what +"\r"
        
    #     message.append(com)
    #     return message

    def __make_message(self,Command,Motor,Data):
        acommand = str(Motor) + Command + str(Data) + '\r'
        return acommand
        # Command List:
        #qp = query positions
        #qs = query speed
        #ap = set actual positoin
        #sv = set velocity
        #ma = move absolute
        #mr = move relative

        


    def __ReadWrite(self,Command):
        #self.serial.open()
        print("attempting to write " + Command)
        
        # print(Command)
        #return 'OK#1', False
        try:
            self.serial.write(Command.encode())
            #self.serial.write(Command)
            #self.serial.write(Command)
            #print("written")
            output = ''
            while True:
                answer = self.serial.read()
                answer = answer.decode()

                if len(answer) == 0:
                    break
                output += answer
                # if "\r" in answer:
                #     break
            print("communication result" + output.strip())
            return output, False
        except Exception as e:
            print("Error while read/write: " + str(e))
            return '', True

    #helpers and conversion



    



    



