"""
Pillalab - Python version
see readme for extensive info
"""
import sys          # system functions
import numpy as np  # arrays, numerical
import threading    # simple multi threading
import time         # time measurement, waiting
import importlib    # used for special import purposes
import win32api     # grab System programs
import win32con     # comunicate/keyboard use
import win32gui     # another windows interface
import win32file    # check for new files
import win32event   # ...
import os           # paths, files, similar
import pickle       # export/import python internal data
from datetime import datetime # used writing dates and time in a nice rendered string fashion
import statistics


sys.path.insert(0, "./GUI") # Quick hack to avoid incompatibilities with Page standard output for GUI's, not Gui.package and package both work!
sys.path.insert(0, "./stepperdrivers") # necessary for the motion module
# always import as, to enable update of individual GUI components
import MainControl_support as MainControl_support               # main control gui, used as parent for other GUI's
import Mapping2_support as Mapping_support                      # Mapping window
import PositionControl_support as PositionControl_support       # 4-axis stepper control window with trajectory mode and similar
import Cell_control3_support as Cell_control_support            # MBE control window, set Temperatures, set shutter status, log, read beps
import Pressures_better_support as Pressures_support            # Pressure Display with Matplotlib interactive display
import Settings_support as Settings_support                     # Auto-extending setting dialogue
import ComissioningTool_support as ComissioningTool_support     # writer and designed for Hexapod and Optics Control in Hamburg
import misc.Logging as Logging                                  # Easy hdf5 logging tool
import stepperdrivers.motionModule as motionModule            # Wrapper for the use of multiple motion modules in multiple groups, access defined directely by GUI package
import initialisation.Settingslib as Settingslib
# import drivers.PyTangoReader as PyTangoReader                   # Driver for reading Tango Interfaces, written at P04 Beamline, Petra III storage ring in cooperation with Jens Buck
import drivers.EurothermWrapper as EurothermWrapper             # Driver package creating the Interface to multiple Eurotherm controlers, at the moment 2408 is supported!


# ******* Importers for drivers **************************************************************************************

# select, whichever device you are using, only import one of them
# import is always mapped onto the same name

#import stepperdrivers.McLennanR40003_simple as StepperDriver       # Steppers used at R4000
#import stepperdrivers.Trinamics as StepperDriver                   # Self writter Trinamic drivers, do not work
import stepperdrivers.dummysteppers as StepperDriver                # dummy, can count and pretend to move
#import stepperdrivers.TMCM_6110_Pillalabdriver as StepperDriver    # TMCM driver wrapper for Trinamic, works for 6-axis (6110) and 3-axis (3110) Trinamics controlers, requires Pytrinamic


import drivers.IonGaugeDriver as IonGaugeDriver                     # Multi purpose Ion gauge driver, Varian, AML,...
#import drivers.IonGaugeDriver_dummy as IonGaugeDriver

class controllBackend:
    def __init__(self):
        self.states = []

        # ********* ini settings *********************************************************************************
        #load settings from pickle:
        self.settings = Settingslib.getDefaultSettings()   #first load default cataloge
        sett, err = self.settingsin()
        if not err:
            for key in sett.keys():
                self.settings[key] = sett[key]
        
        # ******** ini actual data storage ***********************************************************************
        self.temppressures = Pressurearray(self.settings)   # ring-storage object for temporary pressure memory(e.g. graphs)
        self.pressures = []                                 # Array containing the last internal pressure state
        self.pressurenames = []                             # Array containing the names of the last pressure states
        self.positions = []                                 # Array containing the last position poll
        self.moving = [False]                               # Array containing the stepper motor state(s)

        self.physicalStateDict = {}                         # Dictionary for listing various physical states of the system, once they are set the first time, no global initialisation
        self.ImportObjectDict= {}                           # Dictionary for imported programs over various guis
        self.runningThreadDict = {}                         # Dictionary for running imported threads (see above for the programs) 

        # ******** ini flags *************************************************************************************
        self.Flawless = False       # Flag for supressing errors in normal operation set to True
        self.PrintToLog = False      # Flag for redirecting the entire print into a Log File
        self.guitestmode = False    # Flag for bypassing external drivers and using "fake number mode"

        #do not edit***************
        self.PressureWindowExists = False   # Internal Flag for the pressure to be communicated
        self.remoteAllowed = False          # Internal Flag for the remote button
        self.LogGrowth = False              # Internal Flag checking, if Growth Log is active
        self.mappingstatus = 'not'          # Internal Flag marking, if mapping is running

        self.pollPressures = False          # Internal Flag used to terminate Continuous Pressure poll processes
        self.terminate = False              # Flag used for terminating all continuously running processes
        #***************************

        #*********** redirect Logging to file *************
        if self.PrintToLog:
            date = datetime.today().strftime('%Y_%m_%d')
            filenm = self.settings["logging.folder"] + date + "_errorlog.txt"
            sys.stdout=open(filenm,"a")

        # ******* initialize packages *************************************************************************
        if self.settings["logging.log"]:
            self.mrLog = Logging.Loggingmachine(self.settings)                  # create logging function
        if self.settings["internal.readpressures"]:
            self.ionGaugeTalker = IonGaugeDriver.IonGaugeTalker(self.settings)  # get settings from settings dict
            self.ionGaugeStati = self.ionGaugeTalker.checkstatus() 
        if self.settings["internal.comsteppers"]:
            self.StepperCon = StepperDriver.Stepper(self.settings)              # create stepper driver instance
            self.steppererror,self.positions,self.moving = self.StepperCon.get_pos_all()        # stepper pre-check
        if self.settings["motion.initialize"]:
            self.motionModule = motionModule.MotionModule(self.settings)        # multi motion interface to directely speak to
        if self.settings["PyTango.initialize"]:
            self.pyTangoInterface = PyTangoReader.PyTangoWrapper(self.settings) # Py-Tango Driver used to read Beamline devices
        if self.settings["growthcontrol.comPIDs"]:
            self.PIDCommunicator = EurothermWrapper.EurothermWrapper(self.settings) # Wrapper for different eurotherm drivers


        # ********* Ini Check drivers ************************************************************************
        
                                     # ion gauge pre-check
        # ******* start processes ****************************************************************************
        
        if self.settings["internal.readpressures"]:
            self.pollPressures = True
            #self.PressureCallRepeater()
            PressurePollThread=threading.Thread(target=self.ContinuousPressurePoll)
            PressurePollThread.start()
            print("Continuous pressure poll started in Controler")

        # ****** Start GUI *********************************************************************************
        MainControl_support.startMainGUI(self)                              # start main GUI-process, program will hang at this point, anyting later will be executed only after termination
        #******* Terminate all Processes *******************************************************************
        self.settings["internal.readpressures"] = False
        self.pollPressures = False
        print("Main GUI Terminated, program should terminate now")
    

    def __del__(self):
        self.settings["internal.readpressures"] = False
        self.pollPressures = False
  
    
    def updateSettings(self,newdic):                # multi settings update
                                                    # do it in a way to not just cancel out stuff
        for key in newdic.keys():
            self.settings[key] = newdic[key]
        self.settingsout()

    def updateSetting(self,key,val):                # single settings update
        self.settings[key] = val
        self.settingsout()
    
    def settingsout(self,filename="settings"):      # settings to file
        pickle.dump( self.settings, open( filename+".p", "wb" ) )

    def settingsin(self,filename="settings"):       # settings from file if available with error if not
        try: 
            ret = pickle.load( open( filename+".p", "rb" ) )
            err = False
            print("loading settings from pickle")
        except:                                     # no settings file available
            print("no predefined settings, taking standard")
            ret = {}
            err = True
        return ret,err

    #*********************Window Calls****************************************************************************************************************************************
    def CallManiControlWindow(self):
        self.Poswindowactive = True
        PositionControl_support.startMainGUI(self)
    
    def CallMappingWindow(self):
        Mapping_support.startMainGUI(self)
    
    def CallMBEWindow(self):
        Cell_control_support.startMainGUI(self)
    
    def CallPressureWindow(self):
        self.PressureWindowExists = True 
        Pressures_support.startMainGUI(self) #now the function itself will call the continuous update stuff

    def CallSettingsWindow(self):
        Settings_support.startMainGUI(self)
    
    def CallComissioningToolWindow(self):
        ComissioningTool_support.startMainGUI(self)



    #******************Mani Control******************************************************************************************************************************************
    def singleAxisMoveRelative(self,whereto,whichaxis): 
        print("hey, i wanna move " + str(whereto) + " on the " + str(whichaxis) + " axis!")
        try: #catch num error
            whereto = float(whereto)
        except Exception as e:
            print("error in single Axis move relative: " + str(e))
            whereto = 0

        if self.guitestmode:                                                                            # decouple the stepper driver, only test gui functions
            self.positions[whichaxis] += whereto
            PositionControl_support.positionUpdate(self.positions)
        else:
            if whichaxis < len(self.settings["steppers.names"]):
                error = self.StepperCon.go_rel(whichaxis,whereto)
            else:
                print("nope, no motor here")

        #self.pollPosUntilStable()

    def singleAxisMoveAbsolute(self,whereto,whichaxis):
        #print("hey, i wanna move absolute" + str(whereto) + " on the " + str(whichaxis) + " axis!")
        try:                                                                                            #catch num error
            whereto = float(whereto)
        except Exception as e:
            print("Error in singleAxisMoveAbsolute: " + str(e))
            whereto = 0

        if self.guitestmode:                                                                            # decouple the stepper driver, only test gui functions
            self.positions[whichaxis] += whereto
            PositionControl_support.positionUpdate(self.positions)
        else:
            if whichaxis < len(self.settings["steppers.names"]):
                error = self.StepperCon.go_abs(whichaxis,whereto)
            else:
                print("nope, no motor here")
        
    def allAxisMoveAbsolute(self,whereto):
        try:
            error = self.StepperCon.go_abs_all(whereto)
        except Exception as e:
            print("error in AllAxisMoveAbsolute: " + str(e))


    def allAxisMoveRelative(self,whereto):
        try:
            error = self.StepperCon.go_rel_all(whereto)
        except Exception as e:
            print("Error in All Axis Move Relative: " + str(e))

    def stop_motors(self):
        #print("stopping")
        try:
            self.StepperCon.stop_all()
        except Exception as e:
            print("error in stop motors: " + str(e))
    
    def pollPos(self):
        try:
            self.steppererror,self.positions,self.moving = self.StepperCon.get_pos_all()
            PositionControl_support.positionUpdate(self.positions)
        except Exception as e:
            print("error in pollPos: " + str(e))

    def continuous_PositionPoll(self):                                                                      # externally activated, then polling position and pushing it back to the GUI...could be done better...
        while self.Poswindowactive:
            self.pollPos()
            if not True in self.moving:
                wtime = self.settings["internal.posupdatetimestable"]   
            else:
                wtime = self.settings["internal.posupdatetime"]
            time.sleep(wtime)
    
    def checkStability(self):
        self.pollPos()
        if True in self.moving:
            return False
        else:
            return True
        

    #**************** internal Mapping Control **********************************************************************************************************************************
    def runMap(self,maplist,axisorder,relmap=False,folder=''):
        import misc.txtLinelogger as maplogger

        if not self.Flawless: #kind of debug mode
            print("controller recieved map, status " + self.mappingstatus)
        if self.mappingstatus == 'not':
            self.mappingstatus = 'running'
            print("starting to run map")
            
            #first: do movement
            self.mappingdict = {
                "offset" : Mapping_support.orderMoveVec(maplist[0],axisorder),
                "mapI" : 0,
                "maplist" : maplist,
                "axisorder" : axisorder,
                "mapfolder": folder,
                "relmap" : relmap
            }

            #create the documentation
            self.maplog = maplogger.txtLinelogger("map",["filename","xyzt"],self.mappingdict["mapfolder"])
            
            #prevent hanging of GUI by putting the iterate and wait in a thread
            mapthread = threading.Thread(target=self.mapstep)
            success = self.pullWindowToFront("SES")
            mapthread.start()
  

        
            #self.mappingstatus = 'not'

    def terminatemap(self): #can be called from out and inside, stops running mapprocess resets map variables 
        self.mappingstatus = "not"
        self.mappingdict = ""
        self.maplog.closeFile()
        self.maplog=""
    
    def pausemap(self):
        print("Controller will pause map former status: " + self.mappingstatus)
        self.mappingstatus = "paused"
    
    def resumemap(self):
        if self.mappingstatus == "paused":
            self.mappingstatus = "running"
        
    def mapstepdummy(self):
        print("dummymapstep " + self.mappingstatus)
        self.mapstepdummy()

    def mapstep(self):
        maplist = self.mappingdict["maplist"]
        print("mapping " + str(self.mappingdict["mapI"]) + "/" + str(len(maplist)))                             #status update
        goto = Mapping_support.orderMoveVec(maplist[self.mappingdict["mapI"]],self.mappingdict["axisorder"])    #get next position and order correspondingly
        if self.mappingdict["relmap"]:
            relstep = np.copy(goto)
            for i in range(len(goto)):
                try:
                    relstep[i] = float(goto[i]) - float(self.mappingdict["offset"])
                except:
                    relstep[i] = "n"
            self.mappingdict["offset"] = goto
            print("requesting relative move: " + str(relstep))
            self.allAxisMoveRelative(relstep)
        else:
            print("would be moving abs tobut onlz theta implemented" + str(goto))
            self.allAxisMoveAbsolute(goto)
        time.sleep(self.settings["mapping.stabletime"])

        success, filename = self.aquireSpectrum(self.mappingdict["mapfolder"])

        #log:
        self.maplog.writeLine([filename,goto])

        if self.mappingstatus == "paused":                                                                      #just hang around, if paused is on
            while self.mappingstatus == "paused":
                time.sleep(0.5)

        if self.mappingstatus == "running":
            if (not self.mappingdict["mapI"] >= (len(maplist) -1)) and success:                                 #next one
                self.mappingdict["mapI"] = self.mappingdict["mapI"] + 1
                self.mapstep()
            else:
                self.terminatemap()
        else:
            self.terminatemap()
        
    
                                                                                                                # function catching the SES program and pulling it to front, sending shortcut
    def aquireSpectrum(self,folder,program="SES",shortcut=['g']):
                                                                                                                # catch program to front
        success = self.pullWindowToFront(program)
        if not success:
            print("Process " + program + " not found! aborting map")
            return False,""
        self.change_handle = win32file.FindFirstChangeNotification (folder,0,win32con.FILE_NOTIFY_CHANGE_FILE_NAME)
        
                                                                                                                #send shortcut
        time.sleep(self.settings["mapping.sesPulltime"])
        for let in shortcut:
            self.CtrlPlusLetter(let)

        old_path_contents = dict ([(f, None) for f in os.listdir (folder)])
        
        while 1:
            result = win32event.WaitForSingleObject (self.change_handle, 500)
            if result == win32con.WAIT_OBJECT_0:
                new_path_contents = dict ([(f, None) for f in os.listdir (folder)])
                added = [f for f in new_path_contents if not f in old_path_contents]
                #deleted = [f for f in old_path_contents if not f in new_path_contents]
                if added: print("Added: ", ", ".join (added))
                #if deleted: print("Deleted: ", ", ".join (deleted))
                if ".ibw" in "".join(added) or ".pxt" in "".join(added):
                    break
                #for entry in 
                #old_path_contents = new_path_contents
                #win32file.FindNextChangeNotification (change_handle)
            else:
                print("waitin")
        win32file.FindCloseChangeNotification (self.change_handle)
        filename = "unknown file"
        for entry in added:
            if ".ibw" in entry or ".pxt" in entry:
                filename = entry
                break
        return True, filename

    # ******* remote control via network ****************************************************************************************************************************************
    def InitializeRemoteControl(self):
        self.remoteAllowed = True                                                                               # set flag
        import drivers.networkInterface as networkInterface
        try:
            self.SESnetworkInterface = networkInterface.networkInterface(self.settings)                         # open connection
            self.mylistener = threading.Thread(target=self.runlistener)                                         # start listener in separate thread to avoid delay
            self.mylistener.start()                                                                             # start listener Thread, will terminate if flage is false
            success = True
        except Exception as e:
            success = False
            print("opening network interface failed with error: " + str(e))
            self.remoteAllowed = False

        return success
    
    def StopRemoteControl(self):                                                                                # external call, close connection, stop listener
        self.remoteAllowed = False
        try:
            self.SESnetworkInterface.closeconnection()
            self.SESnetworkInterface = ''
            success = True
        except Exception as e:
            success = False
            print(" Closing Network failed! ")
            print(e)
        return success

    def runlistener(self):                                                                                      # infinity loop listening on external interface for commands
        if self.remoteAllowed:
            success = self.SESnetworkInterface.listen()
            if success:
                while True and self.remoteAllowed:
                    #dat = myServer.recieveonconnection()
                    dat = self.SESnetworkInterface.quickreceiveconn()
                    print("received: " + dat)
                    self.ProcessNetworkCommand(dat)
            else:
                print("listening not successfull")
        else:
            print("not gonna listen to network, not allowed!")
    
    def ProcessNetworkCommand(self,command):                                                                    # process external command
        action = command[0:3]
        whichval = command[4:7]
        
        if action == 'set':                                                                                     # commands, where something should be done, either move or stop
            if whichval == 'pos':
                values = command[7:]
                values = np.fromstring(values,dtype=float,sep=';')
                values = self.NetworkCommandToPositionRequest(values)[0]                                        # convert to usable position array
                self.allAxisMoveAbsolute(values)
                self.AnswerToNetwork('done')
            elif whichval == 'stp':
                self.stop_motors()
                self.AnswerToNetwork('done')
        elif action == 'get':                                                                                   # commands, where an info is to be returned, either position or stablility
            if whichval == 'pos':
                stvec = self.states
                outstr = self.CreateNetworkPositionString()
                self.AnswerToNetwork(outstr)
                
            elif whichval == 'sts':
                stable = self.checkStability
                ret = str(int(not stable))
                self.AnswerToNetwork(ret)
    
    def AnswerToNetwork(self,answerstring):
        answerstring += '\r\n'
        self.SESnetworkInterface.sendonconnection(answerstring)
        
    def NetworkCommandToPositionRequest(self,array): # 
        movevec = np.zeros(len(self.settings["steppers.names"]))
        others  = []                                                                                            # reserved for more stuff later, prevent errors
        for i in range(len(array)):                                                                             # should always be 6 or less
            commandtype = self.settings["network.commandtype"][i]
            channel = self.settings["network.channels"][i]
            if commandtype == 'mot':                                                                            # possibilities: mot, nothing, pressure, temperature, ...,this is only a internal referer
                try:
                    index = self.settings["steppers.names"].index(channel)
                    movevec[index] = float(array[i])
                except Exception as e:
                    print("failed to get external command at " + str(i))
                    print(e)
        return movevec, others
    
    def CreateNetworkPositionString(self):                                                                      # network should always to configured to ask for positions first!!!
        self.pollPos()
        posarray = np.zeros(6)                                                                                  # array in SES ordering
        for i in range(len(self.positions)):                                                                    # fill string in right order
            motname = self.settings["steppers.names"][i]
            try: 
                index = self.settings["network.channels"].index(motname)
                posarray[index] = self.positions[i]
            except:
                if not self.Flawless:
                    print("not network at " +str(motname))
        outstr = np.array2string(posarray,formatter={'float_kind':lambda x: "%.2f;" % x}).replace('[','').rstrip(';]') #format to desired listtype
        return outstr
            


    # ****** Display Pressures**************************************************************************************************************************************************
    def PressureCallRepeater(self):
        names,pressures = self.GetPressures()

        self.temppressures.addpressure(pressures,time.time())                                               # write pressure into temporary array
        self.DisplayPressures(names,pressures)
        if self.settings["logging.log"]:
            self.LogPressure(pressures)
        if self.settings["internal.readpressures"]:
            threading.Timer(self.settings['pressures.readrate'],self.PressureCallRepeater).start()
    
    def ContinuousPressurePoll(self):                                                                       # new method for pressure polling
        while self.pollPressures:
            try:                                                                                            # the whole logging is done here, to provide evenly spaced data, if re-read is triggered, the triggering program should write it's own log!
                self.pressurenames,self.pressures = self.__GetPressures()
                #print("I'm here and the pressure is" + str(self.pressures))
                self.temppressures.addpressure(self.pressures,time.time())                                  # write pressure into temporary array
                #print("next step")
                if self.settings["logging.log"]:                                                            # if required, log the pressure to hdf5-file
                    self.LogPressure(self.pressures)
            except Exception as e:
                print("Error in Continuous Pressure poll:" + str(e))
            time.sleep(self.settings['pressures.readrate'])                                                 # wait for the polltime, then repeat...forever


    def __GetPressures(self):                                                                               # internal function for actual communicaiton
        if self.settings["internal.readpressures"]:
            names,pressures,errors = self.ionGaugeTalker.readall()                                          # call ion gauge driver-wrapper (all ion gauges under one caller)
            #print(pressures)
            return names,pressures
        else:                                                                                               # case for dumy testing, remove later
            return self.settings["pressures.names"], np.random.rand(len(self.settings["pressures.names"]))
    
    def GetPressures(self,triggerReRead=False):
        if not triggerReRead:
            return self.pressurenames,self.pressures
        else:
            return self.__GetPressures()


    def __GetSinglePressure(self,name,logtag='',):                                                            # internal single pressure read
        if self.settings["internal.readpressures"]:
            pressure, error = self.ionGaugeTalker.readone(name)
        else:
            pressure =  (10e-8 * np.random.rand())
            error = False
        
        if not logtag == '':
            self.LogAction(logtag,name,pressure)
        
        return pressure, error
    
    def GetSinglePressure(self,name,logtag='',triggerReRead=False):
        if not triggerReRead:
            try:
                pressure = self.pressures[self.pressurenames.index(name)]                                   # simply select pressure from List
                error = False
            except Exception as e:
                error = True
                print("Error in GetSinglePressure: " + str(e))
            return pressure, error
        else:                                                                                               # actually read this specific gauge
            try:
                pressure,error = self.__GetSinglePressure(name,logtag)
            except Exception as e:
                pressure = float('nan')
                error = True
                print ("error in GetSinglePressure Reread: " + str(e))
        
            return pressure,error

    def DisplayPressures(self,names,pressures):                                                             # deprecated, delete
        if self.Flawless and self.PressureWindowExists:
            try:
                Pressures_support.UpdatePressures(pressures=pressures,names=names)
            except:
                print("error displaying pressures, probably no such window")
        elif (not self.Flawless) and self.PressureWindowExists:
            Pressures_support.UpdatePressures(pressures=pressures,names=names)
        else:
            print("no window yet")
    
    def getPressureDisplayData(self,name):                                                                  # get pressure array from ring-buffer
        time,pressurearr = self.temppressures.returnpressure(name)
        return time,pressurearr
    
    # ******* Methods to be used for the automized growth and other automatized modules ******************************************************************************************************************
    '''
    This module ist used for importing "recipes" and programs, but can also be used for automatized data aquisition etc.
    The following structure is required:
    
    main class: Programm (imporant: 2*m to avoid any name doubling)
    methods:    run ->      is always called in thread in order not to halt the gui
                            should also set the run and unpause flag, if already running set unpause flag
                pause ->    should set pause flag and also unpause it
                stop ->     should unset run flag, terminate the program and make the thread stop
                
                IMPORTANT:  pause and stop are not running in threads
                            therefore they may only set flags but not do any substantial action themselves
                            otherwise the GUI will hang until this is complete!
    behaviours: 
                double-load ->      will terminate old thread before creating the new one
                Called from GUI:    always give referer to which runtime object to talk to, should stay the same for each gui
                                    referer is also used to pass arguments to thread
    
    Calls are done the following way:

    import_moduleAndText(path,referer)
        -> import the module by path
        -> save it in a main dict with the key referer
        -> if referer is not given the standard is main, to be backward compatible, this may case some override later
    runProgram(referer)
        -> this will start the main running routine
    '''

    def import_moduleAndText(self,apath,referer='main'):
        if referer in self.runningThreadDict.keys(): # try to end old thread before new import
            try:
                myobject = self.ImportObjectDict[referer]
                myobject.stop()
            except Exception as e:
                print("Error while aborting" + str(e))

        # start new import****************
        apath = apath.rstrip()
        try:
            textfile = open(apath,'r')
            text = textfile.read()
        except:
            text = 'error loading'
        
        try: #a little bit complicated solution as importing from a string variable path is not that easy, will not work in Python 2 
            import importlib.util
            spec = importlib.util.spec_from_file_location("automatizer_programm",apath)
            automatizer = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(automatizer)
            self.AutomatizedModule = automatizer.Programm(self)
        except:
            self.AutomatizedModule = Programm(self)
        
        self.ImportObjectDict[referer] = self.AutomatizedModule
        return text

    def runProgram(self,referer='main'):
        try: # try loading the corresponding object and start it in a thread
            AutomatizedModule = self.ImportObjectDict[referer]
            mythread = threading.Thread(target=AutomatizedModule.run)
            self.runningThreadDict[referer] = mythread
            mythread.start()
        except Exception as e:
            print("Error while trying to run AutomatizedModule: " + str(e))
    
    def pauseProgram(self,referer='main'):
        try:
            AutomatizedModule = self.ImportObjectDict[referer]
            AutomatizedModule.pause()
        except Exception as e:
            print("Error while trying to pause AutomatizedModule: " + str(e))
    
    def stopProgram(self,referer='main'):
        try:
            AutomatizedModule = self.ImportObjectDict[referer]
            AutomatizedModule.stop()
        except:
            print("Error while trying to run AutomatizedModule")

    #********************************* Actual growth methods *****************************************************************************

    # immediate response section*****************************************
    def SetTemperature(self,controlername,setp,autotune=False):
        self.PIDCommunicator.setTemperature(controlername,setp)
        self.LogAction('Tset',controlername,setp)
        if autotune:
            Tunethread = threading.Thread(target=self.AutotuneGrabAndSave,args=(controlername,setp))
            Tunethread.start()
    
    def RampTemperature(self,controlername,setp,ramp,autotune=False):
        self.PIDCommunicator.rampTemperature(controlername,setp,ramp)
        self.LogAction('Tramp',controlername,[setp,ramp])
        if autotune:
            Tunethread = threading.Thread(target=self.AutotuneGrabAndSave,args=(controlername,setp))
            Tunethread.start()
    
    def ReadTemperature(self,controlername):
        success = False
        timeout = 5
        i = 0
        while not success and i < timeout:
            temp = self.PIDCommunicator.readTemperature(controlername)
            try:
                temp = float(temp)
                success = True
                break
            except:
                temp = 0
                success = False
                print("Eurotherm had a hickup and returned none")

            i += 1
        self.LogAction('Tread',controlername,temp)
        if not success:
            print("Eurotherm reading timed out on: " + str(controlername))
        return temp
    
    
    # slower response section*******************************************
    def AutotuneGrabAndSave(self,controlername,setp):                                                                                       # followup-function on Autotune, always run in a thread!
        try:
            PID,error = self.PIDCommunicator.grabAutotuneOnSetpoint(controlername,setp)
            if not error:
                ctrlIndex = self.settings["growthcontrol.Controlernicknames"].index(controlername)
                T_list = self.settings["growthcontrol.PIDswitchingpoints"][ctrlIndex] 
                T_index = next(i for i, x in enumerate(T_list) if x >= setp)
                self.settings["growthcontrol.externalPIDs"][ctrlIndex][T_index] = PID
        except Exception as e:
            print("Error in Controler-AutotuneGrabAndSave: " + str(e))
            error = True
        
        if not error:                                                                                                                       # if this has worked -> save new parameters!
            self.settingsout()

    def measureBEP(self,controlername,shutter):
        
        openstate = self.settings["growthcontrol.bepposition"][self.settings["growthcontrol.Controlernicknames"].index(controlername)]      # search out number of controler, then get the respective fitting value for the bep measuring position
        
        bep_array = []
        
        for j in range(self.settings["growthcontrol.cycles"]):
            basepressure = 0
            basecounter = 0
            for i in range(self.settings["growthcontrol.numreads"]):
                p,err = self.GetSinglePressure(self.settings["growthcontrol.PressureChannels"][1], triggerReRead=True)
                try:
                    basepressure +=  p
                    basecounter += 1                                                                                                            # location of the Pressure monitors name
                except Exception as e:
                    print("missread in p" + str(e))
                time.sleep(self.settings["growthcontrol.BEPreadSeparationtime"])
            self.SetShutterState(shutter,openstate)
            time.sleep(self.settings["growthcontrol.BEPstabilisationTime"])
            openpressure = 0
            opencounter = 0

            for i in range(self.settings["growthcontrol.numreads"]):
                p,err = self.GetSinglePressure(self.settings["growthcontrol.PressureChannels"][1], triggerReRead=True)
                try:
                    openpressure +=  p
                    opencounter += 1                                                                         
                except Exception as e:
                    print("missread in p" + str(e))
                time.sleep(self.settings["growthcontrol.BEPreadSeparationtime"])
            openpressure = openpressure/opencounter

            self.SetShutterState(shutter,'closed')
            time.sleep(self.settings["growthcontrol.BEPstabilisationTime"])
            for i in range(self.settings["growthcontrol.numreads"]):
                p,err = self.GetSinglePressure(self.settings["growthcontrol.PressureChannels"][1], triggerReRead=True)
                try:
                    basepressure +=  p
                    basecounter += 1                                                                         
                except Exception as e:
                    print("missread in p" + str(e))
                time.sleep(self.settings["growthcontrol.BEPreadSeparationtime"])                                                                   
            time.sleep(self.settings["growthcontrol.BEPreadSeparationtime"]) 
            
            basepressure = basepressure/(basecounter)
            bep = openpressure - basepressure
            bep_array.append(bep)
        
        bep_avg = statistics.mean(bep_array)
        bep_stdev = statistics.stdev(bep_array)

        print("BEP measured: " + str(bep_array) + " mean: " + str(bep_avg) + " stdev: " + str(bep_stdev))
        



        self.LogAction('bep',controlername,[bep_avg,bep_stdev])
        return bep_avg
        
    # Shutter control***************************************************
    '''
    How is the Logging structured:
    - general Events like Shutters, BEP readings, changes in T-setpoints etc. are stored as string variables in the Dataset called 'EventLog'
    - a separate Log is written for each temperature
    - a separate Log is written for each pressure
    '''

    def SetShutterState(self,shutter,state):                                                                                            # a Shutter is always refered by a number!
        # 0 is closed, 1 is open, rest depends on system
        #print('Trying to set shutter ' + str(shutter) + ' in state '+ str(state) + 'but fail because of missing implementation...')
        self.LogAction('Shuttermove',shutter,state)
        self.physicalStateDict[str(shutter)] = str(state)
        try:
            shuttername = self.settings["growthcontrol.shutternames"][shutter]
            shutterangle = self.settings["growthcontrol.ShutterstateAngles"][shutter][self.settings["growthcontrol.Shutterstates"][shutter].index(state)]
            error = False
        except Exception as e:
            if not str(shutter) == "substrate":                                                                                               # supress error, if shutter cannot be found, elegant, as that way a substrate shutter could be easily implemented, but errors are ignored 
                print("error defining shuttermove: " + str(e))
            error = True
        
        if not error:
            self.motionModule.go_abs(shuttername,shutterangle)

    def CalibShutterPosition(self,shutter,actualstate):
        print('shutter is calibrated in position ' + str(actualstate))
        self.LogAction('Shuttercalibration',shutter,actualstate)
        try:
            shuttername = self.settings["growthcontrol.shutternames"][shutter]
            error = False
        except Exception as e:
            print("error defining shutter calibration: " + str(e))
            error = True
        
        self.motionModule.set_pos(shuttername,actualstate)

    # backing functions**************************************************
    def LogAction(self,what,name,value=0):
        if self.LogGrowth:
            #print(str(what) + " " + str(name) + " : " + str(value))
            if what == 'Shuttercalibration':
                self.GrowthLogger.logEntry('EventLog','Shutter ' + str(name) + ' calibrated to ' + str(value))
            elif what == 'Shuttermove':
                self.GrowthLogger.logEntry('EventLog','Shutter ' + str(name) + ' moved to ' + str(value))
            elif what == 'bep':
                self.GrowthLogger.logEntry('EventLog','BEP on ' + str(name) + ' measured to ' + str(value))
            elif what == 'Tset':
                self.GrowthLogger.logEntry('EventLog','T setpoint on ' + str(name) + ' changed to ' + str(value))
            elif what == 'TAuto':
                self.GrowthLogger.logEntry('EventLog','T Autotune on ' + str(name) + ' activated at ' + str(value))
            elif what == 'Tramp':
                self.GrowthLogger.logEntry('EventLog','T setpoint on ' + str(name) + ' ramping to/with ' + str(value))
            elif what == 'Tread': #log in separate channel
                self.GrowthLogger.logEntry('T_'+str(name),value)
            elif what == 'Pressurecheck': #log in separate channel
                self.GrowthLogger.logEntry('P_'+str(name),value)
            else:
                print("Logging unknown Tag discovered "+ str(what))
    
    def StartGrowthLog(self,filename,username=''):
        print("Starting Growth Log")
        self.LogGrowth = True
        self.GrowthLogger = Logging.UniversalLoggingTool(self.settings,filename,user=username,groupmask="growthlog")
    
    def EndGrowthLog(self):
        print("Ending Growth Log")
        self.LogGrowth = False
        self.GrowthLogger.stoplog()
        self.GrowthLogger = ""

    



    
    # ********* Prodedures for logging ****************************************************************************************************************************************
    def LogPressure(self,pressures):
        #print ("will be logging " + str(time.time()) + " " + str(pressures))
        pressuresfloat = []
        for pressure in pressures:#in principle not necessary any more...but whatever
            try:
                pressure = float(pressure)
            except:
                try:
                    pressure= pressure.rstrip()
                    pressure = pressure.replace('>','')
                    pressure = float(pressure)
                except:
                    print("error converting " + str(pressure) + " to float")
                    pressure = float(0)
            pressuresfloat.append(pressure)
        self.mrLog.logpressures(pressuresfloat)
        # try:
        #     self.mrLog.logpressures(pressures)
        # except:
        #     print("error while logging")


    # ****** utils *************************************************************************************************************************************************************
    

    def windowEnumerationHandler(self,hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    def pullWindowToFront(self,name):
        top_windows = []
        win32gui.EnumWindows(self.windowEnumerationHandler, top_windows)
        #print(top_windows)
        for i in top_windows:
            if name == i[1]:
            #if name.lower() in i[1].lower():
                print(i)
                win32gui.ShowWindow(i[0],5)
                win32gui.SetForegroundWindow(i[0])
                return True
        return False

    def CtrlPlusLetter(self,l):
        VK_CODE = {'backspace':0x08,
        'tab':0x09,
        'clear':0x0C,
        'enter':0x0D,
        'shift':0x10,
        'ctrl':0x11,
        'alt':0x12,
        'pause':0x13,
        'caps_lock':0x14,
        'esc':0x1B,
        'spacebar':0x20,
        'page_up':0x21,
        'page_down':0x22,
        'end':0x23,
        'home':0x24,
        'left_arrow':0x25,
        'up_arrow':0x26,
        'right_arrow':0x27,
        'down_arrow':0x28,
        'select':0x29,
        'print':0x2A,
        'execute':0x2B,
        'print_screen':0x2C,
        'ins':0x2D,
        'del':0x2E,
        'help':0x2F,
        '0':0x30,
        '1':0x31,
        '2':0x32,
        '3':0x33,
        '4':0x34,
        '5':0x35,
        '6':0x36,
        '7':0x37,
        '8':0x38,
        '9':0x39,
        'a':0x41,
        'b':0x42,
        'c':0x43,
        'd':0x44,
        'e':0x45,
        'f':0x46,
        'g':0x47,
        'h':0x48,
        'i':0x49,
        'j':0x4A,
        'k':0x4B,
        'l':0x4C,
        'm':0x4D,
        'n':0x4E,
        'o':0x4F,
        'p':0x50,
        'q':0x51,
        'r':0x52,
        's':0x53,
        't':0x54,
        'u':0x55,
        'v':0x56,
        'w':0x57,
        'x':0x58,
        'y':0x59,
        'z':0x5A,
        'numpad_0':0x60,
        'numpad_1':0x61,
        'numpad_2':0x62,
        'numpad_3':0x63,
        'numpad_4':0x64,
        'numpad_5':0x65,
        'numpad_6':0x66,
        'numpad_7':0x67,
        'numpad_8':0x68,
        'numpad_9':0x69,
        'multiply_key':0x6A,
        'add_key':0x6B,
        'separator_key':0x6C,
        'subtract_key':0x6D,
        'decimal_key':0x6E,
        'divide_key':0x6F,
        'F1':0x70,
        'F2':0x71,
        'F3':0x72,
        'F4':0x73,
        'F5':0x74,
        'F6':0x75,
        'F7':0x76,
        'F8':0x77,
        'F9':0x78,
        'F10':0x79,
        'F11':0x7A,
        'F12':0x7B,
        'F13':0x7C,
        'F14':0x7D,
        'F15':0x7E,
        'F16':0x7F,
        'F17':0x80,
        'F18':0x81,
        'F19':0x82,
        'F20':0x83,
        'F21':0x84,
        'F22':0x85,
        'F23':0x86,
        'F24':0x87,
        'num_lock':0x90,
        'scroll_lock':0x91,
        'left_shift':0xA0,
        'right_shift ':0xA1,
        'left_control':0xA2,
        'right_control':0xA3,
        'left_menu':0xA4,
        'right_menu':0xA5,
        'browser_back':0xA6,
        'browser_forward':0xA7,
        'browser_refresh':0xA8,
        'browser_stop':0xA9,
        'browser_search':0xAA,
        'browser_favorites':0xAB,
        'browser_start_and_home':0xAC,
        'volume_mute':0xAD,
        'volume_Down':0xAE,
        'volume_up':0xAF,
        'next_track':0xB0,
        'previous_track':0xB1,
        'stop_media':0xB2,
        'play/pause_media':0xB3,
        'start_mail':0xB4,
        'select_media':0xB5,
        'start_application_1':0xB6,
        'start_application_2':0xB7,
        'attn_key':0xF6,
        'crsel_key':0xF7,
        'exsel_key':0xF8,
        'play_key':0xFA,
        'zoom_key':0xFB,
        'clear_key':0xFE,
        '+':0xBB,
        ',':0xBC,
        '-':0xBD,
        '.':0xBE,
        '/':0xBF,
        '`':0xC0,
        ';':0xBA,
        '[':0xDB,
        '\\':0xDC,
        ']':0xDD,
        "'":0xDE,
        '`':0xC0}

        win32api.keybd_event(VK_CODE['ctrl'], 0,0,0)
        win32api.keybd_event(VK_CODE[l], 0,0,0)
        time.sleep(.05)
        win32api.keybd_event(VK_CODE[l],0 ,win32con.KEYEVENTF_KEYUP ,0)
        win32api.keybd_event(VK_CODE['ctrl'],0 ,win32con.KEYEVENTF_KEYUP ,0)



# ************************** Misc ********************************************************************************************************************************************
# ****************************************************************************************************************************************************************************

class Programm: #module for error handling
    def __init__(self,controller):
        a = 1
    def run(self):
        print("no module imported")
    def pause(self):
        print("no module imported")
    def stop(self):
        print ("no module imported")

class Pressurearray:                                                                            # advanced class of Pressure array with limited time memory
    def __init__(self,settings):
        self.settings = settings
        days = settings["pressures.displaytime"]
        self.statearray = []
        self.seconds = days*24*60*60                                                            # number of seconds

    def addpressure(self,pressures,timestamp):                                                  # pressures has to be an array
        
        pressures = [float(i) for i in pressures]                                               # convert whole array to float for safety
        self.statearray.append([timestamp,pressures])                                           # append to long array
        threshold = time.time() - self.seconds                                                  # start ring-buffer function -> get threshold time
        self.statearray = list(filter(lambda entry: entry[0] >=threshold , self.statearray))    # sort out everything older than threshold


    def returnpressure(self,name):                                                              # returns the whole pressure history for a give gauge name

        try:
            index = self.settings["pressures.names"].index(name)
            temparray = np.array(self.statearray)
            pressures = temparray[:,1]
            pressures = np.array([np.array(i) for i in pressures])
            time = temparray[:,0]
            pressure = pressures[:,index]
            pressure = np.array(pressure,dtype=float)
            time = np.array(time,dtype=float)
        except Exception as e:
            time = [0]
            pressure = [0]
            index = self.settings["pressures.names"].index(name)
            temparray = np.array(self.statearray)
            print("Pressure not found: " + str(name) + " --> " + str(e))

        return time,pressure



if __name__ == '__main__':
    TheController = controllBackend()



