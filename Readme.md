"""
Pillalab - Python version
-> a comprehensive adaptable multi-threading package for lab control purposes
-> Manipulator Control, Pressure reading, automated mapping, network communication, Growth control, BEP measurements
-> developed with focus on UHV, MBE and ARPES processes
-> will also include LEED functions and image aquisition on some point

Author: Philipp Kagerer
mailto: Philipp.Kagerer@physik.uni-wuerzburg.de
privat: Pt.kag@gmx.de

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