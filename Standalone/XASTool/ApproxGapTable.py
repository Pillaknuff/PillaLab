#
# The module is used to find optimal linear approximations to the gap table polynomial
# On-The-fly scans could benefit strongly by using this approximation instead of the 
# PID-controlled undulator speed at low velocities.
#
# This code is a reimplemented version for Python from an early MATLAB version (linear_gap_scan.m)
#
#
# Jens Buck, Sep 28, 2020
#

import sys
import argparse
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# conversion factor "undulator speed units" to um/s
gap_v_fac = 0.00856   

# conversion energy[ev] to gap [um], validity 250..2800 eV
hv_min = 250
hv_max = 2800
gap_poly = np.flip( np.array((-182.373, 66.0876, -0.0998202, 0.000108309, -7.35106e-008, 2.97597e-011, -6.53755e-015, 5.97685e-019 )),0)
dgap_poly = np.polyder(gap_poly)
def gap(hv):
	""" undulator gap [um] as a function of photon energy [eV] """
	assert(np.all((hv_min-5<=hv) & (hv<=hv_max+5)))
	return np.polyval(gap_poly, hv)
def dgap(hv):
	""" Derivative of gap polynomial representing relativer velocities on the 
	gap scale to achieve constant rates ion energy scale
	"""
	assert(np.all((hv_min-5<=hv) & (hv<=hv_max+5)))
	return np.polyval(dgap_poly, hv)

# compute inverse polynomial
hv_ = np.exp( np.arange(np.log(hv_min), np.log(hv_max),0.01) )
hv_poly = np.polyfit(gap(hv_),hv_ ,12)
gap_min = gap(hv_min)
gap_max = gap(hv_max)

def hv(gap): 
	"""photon energy [eV] as a function of gap [um]"""
	assert(np.all((gap_min-100<=gap) & (gap<=gap_max+100)))
	return np.polyval(hv_poly, gap)

def RelFlux(hv_mono, hv_undu): 
	""" approximate flux loss due to detuned mono and undulator """
	return np.exp(-0.5*((hv_mono-hv_undu)/(hv_undu/72))**2)

def TargetFun(p_lin, hv_ ):
	"""	function to be minimized: given a linear approximation 
	to the gap curve in an interval, 
	calculate the worst case relative intensity loss """
	return -np.min(RelFlux(hv_, hv( np.polyval(p_lin, hv_) )))

def GuessParam(hv_start,hv_end):
	"""
	make naive guess of linear approximation by using a simple linear fit without considering intensity loss.
	
	hv_start and hv_end must be scalar
	returns 1st order polynomial
	"""
	hv_start= float(hv_start)
	hv_end = float(hv_end)
	if hv_start>hv_end: hv_start,hv_end = hv_end,hv_start 
	hv_ = np.arange(max(hv_min, hv_start), 
	                min(hv_max, hv_end) + 1.,
					min(1, abs(hv_start-hv_end)/21)  )
	return np.polyfit(hv_, gap(hv_), 1)

def GetLinApprox(hv_start, hv_end):
	""" minimize TargetFunction in an interval (discrete points)in order 
	to determine best linear approximation to gap function.
	
	hv_start and hv_end must be scalar.
	Returns coefficients of 1st order polynomial."""
	hv_ = np.arange(max(hv_min,hv_start), min(hv_max,hv_end), 0.1)
	p0 = minimize(lambda x:TargetFun(x, hv_),
	              GuessParam(hv_start, hv_end),
	              method='nelder-mead',
				  options={'xatol':1e-8, 'disp':False})
	return p0
	
def MakeScanParams(hv_start, hv_end, hv_speed):
	""" Calculate undulator speed and starting point 
	as well as some diagnostic data from the given scan params
	
	returns a dict of parameters"""
	scan_time = (hv_end-hv_start)/hv_speed;
		
	# make approximation
	p_lin = GetLinApprox(hv_start, hv_end)
	
	gap_start = np.polyval(p_lin['x'], hv_start)	#gap start value (differs from gap table!)
	gap_v = p_lin['x'][0]*hv_speed   # gap speed in um/s
	gap_v_undu = np.round( gap_v/gap_v_fac )   #  ...in undu speed units (integer required!?)
	
	# calculate results
	scan_t = np.arange(0, scan_time+1, 0.1)
	hv_scan = hv( np.polyval((gap_v, gap_start,), scan_t))  # real energy over time	
	hv_theo = np.polyval((hv_speed, hv_start), scan_t)  # values of the ideal scan
		
	
	return {'mono_start':hv_start,
	        'mono_end':hv_end,
	        'mono_speed':hv_speed,
			'scan_time':scan_time,
			'undu_start':gap_start,
			'undu_speed_um':gap_v,
			'undu_speed':gap_v_undu,
			'hv_axis':hv_theo,
			'hv_diff':hv_scan-hv_theo,
			'flux_diff': RelFlux(hv_theo, hv_scan),
			'flux_worst':-p_lin['fun']
			}
	
if __name__=="__main__":
		
		
	#Cannot be debugged, is just crashing all the time...
	
	"""
	#to do: read params from command line args
	# options: "plot figure", "display output string"...
	
	parser = argparse.ArgumentParser(description='Calculate on-the-fly scan with linearized gap polynomial')
	parser.add_argument('-s', '--start', nargs=1, help='start energy of scan/ eV', action = 'store', default = None, type = float, required = True)
	parser.add_argument('-e','--end', nargs=1, help='end energy of scan/ eV', action = 'store', default = None, type = float, required = True)
	parser.add_argument('-v','--velocity', nargs=1, help='scan speed / eV*s^-1', action = 'store', default = 1., type = float)
	
	parser.add_argument('-t','--text', help='display results on stdout', action='store_true', default = False)
	parser.add_argument('-f','--fig', help='display result figure', action = 'store_true', default = False)
	
	parser.print_help() 
	
	#parser.parse_args(sys.argv)
		
	"""
	
	#todo: evaluate cmd params
	
	hv_start = 615   #eV
	hv_end = 680	#eV
	hv_speed = 0.5   #eV/s 
	disp_outstr = True
	disp_fig = True
	
	par = MakeScanParams(hv_start,hv_end,hv_speed)
	
	if disp_outstr or disp_fig:
		#make output string	
		out_str = \
		"scan parameters\n" +\
		"\tstart\t{:8.3f} eV ; {:8.3f} um\n".format(hv_start, gap(hv_start)) +\
		"\tend\t{:8.3f} eV ; {:8.3f} um\n".format(hv_end, gap(hv_end)) +\
		"\tscan speed\t{:8.3f} eV/s\n".format(hv_speed) +\
		"\tscan duration\t{:8.3f} s\n".format(par["scan_time"]) +\
		"\tgap speed\t{:8.1f} um/s ; {:8.0f} undu units\n".format(par["undu_speed_um"], par["undu_speed"]) +	\
		"undu: energy deviation vs. ideal\n" +\
		"\tminimum\t{:8.3f} eV\n".format(min(par["hv_diff"])) +\
		"\tmaximum\t{:8.3f} eV\n".format(max(par["hv_diff"])) +\
		"\tRMS\t{:8.3f} eV\n".format(np.sqrt(np.mean((par["hv_diff"])**2))) +\
		"intensity with mono/undu mismatch\n" +\
		"\tworst case\t{:8.1f} %\n".format(par["flux_worst"]*100) +\
		"\taverage\t{:8.1f} %".format(  np.mean(par["flux_diff"] )*100 )	
		if disp_outstr: print ('\n\n'+out_str)
	else:
		out_str = ''
	
	if disp_fig:
		#display results
		title_style = {'fontsize': 12,
					'fontweight': 'bold',
					'color':'k',
					'verticalalignment': 'top',
					'horizontalalignment': 'center'}
	
		text_style = {'fontsize': 9,
					'fontweight': 'normal',
					'color':'k',
					'verticalalignment': 'top',
					'horizontalalignment': 'center'}
		
		fig, ax = plt.subplots(3)
		ax[1].plot(par["hv_axis"], par["hv_diff"])
		#ax[1].set_size(9)
		t = ax[1].set_title('energy mismatch /  eV', fontdict = title_style, y = 0.9)	
		ax[1].set_xticklabels(('')*len( ax[1].get_xticklabels() ))   #remove ticks
		ax[1].grid(which='both')
			
		ax[2].plot(par["hv_axis"], par["flux_diff"]*100)
		#ax[2].set_size(9)
		ax[2].set_xlabel('photon energy /  eV')
		t = ax[2].set_title('relative flux / %',fontdict = title_style, y = 0.9)
		ax[2].grid(which='both')
			
		#ax[0].set_size(9)
		t = ax[0].set_title(out_str.replace('\t',' '*8), fontdict = text_style, y = 0.9)
		ax[0].title.set_verticalalignment('top')
		ax[0].title.set_horizontalalignment('left')
		ax[0].title.set_position((0.1,0.93))
		ax[0].set_xticklabels(('')*len( ax[0].get_xticklabels() ))   #remove ticks
		ax[0].set_yticklabels(('')*len( ax[0].get_xticklabels() ))   #remove ticks
	
		fig.show()
	
	
	