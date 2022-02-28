def getDefaultSettings():
        import serial                                                                   # needed for datatypes
        settings = {}
        settings["pressures.readrate"] = 2
        settings["pressures.names"] = ["Mc","Pc","MBE","Fore1","BFM"]                      	        # names of the pressures to be read, most important referer
        settings["pressures.GUIGraphnames"] = ['Mc','Pc','MBE','LL','BFM','Fore1','Fore2']              # allocation of names to the checkboxes in the Pressure display
        settings["pressures.types"] = ["VarianBA","VarianBA","AML","AML","epiMaxUni"]                   # select type of interface to be used, VarianBA, AML_weird, epiMaxUni
        settings["pressures.controllers"] = [0,0,1,1,2]                                                 # should refer to each individual controller available
        settings["pressures.channels"] = [1,2,0,1,1]                                                    # gives the channel to look for in the individual controlers
        settings["pressures.com"] = ["com7","com8","com14"]                                             # port of the individual controlers, not same number as number of gauges
        settings["pressures.baud"] = [9600,9600,4800]                                                   # separated list for each controler
        settings["pressures.bits"] = [8,8,8]                                                            # ...same for bits and so on
        settings["pressures.parity"] = [serial.PARITY_NONE,serial.PARITY_NONE,serial.PARITY_NONE]
        settings["pressures.timeout"] = [0.5,0.5,0.5]
        settings["pressures.stopbits"] = [1,1,1]                     
        settings["pressures.displaytime"] = 2                       # Capture rate for displayin pressures

        settings["internal.readpressures"] = True                  # Flag to turn off pressure read
        #settings["internal.round"] = 1                             # unused
        # 
        # ************************************************** Stepper section *****************************************************************************                
        settings["internal.posupdatetime"] = 2
        settings["internal.posupdatetimestable"] = 2
        settings["internal.comsteppers"] = False                                     # Flag to stop communicating with steppers in direct mode

        #settings for McLennan Hamburg
        # settings["steppers.names" = [0,1,2,3,4,5]]
        # settings["steppers.baud"] = 19200
        # settings["steppers.bits"] = 7
        # settings["steppers.parity"] = "PARITY_EVEN"
        # settings["steppers.stopbits"] = 1
        # settings["steppers.flowcontrol"] = 0
        # settings["steppers.termChar"] = False
        # settings["steppers.timeout"] = 0.5
        
        # settings["steppers.com"] = 'com19'
        # settings["steppers.names"] = [0,1,2,3,4,5]
        # settings["steppers.stepsperunit"] = [1,1,1,1,1,1]
        # settings["steppers.baud"] = 9600
        # settings["steppers.bits"] = 8
        # settings["steppers.parity"] = serial.PARITY_NONE
        # settings["steppers.stopbits"] = 1
        # settings["steppers.flowcontrol"] = 0
        # settings["steppers.termChar"] = False
        # settings["steppers.timeout"] = 0.5

        #settings for r4000
        # settings["steppers.com"] = 'com3'
        # settings["steppers.names"] = [1,10,0,11]
        # #settings["steppers.names"] = [0]
        # settings["steppers.stepsperunit"] = [2000,2000,2000,134,1,1]
        # settings["steppers.baud"] = 4800
        # settings["steppers.bits"] = 8
        # settings["steppers.parity"] = serial.PARITY_NONE
        # settings["steppers.stopbits"] = 1
        # settings["steppers.flowcontrol"] = 0
        # settings["steppers.termChar"] = "\r"
        # settings["steppers.timeout"] = 1

        #settings for Trinamic steppers
        settings["steppers.com"] = 'com22'                                          # com port for main stepper controler
        settings["steppers.names"] = [0,1,2,3,4,5]                                  # names for the individual steppers, makes interface between GUI/listing and controler channels
        settings["steppers.stepsperunit"] = [1000,1000,1000,1000,1000,1000]         # step calibration for steppers
        settings["steppers.holding_currents"] = [5,5,5,5,5,5]                       # Trinamic specific, to avoid overheating
        

        # ********************************* settings for motion module ******************************************************************************
        settings["motion.initialize"] = True
        #settings["motion.nativemove"] = ["multi","single","single"]                 # speciefies, whether moves are prefered on a single axis or movement commands are "collected" and performed uniformely, to be implemented
        settings["motion.nativemove"] = ["single"]   
        #settings["motion.driverfiles"] = ["./stepperdrivers/Hexadrivers.py","./stepperdrivers/McLennanHamburg.py","./stepperdrivers/TMCM_6110_Pillalabdriver.py",]
        #settings["motion.driverfiles"] = ["./stepperdrivers/dummysteppers.py","./stepperdrivers/McLennanHamburg.py","./stepperdrivers/dummysteppers.py"]
        settings["motion.driverfiles"] = ["./stepperdrivers/TMCM_6110_Pillalabdriver.py"]
        #settings["motion.com"] = ['123.345.567','com14','com20']
        settings["motion.com"] = ['com12']
        #settings["motion.baud"] = [9600,9600,9600]
        #settings["motion.bits"] = [9600,7,9600]
        #settings["motion.parity"] = [serial.PARITY_NONE,serial.PARITY_EVEN,serial.PARITY_NONE]
        #settings["motion.stopbits"] = [1,1,1]
        settings["motion.timeout"] = [0.5,0.5,0.5,0.5,0.5,0.5]
        #settings["motion.controllers"] = [0,0,0,0,0,0,1,1,1,1,1,2]
        settings["motion.controllers"] = [0,0,0,0,0,0]
        #settings["motion.groups"] = [0,0,0,0,0,0,1,1,1,1,1,1]
        settings["motion.groups"] = [0,0,0,0,0,0]
        settings["motion.stepsperunit"] = [155,155,155,155,155,155]
        #settings["motion.velocities"] = [[1,1,1,1,1,1],[1,1,1,1,1],[1]]
        settings["motion.velocities"] = [[1000,1000,1000,1000,1000,1000]]
        #settings["motion.names"] = ['x','y','z','u','v','w','s1','s2','s3','s4','s5','s6']      # have to be unique!
        settings["motion.names"] = ['s1','s2','s3','s4','s5','s6']
        settings["motion.channels"] = [0,1,2,3,4,5]                     # Channels on the individual controlers, should match the referer at the individual controler, number at the "dummy"
        # settings["motion.positionsource"] = ["direct","direct","direct","direct","direct","direct","encoder","encoder","encoder","encoder","encoder","encoder"] # not for now, just include in driver

        
        settings["logging.log"] = True                                              # Flag to decide whether to log things like pressures
        settings["logging.filename"] = "logfile.h5"                                 # Name of the logfile, can already exist
        settings["logging.groupname"] = "day_"                                      # name of hdf5 group, will be incremented
        #settings["logging.folder"] = "C:/Users/Philipp/Desktop/temp/"               # folder to log everything into
        settings["logging.folder"] = "C:/Users/MBEcontrol/Documents/Measurements/GrowthLog"
        
        settings["mapping.sesPulltime"] = 1                                         # time in seconds between pulling SES window and sending shortcut
        settings["mapping.stabletime"] = 1                                          # used to decide when movement is stable, dumb waiting without scaling

        settings["network.port"] = 5020                                             # port to listen to for SES interface
        settings["network.timeout"] = 250                                           # timeout time for SES interface in ms, better don't touch
        settings["network.msglen"] = 100                                            # bit-length of network messages, better don't touch
        settings["network.commandtype"] = ["mot","mot","mot","mot","nothing","nothing"] # device type adressed by the individual channels in motor command
        settings["network.channels"] = [0,1,2,3,0,0]                                # channels/motors of the individual positions in SES request, may be motor, ion gauge, ...

        # beamline specific settings, mostly not needed and can be ignored!
        # settings["comtool.polltime"] = 1                                            # polling time for position requests in the comissioning tool
        # settings["comtool.steppernames"] = ['x','y','z','u','v','w','s1','s2','s3','s4','s5','s6']
        # settings["comtool.PyTangoReadNames"] = ['I_sample','I_beam']            # defines what is being read from the PyTango driver, definition of connection done in the PyTango section, names should also be defined there!
        # settings["comtool.trajectoryvecs"] = [[0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,1,1,1,-1,-1,-1],[0,3,0,0,990,0,1,1,1,0,0,0]]       # should be as many as trajectories in GUI defined, will do relative moves on all 6 axis
        
        settings["PyTango.initialize"] = False
        # settings["PyTango.deviceadresses"] = ['hassppa3control:1000/asphere/test/keithley6517a','hassppa3control:1000/asphere/test/keithley6517a']        # List of Tango adresses for devices
        # settings["PyTango.devicetypes"] = ['Keithley_standard','Keithley_standard']                                         # Type of device, used to determine, which variable to read, check driver for what is implemented
        # settings["PyTango.devicename"] = ['I_sample','I_beam']
        # settings["PyTango.dummymode"] = True

        # ******************************************************settings section for growth control*********************************************
        settings["growthcontrol.Controlerallocation"] = [[0],[1],[2],[3],[4],[7],[6]]             # Allocation of the different Controllers to the respective fields (GUI definition)
        settings["growthcontrol.Fieldnames"] = ["Sb2Te3","Tm","Te","BaF2", "MnTe", "Bi2Te3"]                # Naming of the GUI fields
        settings["growthcontrol.Shutterallocation"] = [0,1,2,3,4,5,6]                       # Allocate the shutters to the respective fields
        settings["growthcontrol.BEPreadSeparationtime"] = 2                                     # time spacing between reads
        settings["growthcontrol.BEPstabilisationTime"] = 15                                      # waiting time after opening/closing
        settings["growthcontrol.numreads"] = 2                                                  # number of readings for open/closed to get more precise
        settings["growthcontrol.cycles"] = 3                                                    # number of cycles to do to acquire the BEP
        # backend definitions -> binding of pid controlers
        settings["growthcontrol.comPIDs"] = True
        settings["growthcontrol.Controlernicknames"] = ["Wine","Vodka","Rum","Cachassa","Tequilla","Whiskey","Beer","Cointreau"]      # refering name of the Eurotherms, has to be unique!
        settings["growthcontrol.standardramprates"] = [10,10,10,10,10,10,10,10]                       #
        settings["growthcontrol.bepposition"] = ["open","open","open","open","open","open"]                          # for each Cell gives the setting of the shutter, which should be used for bep reading
        settings["growthcontrol.com"] = ['com10','com11','com4','com13','com5','com9','com6','com15']                           # com adresses of the individual eurotherms
        settings["growthcontrol.slaveadress"] = [1,1,1,1,1,1,1,1]                               # slaveadresses, standard is 1
        settings["growthcontrol.baud"] = [9600,9600,9600,9600,9600,9600,9600,19200]                                # baud rate for eurotherms, standard is 9600
        settings["growthcontrol.type"] = ['eurotherm2408','eurotherm2408','eurotherm2408','eurotherm2408','eurotherm2408','eurotherm2408','eurotherm2408','eurotherm2408']          # refers to eurotherm type, differs in what driver file is assigned to the eurotherm, so far only eurotherm2408 is implemented
        settings["growthcontrol.useexternalPIDvals"] = [False,False,False,False,False,False,False,False]                   # if set to True, uses own PID settings and pushes them to device
        settings["growthcontrol.PIDswitchingpoints"] = [[200,400,800],[200,400,800],[200,400,800],[200,400,800],[200,400,800],[200,400,800],[200,400,800],[200,400,800]]                            # Temperature points for each controler, for which the PID range will be changed (see values below)
        settings["growthcontrol.externalPIDs"] = [[(1,1,1),(1,1,1),(1,1,1)],[(1,1,1),(1,1,1),(1,1,1)],[(1,1,1),(1,1,1),(1,1,1)],[(1,1,1),(1,1,1),(1,1,1)],[(1,1,1),(1,1,1),(1,1,1)],[(1,1,1),(1,1,1),(1,1,1)],[(1,1,1),(1,1,1),(1,1,1)],[(1,1,1),(1,1,1),(1,1,1)],[(1,1,1),(1,1,1),(1,1,1)],[(1,1,1),(1,1,1),(1,1,1)],[(1,1,1),(1,1,1),(1,1,1)],[(1,1,1),(1,1,1),(1,1,1)],[(1,1,1),(1,1,1),(1,1,1)],[(1,1,1),(1,1,1),(1,1,1)],[(1,1,1),(1,1,1),(1,1,1)],[(1,1,1),(1,1,1),(1,1,1)]]          # Software controled PID sets in  controler -> [(PID up to T1),(PID up to T2),...]

        settings["growthcontrol.PressureChannels"] = ["MBE","BFM"]                                              # Used to collect pressures for chamber and monitor

        settings["growthcontrol.Shutterstates"] = [["open","closed"],["open","closed"],["open","closed"],["open","closed"],["open","closed"],["open","closed"],["open","closed"]] # open and closed should always be refered to as open and closed! rest is optiona!
        settings["growthcontrol.ShutterstateAngles"] = [[180,0],[180,0],[180,0],[180,0],[180,0],[180,0],[180,0]]
        settings["growthcontrol.GUIpolltime"] = 1                                                                # GUI refresh every t seconds
        settings["growthcontrol.shutternames"] = ["s4","s2","s3","s1","s5","s6"]                                                     # names of the shutter assignet to the induvidual cells
        

        return settings