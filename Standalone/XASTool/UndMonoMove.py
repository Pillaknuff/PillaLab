#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

@author: jseltmann
"""
# Use HDF5-file with 

__version__ = '1.31'
# 1.3 - arg_range and other argparse optimizations
# 1.23 - Removed datetime, structure of Logfile changed
# 1.22 - File-Counter changed
# 1.21 - New Limitcheck
# 1.2 - Changed name: Offset -> Factor 
# 1.15 - Added Branch 1, P04_Motors
# 1.10 - Log P, I, D in file
# 1.01 - extended try..except, SCANcheck, Fast-shutter
# 1.0 - Lower Limit adjusted, Start modified, Check for Und.State
# Jul 13, 2018, JB: Remembering and restoring shutter state on start of script; disabled guarantee that shutter is closed during approach phase
#

import matplotlib.pyplot as plt							#Plot result

from PyTango import DeviceProxy as DP
from epics import PV
import os
import sys
import time
import math
import argparse							#Getting input arguments
import traceback
import numpy as np
import socket

sys.path.append('/common/p04/PythonLib/')
from PID import PID
import P04_Motors
#from ReadReference import ReadRef						#Read P04-reference file as dict
#P04_Ref = ReadRef()

Path = '/gpfs/local/Beamline_data/P04_{}/{}/UndMonoFly/'.format(\
				time.strftime('%Y'), time.strftime('%m_%B'))

class arg_range(argparse.Action):
	def __init__(self, min=None, max=None, *args, **kwargs):
		self.min = min
		self.max = max
		kwargs["metavar"] = "{%s-%s}" % (self.min, self.max)
		super(arg_range, self).__init__(*args, **kwargs)
	
	def __call__(self, parser, namespace, value, option_string=None):
		if not (self.min <= value <= self.max):
			msg = 'invalid choice: %r (choose from {%s-%s})' % \
				(value, self.min, self.max)
			raise argparse.ArgumentError(self, msg)
		setattr(namespace, self.dest, value)

parser = argparse.ArgumentParser(description = \
		'Script for testing of undulatorgap speed. Results can be found at: {}'.\
		format(Path), formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-b', '--Branch', help='Which branch do you want to use?', \
		choices=['1', '2'], required=True, default=argparse.SUPPRESS)
parser.add_argument('-s', '--Start', help='Enter beginning point for energyscan in eV', \
		type=float, default=600., choices=xrange(250,3000), metavar="{250-3000}")
parser.add_argument('-e', '--End', help='Enter endpoint for energyscan in eV', \
		type=float, default=620., choices=xrange(250,3000), metavar="{250-3000}")
parser.add_argument('-sp', '--Speed', help='Enter speed of energyscan in eV/s.', \
		type=float, default=1.0, min=0.5, max=12, action=arg_range)
parser.add_argument('-f', '--Factor', help='Enter factor to undulator energy.', \
		type=float, default=1.0)
parser.add_argument('-o', '--Offset', help='Enter offset to undulator energy.', \
		type=float, default=0.0)
parser.add_argument('-r', '--Record', help='Record flux with BL-diode.', \
		action="store_true", default=argparse.SUPPRESS)
parser.add_argument('-t', '--Test', help='Test script without changing beamline.', \
		action="store_true", default=argparse.SUPPRESS)
args = parser.parse_args()

Dev_Map = P04_Motors.Device_Map(args.Branch)
Branch = str(int(DP(Dev_Map['smu_dir']['motor']).STELLUNG[0]))

if args.Branch != Branch:
	print('Wrong branch chosen/in use?!?')
	raw_input()
	sys.exit()

def func5(x, a, b, c, d, e, f):
	return a*x**5 + b*x**4 + c*x**3 + d*x**2 + e*x + f

popt = [ -1.66888684e-12,   1.73287403e-08,  -6.23129688e-05,
		1.03303527e-01,  -8.46723000e+01,   3.48410395e+04]

def UndOptSpd(Energy, Speed):
	return int(np.round(float(Speed) * (func5(Energy, *popt)),0))

os.environ["EPICS_CA_ADDR_LIST"] = "131.169.66.109 131.169.66.108"				#PGM1, PGM2

### Initiate components ###
Und = DP(Dev_Map['und']['motor'])
Und_En = DP(Dev_Map['und_en']['motor'])
SCAN = DP(Dev_Map['scan_info']['motor'])
shutter = DP(Dev_Map['beckhoff']['motor'])

Mono = DP(Dev_Map['mono']['motor'])
Mono_En = PV('HASPP04PMPGU{}:ENERGY_MON'.format(args.Branch))
Mono_Start = PV('HASPP04PMPGU{}:START_CMD.PROC'.format(args.Branch))

Screen = DP(Dev_Map['scr_aft_rmu']['motor'])
In_Diode = DP(Dev_Map['in_diode']['motor'])
Keith = DP(Dev_Map['keithley1']['motor'])

try:
	if SCAN.ScanActive == 0:
		ScanActFlag = False
		if str(Und.State()) == 'ON':
			SCAN.ScanActive = 1
			SCAN.ScanInfo = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) + '\nUndMonoMove @' + socket.gethostname()
			### check direction and range of movement
			if args.Start != args.End:		
				direction = math.copysign(1, args.End - args.Start)
				StartEnd = [args.Start - direction*20*args.Speed, \
								args.End + direction*10*args.Speed][::int(direction)]
				if Und_En.UnitLimitMin > StartEnd[0]:
					StartEnd[0] = float(Und_En.UnitLimitMin)
					print('Lower energy limit triggered.')
				if StartEnd[1] > Und_En.UnitLimitMax:
					StartEnd[1] = float(Und_En.UnitLimitMax)
					print('Upper energy limit triggered.')
				Start, End = StartEnd[::int(direction)]
			else:
				print("Can't use the same value for begin and end!")
				exit()
			
			### Prepare files ###
			Counter = 1
			
			if not os.path.exists(Path):
				os.makedirs(Path)
			Fil = '{}_LogFly{}_{}S_{}E_{}Spd'.format(\
				time.strftime("%Y%m%d"), \
				args.Branch, Start, End, args.Speed)
			files = os.listdir(Path)
			for file in files:
				if Fil in file:	
					if int(file[-7:-4].strip('_')) >= Counter:
						Counter = int(file[-7:-4].strip('_'))+1
			#print Counter
			File = '{}_{}.csv'.format(Fil, str(Counter).zfill(3))
			#print(File)
			Datei = open(Path+File, 'a')
			Datei.write('Time, Unrg, plcund.CurrentGap, Mnrg, U_Spd, P, I, D - {} eV/s, UFactor: {}, UOffset: {}, V{}\n\
	---------------------------------------------------------------------------------------------------------------------------------------------------\n'\
					.format(args.Speed, args.Factor, args.Offset, __version__))
			
			### Prepare components ###
			old_shutter_state = shutter.Input0;    #remember shutter state (is restored when target is reached)
			#old_shutter_state = shutter.Value15
			#if old_shutter_state: 
			shutter.Input0 = -1			#close fast-shutter
			if args.Record: 
				In_Diode.Position = 1
				Keith.CurrIntegrationPeriod = 1
				#Keith.CurrRange = 2e-4
				Keith.CurrAutoRange = 1
			Und.DesiredSpeed = 330000
			Und_En.Position = args.Factor*Start + args.Offset		  #Move undulator to Start
			PV('HASPP04PMPGU{}:ENERGY_SP'.format(args.Branch)).put(Start)		#Move mono to Start
			
			while (PV('HASPP04PMPGU{}:ERDY_STS'.format(args.Branch)).get() != 1 or \
					abs(Mono_En.get()-Start) > 0.1) or ('MOVING' in str(Und.State()) or \
					abs(Und_En.Position-(args.Factor*Start + args.Offset)) > 0.1):
				time.sleep(0.1)
			
			Und_En.PositionSim = args.Factor*End + args.Offset							#calc gap for End
			time.sleep(0.1)
			Und.DesiredGap = float(Und_En.ResultSim[15:])*1000	
			
			N_Spd = args.Speed * 10000		#UndOptSpd(args.Factor*Start + args.Offset, args.Speed)
			Und.DesiredSpeed = N_Spd
			
			if args.Speed >= 0.5:
				PV('HASPP04PMPGU{}:EVSTART_SP'.format(args.Branch)).put(Start)	#*args.Factor)
				PV('HASPP04PMPGU{}:EVSTOP_SP'.format(args.Branch)).put(End)	#*args.Factor)
				PV('HASPP04PMPGU{}:EVVELO_SP'.format(args.Branch)).put(args.Speed)
			
			Pa = 200.*args.Speed#*0.9+np.random.random(1)[0]/5
			Ia = 2*args.Speed
			Da = 1600.#*args.Speed
			p = PID(Pa,Ia,Da)
			if args.Record:
				Log = [[time.time(), Und_En.Position, Und.CurrentGap, Mono_En.get(), 0, Keith.CurrentWithTimestamp[0], 0, 0, 0]]
			else:
				Log = [[time.time(), Und_En.Position, Und.CurrentGap, Mono_En.get(), 0, 0, 0, 0]]
			Unrg = args.Factor*Start + args.Offset
			CycT = 1#0.3#0.05
			time .sleep(2)
			
			### Start run ###
			print('Start UndMonoMove')
			
			if args.Speed >= 0.5: 
				Mono_Start.put(1)
			Und.StartMove()
			time.sleep(0.1)
			Und.DesiredSpeed = N_Spd/10
			while (PV('HASPP04PMPGU{}:ERDY_STS'.format(args.Branch)).get() != 1):
				time.sleep(0.05)
			Und.DesiredSpeed = N_Spd
			Mnrg = np.round(Mono_En.get(),3)
			while direction*(End - Mnrg)>2:
				shutter.Input0 = -2
				#if (Unrg - (direction*args.Start - direction*1) >= 0) and not shutter.Value15: shutter.Input0 = -2
				time.sleep(CycT)
				
				Un = np.round(Und_En.Position,3)
				Unrg = (Un - args.Offset)/args.Factor
				Mnrg = np.round(Mono_En.get(),3)
				
				Time = time.time()
				deltaT = Time-Log[-1][0]								#Timedelta
				if args.Record:
					Log.append([Time, Un, Und.CurrentGap, Mnrg, N_Spd, Keith.CurrentWithTimestamp[0]])
				else:
					Log.append([Time, Un, Und.CurrentGap, Mnrg, N_Spd])
				EDiff = direction *(Mnrg/args.Factor - Unrg)		   #Energy difference: Positive when Und lags
				
				if 0.5 <= args.Speed <= 12:
					if (direction*(Log[-1][1]-Log[-2][1]) >= 0) and (direction*(Log[-1][3]-Log[-2][3]) >= 0):			#Falls beide Bewegungen in die richtige Richtung zeigen
						Pa, Ia, Da = p.update(EDiff, deltaT)
						N_Spd = int(np.round(N_Spd + Pa + Ia + Da,0))
						if N_Spd > 330000:
							N_Spd = 330000
							print('Careful, maximum speed reached!')
						elif N_Spd < 1000:
							N_Spd = 1000
							print('Ups, minimum speed reached!')
						Und.DesiredSpeed = N_Spd
						#if len(Log) > 10:
						#	if (sum(np.array(Log)[:,-4]) < 18000) and (PV('HASPP04PMPGU2:ERDY_STS').get() == 1):
						#		raise Exception('Mono not moving!')
						#	Log.pop(1)
				#else:
				#	CycT = 1
				#	N_Spd = UndOptSpd(Unrg, args.Speed)
				#	if N_Spd > 330000:
				#		N_Spd = 330000
				#	elif N_Spd < 100:
				#		N_Spd = 100
				#	Und.DesiredSpeed = N_Spd
				#	#print('EDiff: ' + str(round(EDiff, 3)))
				#	PV('HASPP04PMPGU{}:ENERGY_SP'.format(args.Branch)).put(Unrg+5*args.Speed*deltaT-EDiff/2)		
				Log[-1].extend([Pa, Ia, Da])
				Datei.write(str(Log[-1])[1:-1]+ '\n')	
			
			D = np.array(Log)
#			plt.figure(File)
#			plt.plot(D[:,3],D[:,1]-D[:,3])
#			plt.xlim((StartEnd[0], StartEnd[1]))
#			plt.xlabel('Mono energy [eV]')
#			plt.ylabel('Difference Und-Mono [eV]')
#			plt.grid()
#			plt.show()

			shutter.Input0 = old_shutter_state
			
		else:
			print('Undulator has problems, please check...')
	else:
		print("There is another scan active: {}".format(SCAN.ScanInfo))
		ScanActFlag = True
except:
	ex = sys.exc_info()
	print("Exception!")
	Datei.write(str(traceback.print_tb(ex[2])) + "\n" + str(ex[1]))
	
finally:
	Und.StopMove()
	PV('HASPP04PMPGU{}:ENERGY_ST_CMD.PROC'.format(args.Branch)).put(1)
	if not ScanActFlag:
		SCAN.ScanActive = 0
		SCAN.ScanInfo = ''
	Und.DesiredSpeed = 330000
	Datei.close()
