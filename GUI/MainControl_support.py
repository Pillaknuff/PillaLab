#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.26
#  in conjunction with Tcl version 8.6
#    Feb 14, 2020 06:48:54 PM CET  platform: Windows NT
#    Aug 09, 2020 01:38:33 AM CEST  platform: Windows NT

import sys

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

# def startMainGUI(controlBackend): # main caller
#     import MainControl
#     global theController 
#     theController= controlBackend #tell everybody about statemashine
#     MainControl.vp_start_gui()

def set_Tk_var():
    global combobox
    combobox = tk.StringVar()


def startMainGUI(controlBackend): # main caller
    import MainControl
    global theController, w ,top_level ,root
    theController= controlBackend #tell everybody about statemashine
    theController.root = tk.Tk()
    top_level = theController.root
    w = MainControl.create_Toplevel1(theController.root)
    w.Flexibox.configure(values=['ComTool','nothing'])
    theController.root.mainloop()



def CallGrowthWindow():
    print('MainControl_support.CallGrowthWindow')
    sys.stdout.flush()
    theController.CallMBEWindow()

def CallManiControlWindow():
    print('MainControl_support.CallManiControlWindow')
    sys.stdout.flush()
    theController.CallManiControlWindow()

def CallMappingWindow():
    print('MainControl_support.CallMappingWindow')
    sys.stdout.flush()
    theController.CallMappingWindow()

def CallPressureWindow():
    print('MainControl_support.CallPressureWindow')
    sys.stdout.flush()
    theController.CallPressureWindow()

def CallSettingsWindow():
    print('MainControl_support.CallSettingsWindow')
    sys.stdout.flush()
    theController.CallSettingsWindow()

def StartFlexicommand():
    print("Flexitoolcall")
    selectedWindow  =  w.Flexibox.get()
    if selectedWindow == 'ComTool':
        theController.CallComissioningToolWindow()

def EnableRemoteControl():
    if theController.remoteAllowed: #check, if on at the moment
        success = theController.StopRemoteControl()
        if success:
            ChangeRemote(False) #switch off the light
        else:
            print("error switching off remote")
    else:
        success = theController.InitializeRemoteControl()
        if success:
            ChangeRemote(True) #switch off the light
        else:
            print("error switching off remote")
    sys.stdout.flush()

def ChangeRemote(what):
    if what:
        w.Frame1.configure(background='#80ff00')
    else:
        w.Frame1.configure(background='#eb0214')

    

def LoadOld():
    print('MainControl_support.LoadOld')
    sys.stdout.flush()

def SaveStatus():
    print('MainControl_support.SaveStatus')
    sys.stdout.flush()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import MainControl
    MainControl.vp_start_gui()





