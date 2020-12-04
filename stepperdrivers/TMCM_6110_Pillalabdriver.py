'''
Created on 05.06.2020

@author: JM
reworked by Philipp Kagerer, exp. Physik VII
05.07.2020
change 3110 interface to accept 6 axis and motor selection
This module needs the PyTrinamic package, install using pip
"pip insall PyTrinamic"
Developed for PyTrinamicBeta Jun 19, 2020

'''

from PyTrinamic.connections.ConnectionManager import ConnectionManager
import numpy as np

class Stepper():
    MOTORS = 3

    def __init__(self, settings,initial=[0,0,0,0,0,0]):
        self.settings=settings
        print(settings)
        self.__set_settings()
        print("connecting steppers trinamic at"+ str(self.com))
        self.connectionManager = ConnectionManager(("--port=" + str(self.com)))
        connection = self.connectionManager.connect()
        self.connection = connection

        #self.GPs   = _GPs
        self.APs   = _APs
        #self.ENUMs = _ENUMs
        self.error = False
        self.__default_motor = 0
        self.moving = np.zeros(len(self.names),dtype=bool)

# ****************part for setting handling**********************
    def __set_settings(self):
        self.names = self.settings['steppers.names']
        #self.channels = self.settings['steppers.channels']
        self.com = self.settings["steppers.com"]
        self.stepsperunit = self.settings['steppers.stepsperunit']
        try:
            self.velocities = self.settings['steppers.velocities']
        except:
            self.velocities = [None,None,None,None,None,None]

        for i in range(len(self.stepsperunit)): #prevent 0 division error
            if self.stepsperunit[i] ==0:
                self.stepsperunit[i] = 1

#**********mapping of nomenclature on internal functions*************************
    def go_abs(self,mot,val):
        newstate = val
        try:
            val = int(round(val *(self.settings["steppers.stepsperunit"][mot])))
        except:
            return True, 0

        #motnm = self.channels[self.names.index(mot)]
        self.__default_motor = mot #set motor

        print("abs move requested")
        self.moveTo(val,self.velocities[mot])

        return False, 0

    def go_rel(self,mot,val):
        # print("there?")
        # print(mot)
        # motnm = self.channels[self.names.index(mot)]
        # print("here?")
        index = mot#self.names.index(mot)
        try:
            val = int(round(val *(self.settings["steppers.stepsperunit"][index])))
        except:
            return True, 0

        
 
        self.__default_motor = mot #set motor

        print("rel move requested")
        self.moveBy(val,self.velocities[index])

        return False, 0

    def go_abs_all(self,vals):
        if len(vals) == len(self.names):
            for i in range(len(vals)):
                try:
                    vals[i] = int(round(vals[i] *(self.settings["steppers.stepsperunit"][i])))
                    nonnumeric = False
                except:
                    nonnumeric = True
                if not nonnumeric:
                    motnm = self.names[i]
                    val = vals[i]#-self.positions[i]
                    self.__default_motor = motnm #set motor
                    self.moveTo(val,self.velocities[i])

        else:
            print("wrong motor selected " )
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
                    motnm = self.names[i]
                    val = vals[i]#-self.positions[i]
                    self.__default_motor = motnm #set motor
                    self.moveBy(val,self.velocities[i])

        else:
            print("wrong motor selected " )
        newstate = 0
        error = self.error
        return error, newstate
    
    def get_pos(self,mot):

        self.__default_motor = self.names[mot]
        pos = self.getActualPosition()
        pos = pos/self.stepsperunit[mot]
        return False,self.getActualPosition(),False
    
    def get_pos_all(self):
        vec = []
        for i in range(len(self.names)):
            motnm = self.names[i]
            self.__default_motor = motnm
            vec.append(self.getActualPosition()/self.stepsperunit[i])
        return False, vec, self.moving

    def set_pos(self,mot,newpos):
        self.__default_motor = self.names[mot]
        try:
            newpos = int(round(newpos *(self.settings["steppers.stepsperunit"][index])))
        except Exception as e:
            print("error setting trinamic position " + str(e))
            
        self.setActualPosition(newpos)

#*****************actual out in commands**************************
    # Pilla implemented methods
    def moveMotorTo(self,mot,position,velocity=None):
        self.__default_motor = mot
        self.moveTo(position,velocity)
    
    def configureSteppers(self,settings):
        #holding currents:
        hc_list = settings["steppers.holding_currents"]
        for i in range(len(hc_list)):
            mot = settings["steppers.names"][i]
            self.__default_motor = mot
            self.setMotorStandbyCurrent(hc_list[i])



    @staticmethod
    def getEdsFile():
        return __file__.replace("TMCM_3110.py", "TMCM_3110_V.320.eds")

    def showChipInfo(self):
        ("The TMCM-3110 is a 3-Axis Stepper Controller / Driver. Voltage supply: 12 - 48V");

    # Axis parameter access
    def getAxisParameter(self, apType):
        return self.connection.axisParameter(apType, self.__default_motor)

    def setAxisParameter(self, apType, value):
        self.connection.setAxisParameter(apType, self.__default_motor, value)

    # Global parameter access
    def getGlobalParameter(self, gpType, bank):
        return self.connection.globalParameter(gpType, bank)

    def setGlobalParameter(self, gpType, bank, value):
        self.connection.setGlobalParameter(gpType, bank, value)

    # Motion Control functions
    def rotate(self, velocity):
        self.setRampMode(2)

        self.setAxisParameter(self.APs.TargetVelocity, velocity)

    def stop(self):
        self.rotate(0)

    def moveTo(self, position, velocity=None):
        if velocity:
            self.setMaxVelocity(velocity)

        self.setTargetPosition(position)

        self.setRampMode(0)

    def moveBy(self, difference, velocity=None):
        position = difference + self.getActualPosition()

        self.moveTo(position, velocity)

        return position

    # Current control functions
    def setMotorRunCurrent(self, current):
        self.setMaxCurrent(current)

    def setMotorStandbyCurrent(self, current):
        self.setAxisParameter(self.APs.StandbyCurrent, current)

    def getMaxCurrent(self):
        return self.getAxisParameter(self.APs.MaxCurrent)

    def setMaxCurrent(self, current):
        self.setAxisParameter(self.APs.MaxCurrent, current)

    # StallGuard2 Functions
    def setStallguard2Filter(self, enableFilter):
        self.setAxisParameter(self.APs.SG2FilterEnable, enableFilter)

    def setStallguard2Threshold(self, threshold):
        self.setAxisParameter(self.APs.SG2Threshold, threshold)

    def setStopOnStallVelocity(self, velocity):
        self.setAxisParameter(self.APs.SmartEnergyStallVelocity, velocity)

    # Motion parameter functions
    def getTargetPosition(self):
        return self.getAxisParameter(self.APs.TargetPosition)

    def setTargetPosition(self, position):
        self.setAxisParameter(self.APs.TargetPosition, position)

    def getActualPosition(self):
        return self.getAxisParameter(self.APs.ActualPosition)

    def setActualPosition(self, position):
        return self.setAxisParameter(self.APs.ActualPosition, position)

    def getTargetVelocity(self):
        return self.getAxisParameter(self.APs.TargetVelocity)

    def setTargetVelocity(self, velocity):
        self.setAxisParameter(self.APs.TargetVelocity, velocity)

    def getActualVelocity(self):
        return self.getAxisParameter(self.APs.ActualVelocity)

    def getMaxVelocity(self):
        return self.getAxisParameter(self.APs.MaxVelocity)

    def setMaxVelocity(self, velocity):
        self.setAxisParameter(self.APs.MaxVelocity, velocity)

    def getMaxAcceleration(self):
        return self.getAxisParameter(self.APs.MaxAcceleration)

    def setMaxAcceleration(self, acceleration):
        self.setAxisParameter(self.APs.MaxAcceleration, acceleration)

    def getRampMode(self):
        return self.getAxisParameter(self.APs.RampMode)

    def setRampMode(self, mode):
        return self.setAxisParameter(self.APs.RampMode, mode)

    # Status functions
    def getStatusFlags(self):
        return self.getAxisParameter(self.APs.DrvStatusFlags)

    def getErrorFlags(self):
        return self.getAxisParameter(self.APs.ExtendedErrorFlags)

    def positionReached(self):
        return self.getAxisParameter(self.APs.PositionReachedFlag)

    # IO pin functions
    def analogInput(self, x):
        return self.connection.analogInput(x)

    def digitalInput(self, x):
        return self.connection.digitalInput(x)

class _APs():
    TargetPosition                 = 0
    ActualPosition                 = 1
    TargetVelocity                 = 2
    ActualVelocity                 = 3
    MaxVelocity                    = 4
    MaxAcceleration                = 5
    MaxCurrent                     = 6
    StandbyCurrent                 = 7
    PositionReachedFlag            = 8
    ReferenceSwitchStatus          = 9
    RightEndstop                   = 10
    LeftEndstop                    = 11
    RightLimitSwitchDisable        = 12
    LeftLimitSwitchDisable         = 13
    MinimumSpeed                   = 130
    ActualAcceleration             = 135
    RampMode                       = 138
    MicrostepResolution            = 140
    ReferenceSwitchTolerance       = 141
    SoftStopFlag                   = 149
    EndSwitchPowerDown             = 150
    RampDivisor                    = 153
    PulseDivisor                   = 154
    Intpol                         = 160
    DoubleEdgeSteps                = 161
    ChopperBlankTime               = 162
    ConstantTOffMode               = 163
    DisableFastDecayComparator     = 164
    ChopperHysteresisEnd           = 165
    ChopperHysteresisStart         = 166
    TOff                           = 167
    SEIMIN                         = 168
    SECDS                          = 169
    smartEnergyHysteresis          = 170
    SECUS                          = 171
    smartEnergyHysteresisStart     = 172
    SG2FilterEnable                = 173
    SG2Threshold                   = 174
    SlopeControlHighSide           = 175
    SlopeControlLowSide            = 176
    ShortToGroundProtection        = 177
    ShortDetectionTime             = 178
    VSense                         = 179
    smartEnergyActualCurrent       = 180
    smartEnergyStallVelocity       = 181
    smartEnergyThresholdSpeed      = 182
    smartEnergySlowRunCurrent      = 183
    RandomTOffMode                 = 184
    ReferenceSearchMode            = 193
    ReferenceSearchSpeed           = 194
    ReferenceSwitchSpeed           = 195
    ReferenceSwitchDistance        = 196
    LastReferenceSwitchPosition    = 197
    BoostCurrent                   = 200
    EncoderMode                    = 201
    FreewheelingDelay              = 204
    LoadValue                      = 206
    ExtendedErrorFlags             = 207
    DrvStatusFlags                 = 208
    EncoderPosition                = 209
    EncoderPrescaler               = 210
    MaxEncoderDeviation            = 212
    GroupIndex                     = 213
    PowerDownDelay                 = 214
    StepDirectionMode              = 254
    CurrentStepping                = 0