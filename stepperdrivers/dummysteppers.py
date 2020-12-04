import threading
import time
import numpy as np
class Stepper:
    def __init__(self,settings,initial=[0,0,0,0,0,0]):
        self.positions=initial
        self.moving = np.array(initial,dtype=bool)


        #open serial connection
        



    def go_abs(self,mot,val):
        try:
            val = int(round(val *(self.settings["steppers.stepsperunit"][mot])))
        except:
            return True, 0
        print("go abs " + str(val))
        self.positions[mot] = val
        newstate = self.positions
        error = False
        return error, newstate
    
    def go_abs_all(self,vals):
        print("go abs all " + str(vals))
        for i in range(len(vals)):
            self.positions[i] = vals[i]
        newstate = self.positions
        error = False
        return error, newstate

    def go_rel(self,mot,val):
        
        print("go rel " + str(val))
        mt = threading.Thread(target=self.go_rel_countup)
        self.tempmot=mot
        self.tempval=val
        mt.start()
        newstate = self.positions
        error = False
        return error, newstate

    def go_rel_countup(self):
        steps = 200
        mot = self.tempmot
        val = self.tempval
        for i in range(steps):
            self.positions[mot] += val/steps
            time.sleep(0.1)

    def go_rel_all(self,vals):
        print("go rel all " + str(vals))
        for i in range(len(vals)):
            self.positions[i] += vals[i]
        newstate = self.positions
        error = False
        return error, newstate

    def set_pos(self,mot,val=0): #set current motor setpoint and return it
        self.positions[mot] = val
    
    def setp_pos_all(self,vals): # set all motor setpoints and return them
        for i in range(len(vals)):
            self.positions[i] = vals[i]
    
    def get_pos(self,mot):

        return False, self.positions[mot], False

    
    def get_pos_all(self):
        return False, self.positions, self.moving

    
    def stop_all(self):
        print("stopping")






    





    







        
