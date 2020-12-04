#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jseltmann
"""

class PID:
    """
    Discrete PID control
    """
    
    def __init__(self, P=2.0, I=0.0, D=1.0, Previous=0, Integrator=0, Integrator_max=500, Integrator_min=-500):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.Previous=Previous
        self.Integrator=Integrator
        self.Integrator_max=Integrator_max
        self.Integrator_min=Integrator_min
        
        self.P_value=0.0
        self.I_value=0.0
        self.D_value=0.0
        self.set_point=0.0
        self.error=0.0

    def update(self, current_diff, dt=1.0):
        """
        Calculate PID output value for given difference
        """

        self.error = current_diff
        self.P_value = self.Kp * self.error
        self.Integrator += (self.error + self.Previous)*dt/2
        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min
        self.I_value = self.Integrator * self.Ki
        
        self.D_value = self.Kd * (self.error - self.Previous)/dt
        self.Previous = self.error
        #print ('P: ' + str(self.P_value)  + '\tI: ' + str(self.I_value) + '\tD: ' + str(self.D_value))
        PID = self.P_value + self.I_value + self.D_value

        return (self.P_value, self.I_value, self.D_value)#PID
        
    def resetIntegrator(self):
        self.Integrator = 0
    
    def setKp(self,P):
        self.Kp=P
    
    def setKi(self,I):
        self.Ki=I
    
    def setKd(self,D):
        self.Kd=D
        
    def getP(self):
        return self.P_value
        
    def getI(self):
        return self.I_value

    def getD(self):
        return self.D_value

        
