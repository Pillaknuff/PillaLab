"""
Jens Buck, 18 Oct 2016

library of commonly used tango and epics variables for P04 beamline
and some convenience functions

This has a high potential to be reused in all other beamline-interfacing applications 


to do:
 - add new cookie box variables:
   ISeg voltages
   gas needle motor and encoder
   pressure gauges for cookie box
   
 - update ps2 slit motor names
 
Oct 29, 2017
 - renamed slits from SLT2_* to PS2_*
 - included some tango and epics variables:
  mono (moved to epics)
  gas inlet valve of CB
  keithley at PIPE (diode AFT_PIPE)
  ISeg voltages for CB (?)

Oct 30,2018
 - copy/pasted version for TangoMonitor
 - truncated for use with TangoMonitor (e.g., no EPICS supported)

Nov 1, 2018
 -  removed 'RdWireKoordinaten' from MOMOs
 - updated Tango path/device name to pressure devices

Apr 8, 2020
 - added mcp voltages of branch2 cookie box (to be used with TangoMonitor)
 - updated access to mono (was a really old name!)
May 31, 2020
 - added diode current of intermdiate focus branch1 (Keysight)
 - added beam position from TINE (Cell2 == sector3, according to info in TINE-to-Tango device)
"""


import sys

# library of Tango/Epics paths alongside with flags
# sequence: 
# control system identifier (tango/epics,...)
# string path (with machine/port)
# property of the Tango object
# read flag
# write flag
p04vars_attr = ['sysID','path','valID','ReadFlag','WriteFlag'];
p04vars = {'exitslit':['tango','haspp04exp2:10000/motor/vm_vm_slit/1','Position',True,False],
           'undugap':['tango','haspp04exp2:10000/p04/plcundulator/1','currentgap',True,False],
           'unduenergy':['tango','haspp04exp2:10000/p04/undulatorp04/exp2.01','Position',True,False],
           'undushift':['tango','haspp04exp2:10000/p04/plcundulator/1','CurrentShift',True,False],                      
           'screen':['tango','haspp04exp2:10000/motor/omsvme58_exp2/7','Position',True,False],
           'RMU2_rotx':['tango','haspp04exp1:10000/p04/rmup04/rmu2.vrotx','Position',True,False],
           'RMU2_rotz':['tango','haspp04exp1:10000/p04/rmup04/rmu2.hrotz','Position',True,False],
           'RMU2_transx':['tango','haspp04exp1:10000/p04/rmup04/rmu2.vx','Position',True,False],
           'RMU2_transz':['tango','haspp04exp1:10000/p04/rmup04/rmu2.hz','Position',True,False],           
           'MOMO_xnor78':['tango','haspp04exp2:10000/petra/momo/x-nor_078',['RdKoordinate'],True,False],
           'MOMO_xnor73':['tango','haspp04exp2:10000/petra/momo/x-nor_073',['RdKoordinate'],True,False],
           'MOMO_znor78':['tango','haspp04exp2:10000/petra/momo/z-nor_078',['RdKoordinate'],True,False],
           'MOMO_znor73':['tango','haspp04exp2:10000/petra/momo/z-nor_073',['RdKoordinate'],True,False],
           'EXSU2_bpm':['tango','haspp04exp2:10000/motor/omsvme58_exp2/3','Position',True,False],
           'EXSU2_baffle':['tango','haspp04exp2:10000/motor/omsvme58_exp2/4','Position',True,False],
           'PS2_hleft':['tango','haspp04exp2:10000/motor/slt_exp/3','Position',True,False],
           'PS2_hright':['tango','haspp04exp2:10000/motor/slt_exp/4','Position',True,False],
           'PS2_vgap':['tango','haspp04exp2:10000/motor/slt_exp/5','Position',True,False],
           'PS2_voffset':['tango','haspp04exp2:10000/motor/slt_exp/6','Position',True,False],
           'pressure_exp':['tango','haspp04exp2:10000/p04/centerthree2.2/1.exp','Pressure',True,False],
           'pressure_cb':['tango','haspp04exp2:10000/p04/centerthree2.3/2.cb','Pressure',True,False],
           'pressure_gas':['tango','haspp04exp2:10000/p04/centerthree2.2/2.cb.gas','Pressure',True,False],
           'keithley1':['tango','haspp04exp2:10000/p04/keithley6517a/exp2.01','Current',True,False],
           'keithley2':['tango','haspp04exp2:10000/p04/keithley6517a/exp2.02','Current',True,False],
           'keithley3':['tango','haspp04exp2:10000/p04/keithley6517a/exp2.03','Current',True,False],
           'keithleyPIPE':['tango','haspp04exp2:10000/p04/pipekeithley/exp2.01','PhotoDiodeCurrent',True,False],           
           'monoenergy':['tango','haspp04exp2:10000/p04/monop04/exp2.01','Position',True,False],
           'monocff':['tango','haspp04exp2:10000/p04/monop04/exp2.01','Cff',True,False],      #NOT tested!!! combine with prior reading
           'mono':['tango','haspp04exp2:10000/motor/tm_monop04/1',['Position','Cff'],True,False],     #combination of all           
           'ring':['tango','haspp04exp2:10000/petra/globals/keyword','BeamCurrent',True,False],
           'mcp01':['tango','haspp04exp2:10000/p04/hviseg/exp2.81','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'mcp02':['tango','haspp04exp2:10000/p04/hviseg/exp2.82','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'mcp03':['tango','haspp04exp2:10000/p04/hviseg/exp2.83','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'mcp04':['tango','haspp04exp2:10000/p04/hviseg/exp2.84','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'mcp05':['tango','haspp04exp2:10000/p04/hviseg/exp2.85','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'mcp06':['tango','haspp04exp2:10000/p04/hviseg/exp2.86','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'mcp07':['tango','haspp04exp2:10000/p04/hviseg/exp2.87','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'mcp08':['tango','haspp04exp2:10000/p04/hviseg/exp2.88','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'mcp09':['tango','haspp04exp2:10000/p04/hviseg/exp2.89','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'mcp10':['tango','haspp04exp2:10000/p04/hviseg/exp2.90','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'mcp11':['tango','haspp04exp2:10000/p04/hviseg/exp2.91','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'mcp12':['tango','haspp04exp2:10000/p04/hviseg/exp2.92','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'mcp13':['tango','haspp04exp2:10000/p04/hviseg/exp2.93','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'mcp14':['tango','haspp04exp2:10000/p04/hviseg/exp2.94','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'mcp15':['tango','haspp04exp2:10000/p04/hviseg/exp2.95','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'mcp16':['tango','haspp04exp2:10000/p04/hviseg/exp2.96','MeasSenseVoltage',True,False],   # MCP detector voltages of cookie box branch 2
           'diode_int':['tango','haspp04exp1:10000/p04/keysightb2980/exp1.01','Current',True, False],# Keysight current from diode in intermediate focus branch1
           'beam_xang':['tango','haspp04exp2:10000/petra/parametercollector/keyword','BeamXAngleDeltaCell2',True, False],
           'beam_yang':['tango','haspp04exp2:10000/petra/parametercollector/keyword','BeamYAngleDeltaCell2',True, False],
           'beam_xpos':['tango','haspp04exp2:10000/petra/parametercollector/keyword','BeamXPosDeltaCell2',True, False],
           'beam_ypos':['tango','haspp04exp2:10000/petra/parametercollector/keyword','BeamYPosDeltaCell2',True, False]		   
           }
           
           
           
#'':('tango','','',True,False)        #reserve

#convenience access to make association in table safer
def GetP04Var(ID):
    if p04vars.has_key(ID):
        #v = p04vars[ID];
        #res = {};
        #for i in range(len(p04vars_attr))
        #    res[p04vars_attr[i]] = v[i]
                    
        #convenience: allow for single string of valID, need list of strings later, so convert
        _id = p04vars[ID];
        if type(_id[2])==str:
            _id[2] = [_id[2]]
            
        assert(type(_id[2])==list)
                    
        res = dict(zip(p04vars_attr,_id))
    else:
        sys.stderr.write('unknown p04 variable : ' + ID + '\n')
        res = dict()
    return res

#validate list of beamline variables
assert(type(p04vars)==dict)
for k in p04vars.values():
    assert(type(k)==list and len(k)==5)
    assert(type(k[0])==str)
    assert(type(k[1])==str)
    assert(type(k[2])==str or type(k[2])==list)    
    assert(type(k[3])==bool)
    assert(type(k[4])==bool)
for k in p04vars.keys():
    assert(type(k)==str)
    
