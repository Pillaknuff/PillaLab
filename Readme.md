"""
Pillalab - Python version
-> a comprehensive adaptable multi-threading package for lab control purposes
-> Manipulator Control, Pressure reading, automated mapping, network communication, Growth control, BEP measurements
-> developed with focus on UHV, MBE and ARPES processes
-> will also include LEED functions and image aquisition on some point...maybe

Author: Philipp Kagerer
mailto: Philipp.Kagerer@physik.uni-wuerzburg.de
privat: Pt.kag@gmx.de


v 3   ***********************
Pillalab is now uploaded to GitHub (private repos), minor changes will not result in incremented versions any more
Auto-PID functions implemented

v 2.1 ***********************
Pillalab proudly presents: the motion module
Redesign of motion commands over interface able to read multiple controllers on multiple RS-ports
Idea: import as stepper driver instead of stepper drivers and it then re-imports stepper drivers
Has own namespace in settings with motion.*** 

v 2.0 - latest changes 19.07.2020*********************************

For more Documentation see UML model

Changelog: 
AML reader implemented
GUI for Beamlinecontrol implemented
Full restructuring of code to be more readable
Profound commenting and documetation created  

Pending *****************
Implementation of network warning functions
Growth monitoring
Eurotherm implementation
Settings change on runtime ( at the moment mostly restart is required)



v2.0 *******************
Implementation of SES I/O interface
Package restructuring
Implementation of Trinamic Stepper imports

v1.3*******************
Adaptions to R4000
bugfixes in mapping
bugfixes in McLennan R4000 stepper drivers
Adaption in Pressure interfaces

v1.2*******************
Implementation of pressure display interface
Usage with Varian working properly




Style conventions for GUI
colours:
#5f5f5f = grey
#eb0214 = red
#80ff00 = green
#Standard font: Comic Sans MS, 18pt
#buttons, Segoe UI, 14pt

Dependencies:
- Standards see below
- PyTrinamic, if Driver for Trinamic steppers are supposed to be used
- Tkinter
- tested with python 3.7, 3.8
- not compatible with python 2
- tested on windows 10

Communication Channels used:
- RS-232 -> used for most device communication applications
- Ethernet -> used for SES communication, maybe later for status polling, ...

A short guide to the program structure:
- Main Process file: Controller.py -> start main process, crate main GUI window
- GUI Applications <-> Controller <-> backend, drivers, network, logging, ...
- All GUI Requests are re-mapped on Controller functions to enable intercepting, error catching, poll-frequenzy reductions, ....
- Settings are written into a dict, can be updated, stored externally to avoid loosing them, settings will be given to all GUI's and drivers upon startup
    - at the current point it is not guaranteed, that a settings change is transfered to all devices during runtime, a restart is required exept for specific cases
- Once settings are changed the standard settings do not apply anymore, a file called settings.p (pickle file) will be read instead.