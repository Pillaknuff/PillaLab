#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: jseltmann
"""

__version__ = '0.3'
#0.21 - allowed strings as values
#0.2 - modified to: "with open()..."

import sys
sys.path.append('/common/p04/PythonLib/Testfacility')
from is_number import is_number

def ReadRef():
	"""
	Read P04-Reference-data
	Returns a dictionary
	"""
	Path='/common/p04/P04_reference_values.csv'		#/common/p04/reference_values_exp2.csv'
	
	P04_Ref = {}
	with open(Path, "r") as list:
		for line in list:
			nametag = line.index('_')
			valtag = line.index(';')
			if line[:nametag] not in P04_Ref:
				P04_Ref.update({line[:nametag]:{}})
			if '_in' in line:
				P04_Ref[line[:nametag]].update({line[nametag+1:line.index('_in')]:(float(line[valtag+1:]),)})
			elif ('_out' in line) and (line[nametag+1:line.index('_out')] in P04_Ref[line[:nametag]]):
				P04_Ref[line[:nametag]][line[nametag+1:line.index('_out')]] += (float(line[valtag+1:]),)
			elif 'pgm2_g' in line:
				if line[nametag+1:line.index('_au')] in P04_Ref[line[:nametag]]:
					P04_Ref[line[:nametag]][line[nametag+1:line.index('_au')]].update({line[line.index('au')+3:valtag]:float(line[valtag+1:])})
				else:
					P04_Ref[line[:nametag]].update({line[nametag+1:line.index('_au')]:{line[line.index('au')+3:valtag]:float(line[valtag+1:])}})
			else:
				if is_number(line[valtag+1:]):
					P04_Ref[line[:nametag]].update({line[nametag+1:valtag]:float(line[valtag+1:])})
				else:
					P04_Ref[line[:nametag]].update({line[nametag+1:valtag]:str(line[valtag+1:]).strip()})
	return P04_Ref

