#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 5.4
#  in conjunction with Tcl version 8.6
#    Aug 22, 2020 09:25:28 PM CEST  platform: Windows NT
#    Aug 23, 2020 12:32:52 AM CEST  platform: Windows NT
#    Oct 19, 2020 03:40:46 PM CEST  platform: Windows NT
#    Dec 06, 2020 01:07:28 PM CET  platform: Windows NT

import sys
import threading
import time

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def set_Tk_var():
    global AtuneVar1
    AtuneVar1 = tk.StringVar()
    global che49
    che49 = tk.IntVar()
    global AtuneVar2
    AtuneVar2 = tk.StringVar()
    global AtuneVar3
    AtuneVar3 = tk.StringVar()
    global AtuneVar4
    AtuneVar4 = tk.StringVar()
    global AtuneVar5
    AtuneVar5 = tk.StringVar()
    global AtuneVar6
    AtuneVar6 = tk.StringVar()
    global AtuneVarS
    AtuneVarS = tk.StringVar()
    global Sselect1
    Sselect1 = tk.StringVar()
    global Tselect1
    Tselect1 = tk.StringVar()
    global Sselect2
    Sselect2 = tk.StringVar()
    global Tselect2
    Tselect2 = tk.StringVar()
    global Sselect3
    Sselect3 = tk.StringVar()
    global Tselect3
    Tselect3 = tk.StringVar()
    global Sselect4
    Sselect4 = tk.StringVar()
    global Tselect4
    Tselect4 = tk.StringVar()
    global Sselect5
    Sselect5 = tk.StringVar()
    global Tselect5
    Tselect5 = tk.StringVar()
    global Sselect6
    Sselect6 = tk.StringVar()
    global Tselect6
    Tselect6 = tk.StringVar()
    global combobox
    combobox = tk.StringVar()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def startMainGUI(controlBackend): # main caller
    import Cell_control3
    global theController, w ,top_level ,root, Tselectors, Tsettinpoints, Tramps, Shutterselectors, Cellnames, Tdisplays, BepDisplays,Autotuneboxes,Eventlist, substratenentrynumber
    
    substratenentrynumber = 6 # used to refer to substrate as an special entry, by default the last one
    theController= controlBackend #tell everybody about statemashine
    top, w = Cell_control3.create_Toplevel1(theController.root)  # create initial window process

    # make global lists of widgets *********
    Tselectors = [w.Tselector1,w.Tselector2,w.Tselector3,w.Tselector4,w.Tselector5,w.Tselector6]                                                # select cell length used to label cells, substrate is unique
    Tsettinpoints = [w.Tset1,w.Tset2,w.Tset3,w.Tset4,w.Tset5,w.Tset6,w.Tset_S]                                                                  # setpoints inputs, also contains substrate
    Tramps = [w.rset1,w.rset2,w.rset3,w.rset4,w.rset5,w.rset6,w.rset_S]                                                                         # ramprate inputs, also substrate
    Shutterselectors = [w.Shutterselector1,w.Shutterselector2,w.Shutterselector3,w.Shutterselector1_8,w.Shutterselector5,w.Shutterselector6]    # fields selecting the state the shutter should be set into
    Tdisplays = [w.LabelTcell1,w.LabelTcell2,w.LabelTcell3,w.LabelTcell4,w.LabelTcell5,w.LabelTcell6,w.LabelT_S]                                # Temperature displays for the individual cells
    Cellnames = [w.Headerlabel1,w.Headerlabel2,w.Headerlabel3,w.Headerlabel4,w.Headerlabel5,w.Headerlabel6]
    #BepDisplays = [w.LabelBEP,w.LabelBEP_8,w.LabelBEP_9,w.LabelBEP_10,w.LabelBEP_11,w.LabelBEP_12]
    BepDisplays = [w.BEPdisp1,w.BEPdisp2,w.BEPdisp3,w.BEPdisp4,w.BEPdisp5,w.BEPdisp6]                                                           # Displays to show the measured BEP results
    Autotuneboxes = [w.Autotunecheck1,w.Autotunecheck2,w.Autotunecheck3,w.Autotunecheck4,w.Autotunecheck5,w.Autotunecheck6,w.AutotunecheckS]    # Autotune checkboxes

    for i in range(len(Tselectors)):                    # now fill all fields with meaning
        try:
            allocationlist = theController.settings["growthcontrol.Controlerallocation"][i]
            namelist = []
            for num in allocationlist:
                namelist.append(theController.settings["growthcontrol.Controlernicknames"][num])
            Tselectors[i].configure(values=namelist)
            Tselectors[i].current(0)
            Cellnames[i].config(text=theController.settings["growthcontrol.Fieldnames"][i])
            Shutterselectors[i].configure(values=theController.settings["growthcontrol.Shutterstates"][theController.settings["growthcontrol.Shutterallocation"][i]])
            Shutterselectors[i].current(0)

        except Exception as e:
            print("error while filling fields in Cell Control, maybe ignorable: " + str(e))

    # stuff used for the dynamic string input functions
    Eventlist = []
    global CurrentStringInput
    CurrentStringInput = ""

    global celctrrunning
    celctrrunning = True
    ContiuousUpdateThread = threading.Thread(target = GuiRefresher)
    ContiuousUpdateThread.start()

    top.protocol("WM_DELETE_WINDOW", destroy_window) 

#*************************** Periodic functions ***************************

def GuiRefresher():                                                                     # continuous update of all readings of the GUI
    while celctrrunning:
        for i in range(7):
            # Update Temperature readings***********************
            if not i == substratenentrynumber:
                channel = Tselectors[i].get()
            else:
                channel = "substrate"

            if channel in theController.settings["growthcontrol.Controlernicknames"]:
                Tresponse = theController.ReadTemperature(channel)
                Tresponse = "{:.2f}".format(Tresponse)
                Tdisplays[i].configure(text = (Tresponse + " °C"))

        for i in range(2):    
            # Update Pressure readings*************************
            try:
                mypressure,error = theController.GetSinglePressure(theController.settings["growthcontrol.PressureChannels"][i],logtag='Pressurecheck')
                if i == 1:
                    mywidget = w.monitorPdisp
                else:
                    mywidget = w.chamberPdisp
                pressuretext  = '{:0.2e}'.format(mypressure)
                mywidget.configure(text=pressuretext)
            except Exception as e:
                print("error polling pressure " + str(e))
        time.sleep(theController.settings["growthcontrol.GUIpolltime"])
        

#************************** Universal Cell Control Functions***************
def setTemperature(controler):
    if not controler == substratenentrynumber:                                                  # check, whether the given controler is the substrate, if not, get the corresponding selected entry
        channel = Tselectors[controler].get()                                                   # read dropdown menu value from respective field
    else:
        channel = "substrate"

    autotune = getAutotuneVal(controler)                                                        # check if supposed to autotune
    setpoint = Tsettinpoints[controler].get()
    try:
        setpoint = float(setpoint)
        if channel in theController.settings["growthcontrol.Controlernicknames"]:
            #print("setting temperature on " + str(channel) + " to " + str(setpoint))
            theController.SetTemperature(channel,setpoint,autotune)
        else:
            print("channel not supported!")
    except Exception as e:
        print("error setting Temperature: " + str(e))


def rampTemperature(controler):
    if not controler == substratenentrynumber:
        channel = Tselectors[controler].get()
    else:
        channel = "substrate"

    autotune = getAutotuneVal(controler)                                                        # check if supposed to autotune
    setpoint = Tsettinpoints[controler].get()
    rampspeed = Tramps[controler].get()
    
    try:
        setpoint = float(setpoint)
        rampspeed = float(rampspeed)
        if channel in theController.settings["growthcontrol.Controlernicknames"]:
            #print("setting rampspeed on " + str(channel) + " to " + str(setpoint) + " with speed " + str(rampspeed))
            theController.RampTemperature(channel,setpoint,rampspeed,autotune)
        else:
            print("channel not supported!")
    except Exception as e:
        print("error ramping Temperature: " + str(e))

def getAutotuneVal(controler):                                                                  # function to check, whether a certain controler is supposed to do autotune
    try:
        widget = Autotuneboxes[controler]                                                       # grab autotune checkbox
        state = widget.state()
        if ('alternate' in state) or ('selected' in state):
            state = True
        else:
            state = False
    except Exception as e:
        print("error grabbing Autotune checkbox state")
        state = False
    
    return state

def measureBEP(controler):
    BepThread = threading.Thread(target=performBEPmeasurementAndUpdate,args=[controler])
    BepThread.start()

def performBEPmeasurementAndUpdate(controler):
    error = False
    try:
        channel = Tselectors[controler].get()
        shutter = theController.settings["growthcontrol.Shutterallocation"][controler]
    except Exception as e:
        print(e)
        error = True
    if not error:
        newBEP = theController.measureBEP(channel,shutter)
        strBEP = '{:0.2e}'.format(newBEP)
        BepDisplays[controler].configure(text=strBEP)

def openShutter(field):
    print("opening shutter")
    if not field >= len(theController.settings["growthcontrol.Shutterallocation"]):
        shutter = theController.settings["growthcontrol.Shutterallocation"][field]
        theController.SetShutterState(shutter,'open')
    else:
        print("shutter not implemented on " + str(field))

def closeShutter(field):
    print("closing shutter")
    if not field >= len(theController.settings["growthcontrol.Shutterallocation"]):
        shutter = theController.settings["growthcontrol.Shutterallocation"][field]
        theController.SetShutterState(shutter,'closed')
    else:
        print("shutter not implementedon " + str(field))

def setShutter(field):
    state = Shutterselectors[field].get()
    shutter = theController.settings["growthcontrol.Shutterallocation"][field]
    if not field >= len(theController.settings["growthcontrol.Shutterallocation"]):
        shutter = theController.settings["growthcontrol.Shutterallocation"][field]
        theController.SetShutterState(shutter,state)
    else:
        print("shutter not implementedon " + str(field))

def calibShutter(field):
    print("calibrating shutter")
    outtext = "Please read shutter angle and enter into input console!"
    w.GPIO_text.delete("1.0",tk.END)
    w.GPIO_text.insert("1.0",outtext)
    calibThread = threading.Thread(target=WaitForCalibInput,args=[field])
    calibThread.start()

def WaitForCalibIntput(field):
    myEvent = threading.Event() # used for effective waitint
    global Eventlist
    Eventlist.append(myEvent)

    myEvent.wait()
    try:
        actualstate = float(CurrentStringInput)
        myshutter = theController.settings["growthcontrol.Shutterallocation"][field]
        theController.CalibShutterPosition(myshutter,actualstate)
    except Exception as e:
        print("Error calibrating shutter: " + str(e))

def moveSubstrateShutter(state):
    theController.SetShutterState("substrate",state)
    

#************************** Skript section ********************************
def selectSkriptPath():
    try:
        from tkinter import filedialog
    except:
        import tkFileDialog as filedialog
    file_path = filedialog.askopenfilename()
    w.Loadpath.delete('0', tk.END)
    w.Loadpath.insert('0',file_path)

def loadSkript():
    path = w.Loadpath.get()
    text = theController.import_moduleAndText(path,referer='growthtool')
    try:
        w.LoadedText.delete('1.0', tk.END)
        w.LoadedText.insert('1.0',text)
    except Exception as e:
        print("error while writting program code in com-tool: " + str(e))

def runSkript():
    theController.runProgram(referer='growthtool')

def abortSkript():
    theController.stopProgram(referer='growthtool')

def pauseSkript():
    theController.pauseProgram(referer='growthtool')

# ************** general functions*********************************
def selectGraphEntries():
    print('Cell_control3_support.selectGraphEntries')
    sys.stdout.flush()

def enterInput():
    print('Cell_control3_support.enterInput')
    sys.stdout.flush()
    global CurrentStringInput
    CurrentStringInput = w.GPInput.get()
    global Eventlist
    for event in Eventlist:
        event.set()

def destroy_window():
    # Function which closes the window.
    global top_level,celctrrunning
    celctrrunning = False
    top_level.destroy()
    top_level = None

# ****************** Logging ***************************************

def startLog():
    filename = w.SampleName.get()
    username = w.UserName.get()
    theController.StartGrowthLog(filename,username=username)

def endLogging():
    theController.EndGrowthLog()

#****************** Graphics section ******************************

# ********************** indvidually forwarded commands************
def openS1():
    openShutter(0)

def openS2():
    openShutter(1)

def openS3():
    openShutter(2)

def openS4():
    openShutter(3)

def openS5():
    openShutter(4)

def openS6():
    openShutter(5)

def openTS():
    moveSubstrateShutter("open")

def setS1():
    setShutter(0)

def setS2():
    setShutter(1)

def setS3():
    setShutter(2)

def setS4():
    setShutter(3)

def setS5():
    setShutter(4)

def setS6():
    setShutter(5)

def setT1():
    setTemperature(0)

def setT2():
    setTemperature(1)

def setT3():
    setTemperature(2)

def setT4():
    setTemperature(3)

def setT5():
    setTemperature(4)

def setT6():
    setTemperature(5)

def setTS():
    setTemperature(substratenentrynumber)

def rampS4():
    rampTemperature(3)

def rampT1():
    rampTemperature(0)

def rampT2():
    rampTemperature(1)

def rampT3():
    rampTemperature(2)

def rampT5():
    rampTemperature(4)

def rampT6():
    rampTemperature(5)

def rampTS():
    rampTemperature(substratenentrynumber)

def bepT1():
    measureBEP(0)

def bepT2():
    measureBEP(1)

def bepT3():
    measureBEP(2)

def bepT4():
    measureBEP(3)

def bepT5():
    measureBEP(4)

def bepT6():
    measureBEP(5)

def calibS1():
    calibShutter(0)

def calibS2():
    calibShutter(1)

def calibS3():
    calibShutter(2)

def calibS4():
    calibShutter(3)

def calibS5():
    calibShutter(4)

def calibS6():
    calibShutter(5)

def closeS1():
    closeShutter(0)

def closeS2():
    closeShutter(1)

def closeS3():
    closeShutter(2)

def closeS4():
    closeShutter(3)

def closeS5():
    closeShutter(4)

def closeS6():
    closeShutter(5)

def closeTS():
    moveSubstrateShutter("closed")

if __name__ == '__main__':
    import Cell_control3
    Cell_control3.vp_start_gui()





