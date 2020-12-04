'''
PillaLab adaption of the MEKA Drivers for HXP-hexapod
adaptions:
    create a wrapper class, to make this appear as a normal Stepperdriver
    Use three sockets to run, read, stop
    Each socket is running a Thread, which is taking the commands and communicating them
    This will avoid overloading of the sockets, as well as program hanging

    The Threading/wait structure works with threading events like:
    https://blog.miguelgrinberg.com/post/how-to-make-python-wait

'''

import threading
import numpy as np

class Stepper:
    def __init__(self,settings,initial=[0,0,0,0,0,0]):

        # ********** set settings and options ***************************
        self.settings = settings
        self.group = 'HEXAPOD'

        # ********** set flags and states *******************************
        self.moving = False             # referer, whether the Hexapod is moving
        self.positions = initial        # current Hexa position
        self.hxpActive = True           # Flag to end Hexamqueues from running

        # ********** initialize the three XPS Channels ******************
        self.myxps = XPS()
        self.MoveConnID = self.myxps.TCP_ConnectToServer(self.settings["steppers.com"], 5001, 20) # socket for movement

        [errorCode, returnString] = self.myxps.GroupKill(self.MoveConnID, group)
        [errorCode, returnString] = self.myxps.TCLScriptExecuteAndWait(self.MoveConnID,'InitializeFromRegistration.tcl','HexaIniFromPython','')

        self.mycheckxps = XPS()
        self.CheckConnID = self.mycheckxps.TCP_ConnectToServer(self.settings["steppers.com"], 5001, 20) # socket for position check

        self.mystopxps = XPS()
        self.StopConnID = self.mycheckxps.TCP_ConnectToServer(self.settings["steppers.com"], 5001, 20) # socket for stop

        # *********** define three queues for movement, check, stop********
        self.movreqlist = []                    # one sided event structure
        self.moveevent = threading.Event()
        self.checkreqlist = []                  # two sided event structure through two events for synchronous pos request
        self.checkevent = threading.Event()
        self.stopreqlist = []
        self.stopevent = threading.Event()

    def movwatcher(self):
        while self.hxpActive:                   # infinity loop
            self.moveevent.wait(timeout=2)      # efficient way of waiting for an event
            while not self.movreqlist==[]:
                com = self.movreqlist.pop(0)    # take first element in list
                command = com[0]                # command text
                vec = com[1]                    # positioning vector
                print(com)
                if command == 'move_abs':
                    self.MoveHexa(vec)
                elif command == 'move_rel':
                    self.MoveHexaRel(vec)
                else:
                    print('Hexa move unknown command!')
    
    def checkwatcher(self):
        while self.hxpActive:                   # infinity loop
            self.checkevent.wait(timeout=2)      # efficient way of waiting for an event





    def shutdown(self):
        self.hxpActive = False

    def move_abs(self,mot,pos):
        movevec = np.zeros(6)
        movevec[mot] = pos

        self.movreqlist.append(['move_abs',movevec])
        self.moveevent.set()

    
    def MoveHexa(self,whereto):
        self.moving = True
        [errorCode, returnString] = self.myxps.HexapodMoveAbsolute(self.MoveConnID,self.group,'Work',whereto)
        [errorCode2, returnString] = self.myxps.TCLScriptExecuteAndWait(self.MoveConnID,'BackupPosition.tcl','HexaBackupFromPython','')
        self.moving = False
        return errorCode

    def MoveHexaRel(self,whereto,sys='Work'):
        self.moving = True
        # [errorCode, returnString] = self.myxps.GroupMoveRelativeInSystem(self.MoveConnID,self.group,whereto)
        [errorCode, returnString] = self.myxps.HexapodMoveIncremental(self.MoveConnID,self.group,sys,whereto)
        [errorCode2, returnString2] = self.myxps.TCLScriptExecuteAndWait(self.MoveConnID,'BackupPosition.tcl','HexaBackupFromPython','')
        self.moving = False
        return errorCode
        

# XPS Python class
#
#  for HXP Firmware V1.3.x
#
#  See Programmer's manual for more information on XPS function calls

import socket


class XPS:
    # Defines
    MAX_NB_SOCKETS = 100

    # Global variables
    __sockets = {}
    __usedSockets = {}
    __nbSockets = 0

    # Initialization Function
    def __init__ (self):
        XPS.__nbSockets = 0
        for socketId in range(self.MAX_NB_SOCKETS):
            XPS.__usedSockets[socketId] = 0

    # Send command and get return
    def __sendAndReceive (self, socketId, command):
        try:
            XPS.__sockets[socketId].send(command)
            ret = XPS.__sockets[socketId].recv(1024)
            while (ret.find(',EndOfAPI') == -1):
                ret += XPS.__sockets[socketId].recv(1024)
        except socket.timeout:
            return [-2, '']
        except socket.error: #(errNb, errString):
            print('Socket error : ' )#+ errString)
            return [-2, '']

        for i in range(len(ret)):
            if (ret[i] == ','):
                return [int(ret[0:i]), ret[i+1:-9]]

    # TCP_ConnectToServer
    def TCP_ConnectToServer (self, IP, port, timeOut):
        socketId = 0
        if (XPS.__nbSockets < self.MAX_NB_SOCKETS):
            while (XPS.__usedSockets[socketId] == 1 and socketId < self.MAX_NB_SOCKETS):
                socketId += 1
            if (socketId == self.MAX_NB_SOCKETS):
                return -1
        else:
            return -1

        XPS.__usedSockets[socketId] = 1
        XPS.__nbSockets += 1
        try:
            XPS.__sockets[socketId] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            XPS.__sockets[socketId].connect((IP, port))
            XPS.__sockets[socketId].settimeout(timeOut)
            XPS.__sockets[socketId].setblocking(1)
        except socket.error:
            return -1

        return socketId

    # TCP_SetTimeout
    def TCP_SetTimeout (self, socketId, timeOut):
        if (XPS.__usedSockets[socketId] == 1):
            XPS.__sockets[socketId].settimeout(timeOut)

    # TCP_CloseSocket
    def TCP_CloseSocket (self, socketId):
        if (socketId >= 0 and socketId < self.MAX_NB_SOCKETS):
            try:
                XPS.__sockets[socketId].close()
                XPS.__usedSockets[socketId] = 0
                XPS.__nbSockets -= 1
            except socket.error:
                pass

    # GetLibraryVersion
    def GetLibraryVersion (self):
        return ['HXP Firmware V1.3.x']

    # ControllerMotionKernelTimeLoadGet :  Get controller motion kernel time load
    def ControllerMotionKernelTimeLoadGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'ControllerMotionKernelTimeLoadGet(double *,double *,double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(4):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # ElapsedTimeGet :  Return elapsed time from controller power on
    def ElapsedTimeGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'ElapsedTimeGet(double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
            j += 1
        retList.append(eval(returnedString[i:i+j]))

        return retList


    # ErrorStringGet :  Return the error string corresponding to the error code
    def ErrorStringGet (self, socketId, ErrorCode):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'ErrorStringGet(' + str(ErrorCode) + ',char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # FirmwareVersionGet :  Return firmware version
    def FirmwareVersionGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'FirmwareVersionGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # TCLScriptExecute :  Execute a TCL script from a TCL file
    def TCLScriptExecute (self, socketId, TCLFileName, TaskName, ParametersList):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'TCLScriptExecute(' + TCLFileName + ',' + TaskName + ',' + ParametersList + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # TCLScriptExecuteAndWait :  Execute a TCL script from a TCL file and wait the end of execution to return
    def TCLScriptExecuteAndWait (self, socketId, TCLFileName, TaskName, InputParametersList):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'TCLScriptExecuteAndWait(' + TCLFileName + ',' + TaskName + ',' + InputParametersList + ',char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # TCLScriptKill :  Kill TCL Task
    def TCLScriptKill (self, socketId, TaskName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'TCLScriptKill(' + TaskName + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # TimerGet :  Get a timer
    def TimerGet (self, socketId, TimerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'TimerGet(' + TimerName + ',int *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
            j += 1
        retList.append(eval(returnedString[i:i+j]))

        return retList


    # TimerSet :  Set a timer
    def TimerSet (self, socketId, TimerName, FrequencyTicks):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'TimerSet(' + TimerName + ',' + str(FrequencyTicks) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # Reboot :  Reboot the controller
    def Reboot (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'Reboot()'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # Login :  Log in
    def Login (self, socketId, Name, Password):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'Login(' + Name + ',' + Password + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # CloseAllOtherSockets :  Close all socket beside the one used to send this command
    def CloseAllOtherSockets (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'CloseAllOtherSockets()'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EventAdd :  ** OBSOLETE ** Add an event
    def EventAdd (self, socketId, PositionerName, EventName, EventParameter, ActionName, ActionParameter1, ActionParameter2, ActionParameter3):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EventAdd(' + PositionerName + ',' + EventName + ',' + EventParameter + ',' + ActionName + ',' + ActionParameter1 + ',' + ActionParameter2 + ',' + ActionParameter3 + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EventGet :  ** OBSOLETE ** Read events and actions list
    def EventGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EventGet(' + PositionerName + ',char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EventRemove :  ** OBSOLETE ** Delete an event
    def EventRemove (self, socketId, PositionerName, EventName, EventParameter):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EventRemove(' + PositionerName + ',' + EventName + ',' + EventParameter + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EventWait :  ** OBSOLETE ** Wait an event
    def EventWait (self, socketId, PositionerName, EventName, EventParameter):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EventWait(' + PositionerName + ',' + EventName + ',' + EventParameter + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EventExtendedConfigurationTriggerSet :  Configure one or several events
    def EventExtendedConfigurationTriggerSet (self, socketId, ExtendedEventName, EventParameter1, EventParameter2, EventParameter3, EventParameter4):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EventExtendedConfigurationTriggerSet('
        for i in range(len(ExtendedEventName)):
            if (i > 0):
                command += ','
            command += ExtendedEventName[i] + ',' + EventParameter1[i] + ',' + EventParameter2[i] + ',' + EventParameter3[i] + ',' + EventParameter4[i]
        command += ')'

        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EventExtendedConfigurationTriggerGet :  Read the event configuration
    def EventExtendedConfigurationTriggerGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EventExtendedConfigurationTriggerGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EventExtendedConfigurationActionSet :  Configure one or several actions
    def EventExtendedConfigurationActionSet (self, socketId, ExtendedActionName, ActionParameter1, ActionParameter2, ActionParameter3, ActionParameter4):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EventExtendedConfigurationActionSet('
        for i in range(len(ExtendedActionName)):
            if (i > 0):
                command += ','
            command += ExtendedActionName[i] + ',' + ActionParameter1[i] + ',' + ActionParameter2[i] + ',' + ActionParameter3[i] + ',' + ActionParameter4[i]
        command += ')'

        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EventExtendedConfigurationActionGet :  Read the action configuration
    def EventExtendedConfigurationActionGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EventExtendedConfigurationActionGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EventExtendedStart :  Launch the last event and action configuration and return an ID
    def EventExtendedStart (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EventExtendedStart(int *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
            j += 1
        retList.append(eval(returnedString[i:i+j]))

        return retList


    # EventExtendedAllGet :  Read all event and action configurations
    def EventExtendedAllGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EventExtendedAllGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EventExtendedGet :  Read the event and action configuration defined by ID
    def EventExtendedGet (self, socketId, ID):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EventExtendedGet(' + str(ID) + ',char *,char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EventExtendedRemove :  Remove the event and action configuration defined by ID
    def EventExtendedRemove (self, socketId, ID):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EventExtendedRemove(' + str(ID) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EventExtendedWait :  Wait events from the last event configuration
    def EventExtendedWait (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EventExtendedWait()'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GatheringConfigurationGet :  Read different mnemonique type
    def GatheringConfigurationGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringConfigurationGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GatheringConfigurationSet :  Configuration acquisition
    def GatheringConfigurationSet (self, socketId, Type):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringConfigurationSet('
        for i in range(len(Type)):
            if (i > 0):
                command += ','
            command += Type[i]
        command += ')'

        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GatheringCurrentNumberGet :  Maximum number of samples and current number during acquisition
    def GatheringCurrentNumberGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringCurrentNumberGet(int *,int *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(2):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # GatheringStopAndSave :  Stop acquisition and save data
    def GatheringStopAndSave (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringStopAndSave()'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GatheringDataAcquire :  Acquire a configured data
    def GatheringDataAcquire (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringDataAcquire()'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GatheringDataGet :  Get a data line from gathering buffer
    def GatheringDataGet (self, socketId, IndexPoint):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringDataGet(' + str(IndexPoint) + ',char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GatheringReset :  Empty the gathered data in memory to start new gathering from scratch
    def GatheringReset (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringReset()'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GatheringRun :  Start a new gathering
    def GatheringRun (self, socketId, DataNumber, Divisor):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringRun(' + str(DataNumber) + ',' + str(Divisor) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GatheringStop :  Stop the data gathering (without saving to file)
    def GatheringStop (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringStop()'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GatheringExternalConfigurationSet :  Configuration acquisition
    def GatheringExternalConfigurationSet (self, socketId, Type):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringExternalConfigurationSet('
        for i in range(len(Type)):
            if (i > 0):
                command += ','
            command += Type[i]
        command += ')'

        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GatheringExternalConfigurationGet :  Read different mnemonique type
    def GatheringExternalConfigurationGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringExternalConfigurationGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GatheringExternalCurrentNumberGet :  Maximum number of samples and current number during acquisition
    def GatheringExternalCurrentNumberGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringExternalCurrentNumberGet(int *,int *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(2):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # GatheringExternalStopAndSave :  Stop acquisition and save data
    def GatheringExternalStopAndSave (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringExternalStopAndSave()'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GlobalArrayGet :  Get global array value
    def GlobalArrayGet (self, socketId, Number):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GlobalArrayGet(' + str(Number) + ',char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GlobalArraySet :  Set global array value
    def GlobalArraySet (self, socketId, Number, ValueString):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GlobalArraySet(' + str(Number) + ',' + ValueString + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # DoubleGlobalArrayGet :  Get double global array value
    def DoubleGlobalArrayGet (self, socketId, Number):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'DoubleGlobalArrayGet(' + str(Number) + ',double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
            j += 1
        retList.append(eval(returnedString[i:i+j]))

        return retList


    # DoubleGlobalArraySet :  Set double global array value
    def DoubleGlobalArraySet (self, socketId, Number, DoubleValue):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'DoubleGlobalArraySet(' + str(Number) + ',' + str(DoubleValue) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GPIOAnalogGet :  Read analog input or analog output for one or few input
    def GPIOAnalogGet (self, socketId, GPIOName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GPIOAnalogGet('
        for i in range(len(GPIOName)):
            if (i > 0):
                command += ','
            command += GPIOName[i] + ',' + 'double *'
        command += ')'

        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(len(GPIOName)):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # GPIOAnalogSet :  Set analog output for one or few output
    def GPIOAnalogSet (self, socketId, GPIOName, AnalogOutputValue):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GPIOAnalogSet('
        for i in range(len(GPIOName)):
            if (i > 0):
                command += ','
            command += GPIOName[i] + ',' + str(AnalogOutputValue[i])
        command += ')'

        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GPIOAnalogGainGet :  Read analog input gain (1, 2, 4 or 8) for one or few input
    def GPIOAnalogGainGet (self, socketId, GPIOName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GPIOAnalogGainGet('
        for i in range(len(GPIOName)):
            if (i > 0):
                command += ','
            command += GPIOName[i] + ',' + 'int *'
        command += ')'

        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(len(GPIOName)):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # GPIOAnalogGainSet :  Set analog input gain (1, 2, 4 or 8) for one or few input
    def GPIOAnalogGainSet (self, socketId, GPIOName, AnalogInputGainValue):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GPIOAnalogGainSet('
        for i in range(len(GPIOName)):
            if (i > 0):
                command += ','
            command += GPIOName[i] + ',' + str(AnalogInputGainValue[i])
        command += ')'

        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GPIODigitalGet :  Read digital output or digital input 
    def GPIODigitalGet (self, socketId, GPIOName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GPIODigitalGet(' + GPIOName + ',unsigned short *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
            j += 1
        retList.append(eval(returnedString[i:i+j]))

        return retList


    # GPIODigitalSet :  Set Digital Output for one or few output TTL
    def GPIODigitalSet (self, socketId, GPIOName, Mask, DigitalOutputValue):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GPIODigitalSet(' + GPIOName + ',' + str(Mask) + ',' + str(DigitalOutputValue) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GroupCorrectorOutputGet :  Return corrector outputs
    def GroupCorrectorOutputGet (self, socketId, GroupName, nbElement):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupCorrectorOutputGet(' + GroupName + ','
        for i in range(nbElement):
            if (i > 0):
                command += ','
            command += 'double *'
        command += ')'

        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(nbElement):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # GroupHomeSearch :  Start home search sequence
    def GroupHomeSearch (self, socketId, GroupName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupHomeSearch(' + GroupName + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GroupHomeSearchAndRelativeMove :  Start home search sequence and execute a displacement
    def GroupHomeSearchAndRelativeMove (self, socketId, GroupName, TargetDisplacement):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupHomeSearchAndRelativeMove(' + GroupName + ','
        for i in range(len(TargetDisplacement)):
            if (i > 0):
                command += ','
            command += str(TargetDisplacement[i])
        command += ')'

        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GroupInitialize :  Start the initialization
    def GroupInitialize (self, socketId, GroupName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupInitialize(' + GroupName + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GroupInitializeWithEncoderCalibration :  Start the initialization with encoder calibration
    def GroupInitializeWithEncoderCalibration (self, socketId, GroupName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupInitializeWithEncoderCalibration(' + GroupName + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GroupKill :  Kill the group
    def GroupKill (self, socketId, GroupName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupKill(' + GroupName + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GroupMoveAbort :  Abort a move
    def GroupMoveAbort (self, socketId, GroupName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupMoveAbort(' + GroupName + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GroupMoveAbsolute :  Do an absolute move
    def GroupMoveAbsolute (self, socketId, GroupName, TargetPosition):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupMoveAbsolute(' + GroupName + ','
        for i in range(len(TargetPosition)):
            if (i > 0):
                command += ','
            command += str(TargetPosition[i])
        command += ')'

        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GroupMoveRelative :  Do a relative move
    
    def GroupMoveRelative (self, socketId, GroupName, TargetDisplacement):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupMoveRelative(' + GroupName + ','
        for i in range(len(TargetDisplacement)):
            if (i > 0):
                command += ','
            command += str(TargetDisplacement[i])
        command += ')'

        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GroupMotionDisable :  Set Motion disable on selected group
    def GroupMotionDisable (self, socketId, GroupName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupMotionDisable(' + GroupName + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GroupMotionEnable :  Set Motion enable on selected group
    def GroupMotionEnable (self, socketId, GroupName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupMotionEnable(' + GroupName + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GroupPositionCorrectedProfilerGet :  Return corrected profiler positions
    def GroupPositionCorrectedProfilerGet (self, socketId, GroupName, PositionX, PositionY):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupPositionCorrectedProfilerGet(' + GroupName + ',' + str(PositionX) + ',' + str(PositionY) + ',double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(2):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # GroupPositionCurrentGet :  Return current positions
    def GroupPositionCurrentGet (self, socketId, GroupName, nbElement):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupPositionCurrentGet(' + GroupName + ','
        for i in range(nbElement):
            if (i > 0):
                command += ','
            command += 'double *'
        command += ')'

        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(nbElement):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # GroupPositionSetpointGet :  Return setpoint positions
    def GroupPositionSetpointGet (self, socketId, GroupName, nbElement):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupPositionSetpointGet(' + GroupName + ','
        for i in range(nbElement):
            if (i > 0):
                command += ','
            command += 'double *'
        command += ')'

        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(nbElement):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # GroupPositionTargetGet :  Return target positions
    def GroupPositionTargetGet (self, socketId, GroupName, nbElement):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupPositionTargetGet(' + GroupName + ','
        for i in range(nbElement):
            if (i > 0):
                command += ','
            command += 'double *'
        command += ')'

        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(nbElement):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # GroupStatusGet :  Return group status
    def GroupStatusGet (self, socketId, GroupName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupStatusGet(' + GroupName + ',int *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
            j += 1
        retList.append(eval(returnedString[i:i+j]))

        return retList


    # GroupStatusStringGet :  Return the group status string corresponding to the group status code
    def GroupStatusStringGet (self, socketId, GroupStatusCode):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupStatusStringGet(' + str(GroupStatusCode) + ',char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # KillAll :  Put all groups in 'Not initialized' state
    def KillAll (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'KillAll()'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # RestartApplication :  Restart the Controller
    def RestartApplication (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'RestartApplication()'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerBacklashGet :  Read backlash value and status
    def PositionerBacklashGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerBacklashGet(' + PositionerName + ',double *,char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(2):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # PositionerBacklashSet :  Set backlash value
    def PositionerBacklashSet (self, socketId, PositionerName, BacklashValue):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerBacklashSet(' + PositionerName + ',' + str(BacklashValue) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerBacklashEnable :  Enable the backlash
    def PositionerBacklashEnable (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerBacklashEnable(' + PositionerName + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerBacklashDisable :  Disable the backlash
    def PositionerBacklashDisable (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerBacklashDisable(' + PositionerName + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerCorrectorNotchFiltersSet :  Update filters parameters 
    def PositionerCorrectorNotchFiltersSet (self, socketId, PositionerName, NotchFrequency1, NotchBandwith1, NotchGain1, NotchFrequency2, NotchBandwith2, NotchGain2):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerCorrectorNotchFiltersSet(' + PositionerName + ',' + str(NotchFrequency1) + ',' + str(NotchBandwith1) + ',' + str(NotchGain1) + ',' + str(NotchFrequency2) + ',' + str(NotchBandwith2) + ',' + str(NotchGain2) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerCorrectorNotchFiltersGet :  Read filters parameters 
    def PositionerCorrectorNotchFiltersGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerCorrectorNotchFiltersGet(' + PositionerName + ',double *,double *,double *,double *,double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(6):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # PositionerCorrectorPIDFFAccelerationSet :  Update corrector parameters
    def PositionerCorrectorPIDFFAccelerationSet (self, socketId, PositionerName, ClosedLoopStatus, KP, KI, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, FeedForwardGainAcceleration):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerCorrectorPIDFFAccelerationSet(' + PositionerName + ',' + str(ClosedLoopStatus) + ',' + str(KP) + ',' + str(KI) + ',' + str(KD) + ',' + str(KS) + ',' + str(IntegrationTime) + ',' + str(DerivativeFilterCutOffFrequency) + ',' + str(GKP) + ',' + str(GKI) + ',' + str(GKD) + ',' + str(KForm) + ',' + str(FeedForwardGainAcceleration) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerCorrectorPIDFFAccelerationGet :  Read corrector parameters
    def PositionerCorrectorPIDFFAccelerationGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerCorrectorPIDFFAccelerationGet(' + PositionerName + ',bool *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(12):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # PositionerCorrectorPIDFFVelocitySet :  Update corrector parameters
    def PositionerCorrectorPIDFFVelocitySet (self, socketId, PositionerName, ClosedLoopStatus, KP, KI, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, FeedForwardGainVelocity):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerCorrectorPIDFFVelocitySet(' + PositionerName + ',' + str(ClosedLoopStatus) + ',' + str(KP) + ',' + str(KI) + ',' + str(KD) + ',' + str(KS) + ',' + str(IntegrationTime) + ',' + str(DerivativeFilterCutOffFrequency) + ',' + str(GKP) + ',' + str(GKI) + ',' + str(GKD) + ',' + str(KForm) + ',' + str(FeedForwardGainVelocity) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerCorrectorPIDFFVelocityGet :  Read corrector parameters
    def PositionerCorrectorPIDFFVelocityGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerCorrectorPIDFFVelocityGet(' + PositionerName + ',bool *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(12):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # PositionerCorrectorPIDDualFFVoltageSet :  Update corrector parameters
    def PositionerCorrectorPIDDualFFVoltageSet (self, socketId, PositionerName, ClosedLoopStatus, KP, KI, KD, KS, IntegrationTime, DerivativeFilterCutOffFrequency, GKP, GKI, GKD, KForm, FeedForwardGainVelocity, FeedForwardGainAcceleration, Friction):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerCorrectorPIDDualFFVoltageSet(' + PositionerName + ',' + str(ClosedLoopStatus) + ',' + str(KP) + ',' + str(KI) + ',' + str(KD) + ',' + str(KS) + ',' + str(IntegrationTime) + ',' + str(DerivativeFilterCutOffFrequency) + ',' + str(GKP) + ',' + str(GKI) + ',' + str(GKD) + ',' + str(KForm) + ',' + str(FeedForwardGainVelocity) + ',' + str(FeedForwardGainAcceleration) + ',' + str(Friction) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerCorrectorPIDDualFFVoltageGet :  Read corrector parameters
    def PositionerCorrectorPIDDualFFVoltageGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerCorrectorPIDDualFFVoltageGet(' + PositionerName + ',bool *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(14):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # PositionerCorrectorPIPositionSet :  Update corrector parameters
    def PositionerCorrectorPIPositionSet (self, socketId, PositionerName, ClosedLoopStatus, KP, KI, IntegrationTime):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerCorrectorPIPositionSet(' + PositionerName + ',' + str(ClosedLoopStatus) + ',' + str(KP) + ',' + str(KI) + ',' + str(IntegrationTime) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerCorrectorPIPositionGet :  Read corrector parameters
    def PositionerCorrectorPIPositionGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerCorrectorPIPositionGet(' + PositionerName + ',bool *,double *,double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(4):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # PositionerCorrectorTypeGet :  Read corrector type
    def PositionerCorrectorTypeGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerCorrectorTypeGet(' + PositionerName + ',char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerCurrentVelocityAccelerationFiltersSet :  Set current velocity and acceleration cut off frequencies
    def PositionerCurrentVelocityAccelerationFiltersSet (self, socketId, PositionerName, CurrentVelocityCutOffFrequency, CurrentAccelerationCutOffFrequency):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerCurrentVelocityAccelerationFiltersSet(' + PositionerName + ',' + str(CurrentVelocityCutOffFrequency) + ',' + str(CurrentAccelerationCutOffFrequency) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerCurrentVelocityAccelerationFiltersGet :  Get current velocity and acceleration cut off frequencies
    def PositionerCurrentVelocityAccelerationFiltersGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerCurrentVelocityAccelerationFiltersGet(' + PositionerName + ',double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(2):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # PositionerDriverStatusGet :  Read positioner driver status
    def PositionerDriverStatusGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerDriverStatusGet(' + PositionerName + ',int *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
            j += 1
        retList.append(eval(returnedString[i:i+j]))

        return retList


    # PositionerDriverStatusStringGet :  Return the positioner driver status string corresponding to the positioner error code
    def PositionerDriverStatusStringGet (self, socketId, PositionerDriverStatus):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerDriverStatusStringGet(' + str(PositionerDriverStatus) + ',char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerEncoderAmplitudeValuesGet :  Read analog interpolated encoder amplitude values
    def PositionerEncoderAmplitudeValuesGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerEncoderAmplitudeValuesGet(' + PositionerName + ',double *,double *,double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(4):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # PositionerEncoderCalibrationParametersGet :  Read analog interpolated encoder calibration parameters
    def PositionerEncoderCalibrationParametersGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerEncoderCalibrationParametersGet(' + PositionerName + ',double *,double *,double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(4):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # PositionerErrorGet :  Read and clear positioner error code
    def PositionerErrorGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerErrorGet(' + PositionerName + ',int *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
            j += 1
        retList.append(eval(returnedString[i:i+j]))

        return retList


    # PositionerErrorRead :  Read only positioner error code without clear it
    def PositionerErrorRead (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerErrorRead(' + PositionerName + ',int *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
            j += 1
        retList.append(eval(returnedString[i:i+j]))

        return retList


    # PositionerErrorStringGet :  Return the positioner status string corresponding to the positioner error code
    def PositionerErrorStringGet (self, socketId, PositionerErrorCode):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerErrorStringGet(' + str(PositionerErrorCode) + ',char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerHardwareStatusGet :  Read positioner hardware status
    def PositionerHardwareStatusGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerHardwareStatusGet(' + PositionerName + ',int *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
            j += 1
        retList.append(eval(returnedString[i:i+j]))

        return retList


    # PositionerHardwareStatusStringGet :  Return the positioner hardware status string corresponding to the positioner error code
    def PositionerHardwareStatusStringGet (self, socketId, PositionerHardwareStatus):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerHardwareStatusStringGet(' + str(PositionerHardwareStatus) + ',char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerHardInterpolatorFactorGet :  Get hard interpolator parameters
    def PositionerHardInterpolatorFactorGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerHardInterpolatorFactorGet(' + PositionerName + ',int *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
            j += 1
        retList.append(eval(returnedString[i:i+j]))

        return retList


    # PositionerHardInterpolatorFactorSet :  Set hard interpolator parameters
    def PositionerHardInterpolatorFactorSet (self, socketId, PositionerName, InterpolationFactor):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerHardInterpolatorFactorSet(' + PositionerName + ',' + str(InterpolationFactor) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerMaximumVelocityAndAccelerationGet :  Return maximum velocity and acceleration of the positioner
    def PositionerMaximumVelocityAndAccelerationGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerMaximumVelocityAndAccelerationGet(' + PositionerName + ',double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(2):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # PositionerMotionDoneGet :  Read motion done parameters
    def PositionerMotionDoneGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerMotionDoneGet(' + PositionerName + ',double *,double *,double *,double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(5):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # PositionerMotionDoneSet :  Update motion done parameters
    def PositionerMotionDoneSet (self, socketId, PositionerName, PositionWindow, VelocityWindow, CheckingTime, MeanPeriod, TimeOut):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerMotionDoneSet(' + PositionerName + ',' + str(PositionWindow) + ',' + str(VelocityWindow) + ',' + str(CheckingTime) + ',' + str(MeanPeriod) + ',' + str(TimeOut) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerSGammaExactVelocityAjustedDisplacementGet :  Return adjusted displacement to get exact velocity
    def PositionerSGammaExactVelocityAjustedDisplacementGet (self, socketId, PositionerName, DesiredDisplacement):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerSGammaExactVelocityAjustedDisplacementGet(' + PositionerName + ',' + str(DesiredDisplacement) + ',double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
            j += 1
        retList.append(eval(returnedString[i:i+j]))

        return retList


    # PositionerSGammaParametersGet :  Read dynamic parameters for one axe of a group for a future displacement 
    def PositionerSGammaParametersGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerSGammaParametersGet(' + PositionerName + ',double *,double *,double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(4):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # PositionerSGammaParametersSet :  Update dynamic parameters for one axe of a group for a future displacement
    def PositionerSGammaParametersSet (self, socketId, PositionerName, Velocity, Acceleration, MinimumTjerkTime, MaximumTjerkTime):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerSGammaParametersSet(' + PositionerName + ',' + str(Velocity) + ',' + str(Acceleration) + ',' + str(MinimumTjerkTime) + ',' + str(MaximumTjerkTime) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerSGammaPreviousMotionTimesGet :  Read SettingTime and SettlingTime
    def PositionerSGammaPreviousMotionTimesGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerSGammaPreviousMotionTimesGet(' + PositionerName + ',double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(2):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # PositionerStageParameterGet :  Return the stage parameter
    def PositionerStageParameterGet (self, socketId, PositionerName, ParameterName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerStageParameterGet(' + PositionerName + ',' + ParameterName + ',char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerStageParameterSet :  Save the stage parameter
    def PositionerStageParameterSet (self, socketId, PositionerName, ParameterName, ParameterValue):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerStageParameterSet(' + PositionerName + ',' + ParameterName + ',' + ParameterValue + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerUserTravelLimitsGet :  Read UserMinimumTarget and UserMaximumTarget
    def PositionerUserTravelLimitsGet (self, socketId, PositionerName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerUserTravelLimitsGet(' + PositionerName + ',double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(2):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # PositionerUserTravelLimitsSet :  Update UserMinimumTarget and UserMaximumTarget
    def PositionerUserTravelLimitsSet (self, socketId, PositionerName, UserMinimumTarget, UserMaximumTarget):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerUserTravelLimitsSet(' + PositionerName + ',' + str(UserMinimumTarget) + ',' + str(UserMaximumTarget) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # HexapodMoveAbsolute :  Hexapod absolute move in a specific coordinate system
    def HexapodMoveAbsolute (self, socketId, GroupName, CoordinateSystem, pos):
        X = pos[0] 
        Y = pos[1] 
        Z = pos[2] 
        U = pos[3]
        V = pos[4] 
        W = pos[5] 
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'HexapodMoveAbsolute(' + GroupName + ',' + CoordinateSystem + ',' + str(X) + ',' + str(Y) + ',' + str(Z) + ',' + str(U) + ',' + str(V) + ',' + str(W) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]
        
        # HexapodMoveAbsolute :  Hexapod absolute move in a specific coordinate system
    def HexapodMoveAbsoluteold (self, socketId, GroupName, CoordinateSystem, X, Y, Z, U, V, W):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'HexapodMoveAbsolute(' + GroupName + ',' + CoordinateSystem + ',' + str(X) + ',' + str(Y) + ',' + str(Z) + ',' + str(U) + ',' + str(V) + ',' + str(W) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]

    # HexapodMoveIncremental :  Hexapod incremental move in a specific coordinate system
    def HexapodMoveIncremental (self, socketId, GroupName, CoordinateSystem, pos):
        dX = pos[0] 
        dY = pos[1] 
        dZ = pos[2] 
        dU = pos[3]
        dV = pos[4] 
        dW = pos[5] 
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'HexapodMoveIncremental(' + GroupName + ',' + CoordinateSystem + ',' + str(dX) + ',' + str(dY) + ',' + str(dZ) + ',' + str(dU) + ',' + str(dV) + ',' + str(dW) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]

    def HexapodMoveIncrementalold (self, socketId, GroupName, CoordinateSystem, dX, dY, dZ, dU, dV, dW):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'HexapodMoveIncremental(' + GroupName + ',' + CoordinateSystem + ',' + str(dX) + ',' + str(dY) + ',' + str(dZ) + ',' + str(dU) + ',' + str(dV) + ',' + str(dW) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]

    # HexapodCoordinatesGet :  Get coordinates in a specific coordinate system of a point specified in another coordinate system
    def HexapodCoordinatesGet (self, socketId, GroupName, CoordinateSystemIn, CoordinateSystemOut, Xin, Yin, Zin, Uin, Vin, Win):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'HexapodCoordinatesGet(' + GroupName + ',' + CoordinateSystemIn + ',' + CoordinateSystemOut + ',' + str(Xin) + ',' + str(Yin) + ',' + str(Zin) + ',' + str(Uin) + ',' + str(Vin) + ',' + str(Win) + ',double *,double *,double *,double *,double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(6):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # HexapodCoordinateSystemSet :  Modify the position of a coordinate system
    def HexapodCoordinateSystemSet (self, socketId, GroupName, CoordinateSystem, X, Y, Z, U, V, W):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'HexapodCoordinateSystemSet(' + GroupName + ',' + CoordinateSystem + ',' + str(X) + ',' + str(Y) + ',' + str(Z) + ',' + str(U) + ',' + str(V) + ',' + str(W) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # HexapodCoordinateSystemGet :  Get the position of a coordinate system
    def HexapodCoordinateSystemGet (self, socketId, GroupName, CoordinateSystem):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'HexapodCoordinateSystemGet(' + GroupName + ',' + CoordinateSystem + ',double *,double *,double *,double *,double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(6):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # OptionalModuleExecute :  Execute an optional module
    def OptionalModuleExecute (self, socketId, ModuleFileName, TaskName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'OptionalModuleExecute(' + ModuleFileName + ',' + TaskName + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # OptionalModuleKill :  Kill an optional module
    def OptionalModuleKill (self, socketId, TaskName):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'OptionalModuleKill(' + TaskName + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # ControllerStatusGet :  Read controller current status
    def ControllerStatusGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'ControllerStatusGet(int *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
            j += 1
        retList.append(eval(returnedString[i:i+j]))

        return retList


    # ControllerStatusStringGet :  Return the controller status string corresponding to the controller status code
    def ControllerStatusStringGet (self, socketId, ControllerStatusCode):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'ControllerStatusStringGet(' + str(ControllerStatusCode) + ',char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EEPROMCIESet :  Set CIE EEPROM reference string
    def EEPROMCIESet (self, socketId, CardNumber, ReferenceString):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EEPROMCIESet(' + str(CardNumber) + ',' + ReferenceString + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EEPROMDACOffsetCIESet :  Set CIE DAC offsets
    def EEPROMDACOffsetCIESet (self, socketId, PlugNumber, DAC1Offset, DAC2Offset):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EEPROMDACOffsetCIESet(' + str(PlugNumber) + ',' + str(DAC1Offset) + ',' + str(DAC2Offset) + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EEPROMDriverSet :  Set Driver EEPROM reference string
    def EEPROMDriverSet (self, socketId, PlugNumber, ReferenceString):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EEPROMDriverSet(' + str(PlugNumber) + ',' + ReferenceString + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EEPROMINTSet :  Set INT EEPROM reference string
    def EEPROMINTSet (self, socketId, CardNumber, ReferenceString):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EEPROMINTSet(' + str(CardNumber) + ',' + ReferenceString + ')'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # CPUCoreAndBoardSupplyVoltagesGet :  Get power informations
    def CPUCoreAndBoardSupplyVoltagesGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'CPUCoreAndBoardSupplyVoltagesGet(double *,double *,double *,double *,double *,double *,double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(8):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # CPUTemperatureAndFanSpeedGet :  Get CPU temperature and fan speed
    def CPUTemperatureAndFanSpeedGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'CPUTemperatureAndFanSpeedGet(double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(2):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # ActionListGet :  Action list
    def ActionListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'ActionListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # ActionExtendedListGet :  Action extended list
    def ActionExtendedListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'ActionExtendedListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # APIExtendedListGet :  API method list
    def APIExtendedListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'APIExtendedListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # APIListGet :  API method list without extended API
    def APIListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'APIListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # ErrorListGet :  Error list
    def ErrorListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'ErrorListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # EventListGet :  General event list
    def EventListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'EventListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GatheringListGet :  Gathering type list
    def GatheringListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GatheringExtendedListGet :  Gathering type extended list
    def GatheringExtendedListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringExtendedListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GatheringExternalListGet :  External Gathering type list
    def GatheringExternalListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringExternalListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GroupStatusListGet :  Group status list
    def GroupStatusListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GroupStatusListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # HardwareInternalListGet :  Internal hardware list
    def HardwareInternalListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'HardwareInternalListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # HardwareDriverAndStageGet :  Smart hardware
    def HardwareDriverAndStageGet (self, socketId, PlugNumber):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'HardwareDriverAndStageGet(' + str(PlugNumber) + ',char *,char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # ObjectsListGet :  Group name and positioner name
    def ObjectsListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'ObjectsListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerErrorListGet :  Positioner error list
    def PositionerErrorListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerErrorListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerHardwareStatusListGet :  Positioner hardware status list
    def PositionerHardwareStatusListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerHardwareStatusListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PositionerDriverStatusListGet :  Positioner driver status list
    def PositionerDriverStatusListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PositionerDriverStatusListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # ReferencingActionListGet :  Get referencing action list
    def ReferencingActionListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'ReferencingActionListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # ReferencingSensorListGet :  Get referencing sensor list
    def ReferencingSensorListGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'ReferencingSensorListGet(char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # GatheringUserDatasGet :  Return UserDatas values
    def GatheringUserDatasGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'GatheringUserDatasGet(double *,double *,double *,double *,double *,double *,double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(8):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # ControllerMotionKernelPeriodMinMaxGet :  Get controller motion kernel min/max periods
    def ControllerMotionKernelPeriodMinMaxGet (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'ControllerMotionKernelPeriodMinMaxGet(double *,double *,double *,double *,double *,double *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        if (error != 0):
            return [error, returnedString]

        i, j, retList = 0, 0, [error]
        for paramNb in range(6):
            while ((i+j) < len(returnedString) and returnedString[i+j] != ','):
                j += 1
            retList.append(eval(returnedString[i:i+j]))
            i, j = i+j+1, 0

        return retList


    # ControllerMotionKernelPeriodMinMaxReset :  Reset controller motion kernel min/max periods
    def ControllerMotionKernelPeriodMinMaxReset (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'ControllerMotionKernelPeriodMinMaxReset()'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # TestTCP :  Test TCP/IP transfert
    def TestTCP (self, socketId, InputString):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'TestTCP(' + InputString + ',char *)'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]


    # PrepareForUpdate :  Kill QNX processes for firmware update
    def PrepareForUpdate (self, socketId):
        if (XPS.__usedSockets[socketId] == 0):
            return

        command = 'PrepareForUpdate()'
        [error, returnedString] = self.__sendAndReceive(socketId, command)
        return [error, returnedString]

