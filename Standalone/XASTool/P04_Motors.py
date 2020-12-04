#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Usage:
	import P04_Motors
	P04_Map = P04_Motors.Device_Map([BRANCH])
		[BRANCH] should be a string in ['', '1', '2'] for Frontend, Branch1 or Branch2
		
Used in:
	BStatus_ELog
	ComServer
	GapEnergy
	Helicity
	InsertDiode
	UndMonoMove
	WL_Scan
	WhatsWrong
	
Usage for cam_map:
import P04_Motors
cam_map = P04_Motors.cam_map()
cam01=cam_map['coupling_cam']['server']

	
'''
__version__ = '0.2'


def Device_Map(Branch):
	D_M = {\
	'scan_info': {'motor': 'haspp04exp2:10000/p04/scaninfop04/exp2.01', 'attribute': ['ScanActive', 'ServerActive']}, \
	'keithley_kill': {'motor': 'haspp04exp2:10000/p04/soft_kill_switch/01', 'attribute': ['ScanTime', 'ScanTime2'],\
					'info': 'kill switch keithley-panel branch1 and branch2'}, \
	'petra': {'motor': 'haspp04exp2:10000/petra/globals/keyword', 'attribute': ['BeamCurrent']}, \
	'momos': {'motor': 'haspp04exp2:10000/petra/momo/x-nor_011', 'attribute': ['RdKoordinate'], \
					'info': 'Reads all Momo values simultaneously with RdKoordinate. \
							Values for PU04-Momos 73 and 78 are listed at X:[18, 106] and Z:[19, 107]'}, \
	'und': {'motor': 'haspp04exp2:10000/p04/plcundulator/1', 'attribute': ['CurrentGap', 'CurrentShift', 'CurrentTaper', 'CurrentSpeed']}, \
	'und_en': {'motor': 'haspp04exp2:10000/p04/undulatorp04/exp2.01', 'pool': 'haspp04exp2:10000/motor/tm_undp04/1'}, \
	'ps1_vgap': {'motor': 'haspp04exp1:10000/p04/motor/ps2.03', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/3'}, \
	'ps1_voff': {'motor': 'haspp04exp1:10000/p04/motor/ps2.04', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/4'}, \
	'oam1_x': {'motor': 'haspp04exp2:10000/p04/spk/exp.02'}, \
	'oam1_rotz': {'motor': 'haspp04exp2:10000/p04/spk/exp.01'}, \
	'oam2_x': {'motor': 'haspp04exp2:10000/p04/spk/exp.04'}, \
	'oam2_rotz': {'motor': 'haspp04exp2:10000/p04/spk/exp.03'}, \
	'ps2_left': {'motor': 'haspp04exp1:10000/p04/motor/ps2.15', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/15'}, \
	'ps2_right': {'motor': 'haspp04exp1:10000/p04/motor/ps2.16', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/16'}, \
	'ps2_vgap': {'motor': 'haspp04exp1:10000/p04/motor/ps2.11', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/11'}, \
	'ps2_voff': {'motor': 'haspp04exp1:10000/p04/motor/ps2.12', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/12'}, \
	'smu_x': {'motor': 'haspp04exp1:10000/p04/motor/ps2.18', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/18'}, \
	'smu_z': {'motor': 'haspp04exp1:10000/p04/motor/ps2.17', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/17'}, \
	'smu_rotz': {'motor': 'haspp04exp1:10000/p04/motor/ps2.19', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/19'}, \
	'smu_dir': {'motor': 'haspp04exp2:10000/hasylab/petra3_p04vil.cdi.srv/sp_2', 'attribute': ['STELLUNG']}, \
	}
	if str(Branch) in ['1', '2']:
		Branches = {\
		'branch1': {\
		'ps3_left': {'motor': 'haspp04exp1:10000/p04/motor/ps2.01', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/1'}, \
		'ps3_top': {'motor': 'haspp04exp1:10000/p04/motor/ps2.05', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/5'}, \
		'ps3_right': {'motor': 'haspp04exp1:10000/p04/motor/ps2.09', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/9'}, \
		'ps3_bottom': {'motor': 'haspp04exp1:10000/p04/motor/ps2.13', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/13'}, \
		'scr_aft_smu': {'motor': 'haspp04exp1:10000/p04/motor/ps2.07', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/7'}, \
		'mono': {'motor': 'haspp04exp1:10000/p04/monop04/exp1.01'}, \
		'scr_aft_mono': {'motor': 'haspp04exp1:10000/p04/motor/exp1.05', 'pool': 'haspp04exp1:10000/motor/omsvme58_exp1/5'}, \
		'exsu_vg': {'motor': 'haspp04exp1:10000/p04/motor/exp1.01', 'pool': 'haspp04exp1:10000/motor/omsvme58_exp1/1'}, \
		'exsu_trans': {'motor': 'haspp04exp1:10000/p04/motor/exp1.02', 'pool': 'haspp04exp1:10000/motor/omsvme58_exp1/2'}, \
		'exsu_left': {'motor': 'haspp04exp1:10000/p04/motor/exp1.03', 'pool': 'haspp04exp1:10000/motor/omsvme58_exp1/3', \
						'info': 'YAG'}, \
		'exsu_right': {'motor': 'haspp04exp1:10000/p04/motor/exp1.04', 'pool': 'haspp04exp1:10000/motor/omsvme58_exp1/4', \
						'info': 'Baffle'}, \
		'exsu_slit': {'motor': 'haspp04exp1:10000/p04/vmexecutor/exitslit_1.01', 'pool': 'haspp04exp1:10000/motor/vm_slit_exsu1/1', \
						'info': 'Width in micrometer'}, \
		'scr_aft_exsu': {'motor': 'haspp04exp1:10000/p04/motor/exp1.06', 'pool': 'haspp04exp1:10000/motor/omsvme58_exp1/6'}, \
		'beckhoff': {'motor': 'haspp04exp1:10000/p04/haspp04beck10/exp1', \
					'attribute': ['Value0', 'Value1', 'Value2', 'Value3', 'Value4', 'Value5',\
								'Value6', 'Value7', 'Value10', 'Value15', 'Value20', \
								'Input1', 'Input2', 'Input3', 'Input4']}, \
		'rmu_vx': {'motor': 'haspp04exp1:10000/p04/rmu1/vx', 'pool': 'haspp04exp1:10000/motor/tm_rmu1_vx/1'}, \
		'rmu_vy': {'motor': 'haspp04exp1:10000/p04/rmu1/vy', 'pool': 'haspp04exp1:10000/motor/tm_rmu1_vy/1'},	
		'rmu_vz': {'motor': 'haspp04exp1:10000/p04/rmu1/vz', 'pool': 'haspp04exp1:10000/motor/tm_rmu1_vz/1'},	
		'rmu_vrotx': {'motor': 'haspp04exp1:10000/p04/rmu1/vrotx', 'pool': 'haspp04exp1:10000/motor/tm_rmu1_vrotx/1'}, \
		'rmu_vroty': {'motor': 'haspp04exp1:10000/p04/rmu1/vroty', 'pool': 'haspp04exp1:10000/motor/tm_rmu1_vroty/1'},
		'rmu_vrotz': {'motor': 'haspp04exp1:10000/p04/rmu1/vrotz', 'pool': 'haspp04exp1:10000/motor/tm_rmu1_vrotz/1'}, 		 	
		'rmu_hz': {'motor': 'haspp04exp1:10000/p04/rmucoordinate/rmu1_hz', 'pool': 'haspp04exp1:10000/motor/tm_rmu1_hz/1'}, \
		'rmu_hx': {'motor': 'haspp04exp1:10000/p04/rmucoordinate/rmu1_hx', 'pool': 'haspp04exp1:10000/motor/tm_rmu1_hx/1'}, 
		'rmu_hy': {'motor': 'haspp04exp1:10000/p04/rmucoordinate/rmu1_hy', 'pool': 'haspp04exp1:10000/motor/tm_rmu1_hy/1'},
		'rmu_hrotx': {'motor': 'haspp04exp1:10000/p04/rmucoordinate/rmu1_hrotx', 'pool': 'haspp04exp1:10000/motor/tm_rmu1_hrotx/1'},	
		'rmu_hroty': {'motor': 'haspp04exp1:10000/p04/rmucoordinate/rmu1_hroty', 'pool': 'haspp04exp1:10000/motor/tm_rmu1_hroty/1'},
		'rmu_hrotz': {'motor': 'haspp04exp1:10000/p04/rmucoordinate/rmu1_hrotz', 'pool': 'haspp04exp1:10000/motor/tm_rmu1_hrotz/1'}, \
		'pressure_cb': {'motor': 'haspp04exp1:10000/p04/centerthree/1.diff', 'attribute': ['Pressure']}, \
		'scr_aft_rmu': {'motor': 'haspp04exp1:10000/p04/motor/exp1.07',  'pool': 'haspp04exp1:10000/motor/omsvme58_exp1/7'}, \
		'in_diode': {'motor': 'haspp04exp1:10000/p04/vmexecutor/insertdiode.1'}, \
		'keithley1_ctrl': {'motor': 'haspp04exp1:10000/p04/gpibdeviceserver/exp1.01'}, \
		'keithley1': {'motor': 'haspp04exp1:10000/p04/keithley6517a/exp1.01', 'attribute': ['Current', 'CurrRange', 'CurrIntegrationPeriod'],\
						'property': ['GpibDevice'], 'info': 'Diode'}, \
		'pressure_diff1': {'motor': 'haspp04exp1:10000/p04/centerthree/1.diff', 'attribute': ['Pressure']}, \
		'pressure_exp': {'motor': 'haspp04exp1:10000/p04/centerthree/1.exp', 'attribute': ['Pressure']}, \
		'interm_trans_x': {'motor': 'haspp04exp1:10000/p04/motor/exp1_2.01',
				'pool': 'haspp04exp1:10000/motor/omsvme58_exp1/17'}, \
		'maxp04_stage_x': {'motor': 'haspp04exp1:10000/p04/motor/exp1_2.02',
				'pool': 'haspp04exp1:10000/motor/omsvme58_exp1/18'}, \
		'maxp04_stage_y': {'motor': 'haspp04exp1:10000/p04/motor/exp1_2.03',
				'pool': 'haspp04exp1:10000/motor/omsvme58_exp1/19'}, \
		'maxp04_stage_z': {'motor': 'haspp04exp1:10000/p04/motor/exp1_2.04',
				'pool': 'haspp04exp1:10000/motor/omsvme58_exp1/20'}, \
		'pinhole_diode': {'motor': 'haspp04exp1:10000/p04/motor/exp1_2.07', 'pool': 'haspp04exp1:10000/motor/omsvme58_exp1/23'}, \
		'coupling': {'motor': 'haspp04exp1:10000/p04/motor/exp1_2.08', 'pool': 'haspp04exp1:10000/motor/omsvme58_exp1/24'}, \
		'pinhole_vert': {'motor': 'haspp04exp1:10000/p04/smaractmotor/exp.01',
				'pool': 'haspp04exp1:10000/motor/tm_smaractmotor_exp/1'}, \
		'pinhole_hor': {'motor': 'haspp04exp1:10000/p04/smaractmotor/exp.02',
				'pool': 'haspp04exp1:10000/motor/tm_smaractmotor_exp/2'}, \
		'beamstop_vert': {'motor': 'haspp04exp1:10000/p04/smaractmotor/exp.05',
				'pool': 'haspp04exp1:10000/motor/tm_smaractmotor_exp/5'},
		'beamstop_hor': {'motor': 'haspp04exp1:10000/p04/smaractmotor/exp.04',
				'pool': 'haspp04exp1:10000/motor/tm_smaractmotor_exp/4'}, \
		'maxp04_diode_hor': {'motor': 'haspp04exp1:10000/p04/smaractmotor/exp.07',
				'pool': 'haspp04exp1:10000/motor/tm_smaractmotor_exp/7'},
		'maxp04_diode_vert': {'motor': 'haspp04exp1:10000/p04/smaractmotor/exp.06',
				'pool': 'haspp04exp1:10000/motor/tm_smaractmotor_exp/6'}, \
		}, \
		
		'branch2': {\
		'ps3_left': {'motor': 'haspp04exp1:10000/p04/motor/ps2.02', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/2'}, \
		'ps3_top': {'motor': 'haspp04exp1:10000/p04/motor/ps2.14', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/14'}, \
		'ps3_right': {'motor': 'haspp04exp1:10000/p04/motor/ps2.10', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/10'}, \
		'ps3_bottom': {'motor': 'haspp04exp1:10000/p04/motor/ps2.06', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/6'}, \
		'scr_aft_smu': {'motor': 'haspp04exp1:10000/p04/motor/ps2.8', 'pool': 'haspp04exp1:10000/motor/omsvme58_motor_ps2/8'}, \
		'mono': {'motor': 'haspp04exp2:10000/p04/monop04/exp2.01', \
				'pool': 'haspp04exp2:10000/motor/tm_monop04/1'}, \
		'scr_aft_mono': {'motor': 'haspp04exp2:10000/p04/motor/exp2.05', 'pool': 'haspp04exp2:10000/motor/omsvme58_exp2/5'}, \
		'exsu_vg': {'motor': 'haspp04exp2:10000/p04/motor/exp2.01', 'pool': 'haspp04exp2:10000/motor/omsvme58_exp2/1'}, \
		'exsu_trans': {'motor': 'haspp04exp2:10000/p04/motor/exp2.02', 'pool': 'haspp04exp2:10000/motor/omsvme58_exp2/2'}, \
		'exsu_left': {'motor': 'haspp04exp2:10000/p04/motor/exp2.03', \
					'pool': 'haspp04exp2:10000/motor/omsvme58_exp2/3', \
					'info': 'YAG'}, \
		'exsu_right': {'motor': 'haspp04exp2:10000/p04/motor/exp2.04', \
						'pool': 'haspp04exp2:10000/motor/omsvme58_exp2/4', \
						'info': 'Baffle'}, \
		'exsu_slit': {'motor': 'haspp04exp2:10000/p04/vmexecutor/exitslit.02', 'pool': 'haspp04exp2:10000/motor/vm_slit_exsu2/1'}, \
		'scr_aft_exsu': {'motor': 'haspp04exp2:10000/p04/motor/exp2.10', 'pool': 'haspp04exp2:10000/motor/omsvme58_exp2/10'}, \
		'beckhoff': {'motor': 'haspp04exp2:10000/p04/Beckhoff02p04/exp2.01', \
					'attribute': ['Value0', 'Value1', 'Value2', 'Value3', 'Value4', 'Value5',\
								'Value9', 'Value10', 'Value11', 'Value15', 'Value20', \
								'Input3', 'Input4', 'Input5', 'Input6', 'Input7', 'Input8', 'Input9', 'Input10']}, \
		'rmu_vx': {'motor': 'haspp04exp1:10000/p04/rmup04/rmu2.vx', 'pool': 'haspp04exp1:10000/motor/tm_rmup04_rmu2/10'}, \
		'rmu_vy': {'motor': 'haspp04exp1:10000/p04/rmup04/rmu2.vy', 'pool': 'haspp04exp1:10000/motor/tm_rmup04_rmu2/11'}, \
		'rmu_vz': {'motor': 'haspp04exp1:10000/p04/rmup04/rmu2.vz', 'pool': 'haspp04exp1:10000/motor/tm_rmup04_rmu2/12'}, \
		'rmu_vrotx': {'motor': 'haspp04exp1:10000/p04/rmup04/rmu2.vrotx', 'pool': 'haspp04exp1:10000/motor/tm_rmup04_rmu2/7'}, \
		'rmu_vroty': {'motor': 'haspp04exp1:10000/p04/rmup04/rmu2.vroty', 'pool': 'haspp04exp1:10000/motor/tm_rmup04_rmu2/8'}, \
		'rmu_vrotz': {'motor': 'haspp04exp1:10000/p04/rmup04/rmu2.vrotz', 'pool': 'haspp04exp1:10000/motor/tm_rmup04_rmu2/9'}, \
		'rmu_hx': {'motor': 'haspp04exp1:10000/p04/rmup04/rmu2.hx', 'pool': 'haspp04exp1:10000/motor/tm_rmup04_rmu2/4'}, \
		'rmu_hy': {'motor': 'haspp04exp1:10000/p04/rmup04/rmu2.hy', 'pool': 'haspp04exp1:10000/motor/tm_rmup04_rmu2/5'}, \
		'rmu_hz': {'motor': 'haspp04exp1:10000/p04/rmup04/rmu2.hz', 'pool': 'haspp04exp1:10000/motor/tm_rmup04_rmu2/6'}, \
		'rmu_hrotx': {'motor': 'haspp04exp1:10000/p04/rmup04/rmu2.hrotx', 'pool': 'haspp04exp1:10000/motor/tm_rmup04_rmu2/1'}, \
		'rmu_hroty': {'motor': 'haspp04exp1:10000/p04/rmup04/rmu2.hroty', 'pool': 'haspp04exp1:10000/motor/tm_rmup04_rmu2/2'}, \
		'rmu_hrotz': {'motor': 'haspp04exp1:10000/p04/rmup04/rmu2.hrotz', 'pool': 'haspp04exp1:10000/motor/tm_rmup04_rmu2/3'}, \
		'pressure_cb': {'motor': 'haspp04exp2:10000/p04/centerthree2.3/2.cb', 'attribute': ['Pressure']}, \
		'scr_aft_rmu': {'motor': 'haspp04exp2:10000/p04/motor/exp2.07',  'pool': 'haspp04exp2:10000/motor/omsvme58_exp2/7'}, \
					'in_diode': {'motor': 'haspp04exp2:10000/p04/vmexecutor/insertdiode.2'}, \
		'keithley1_ctrl': {'motor': 'haspp04exp2:10000/p04/gpibdeviceserver/exp2.01'}, \
		'keithley1': {'motor': 'haspp04exp2:10000/p04/keithley6517a/exp2.01', 'attribute': ['Current', 'CurrRange', 'CurrIntegrationPeriod'], \
						'property': ['GpibDevice'], 'info': 'Diode'}, \
		'keithley2_ctrl': {'motor': 'haspp04exp2:10000/p04/gpibdeviceserver/keithley2_b2'}, \
		'keithley2': {'motor': 'haspp04exp2:10000/p04/keithley6517a/keithley2_b2', 'attribute': ['Current', 'CurrRange', 'CurrIntegrationPeriod'], \
						'property': ['GpibDevice'], 'info': 'Mesh'}, \
		'pressure_diff2': {'motor': 'haspp04exp2:10000/p04/centerthree2.3/3.diff2', 'attribute': ['Pressure']}, \
		'pressure_exp': {'motor': 'haspp04exp2:10000/p04/centerthree2.2/1.exp', 'attribute': ['Pressure']}, \
		'scr_bef_pipe': {'motor': 'haspp04exp2:10000/p04/motor/exp2.11', 'pool': 'haspp04exp2:10000/motor/omsvme58_exp2/11'}, \
		'scr_aft_pipe': {'motor': 'haspp04exp2:10000/p04/motor/exp2.12', 'pool': 'haspp04exp2:10000/motor/omsvme58_exp2/12'}, \
		'leakvalve_cb2': {'motor': 'haspp04exp2:10000/p04/motor/exp2.13','pool': 'haspp04exp2:10000/motor/omsvme58_exp2/13'}, \
			}}
		D_M.update(Branches['branch{}'.format(Branch)])
	return D_M

def cam_map():
	#c_m = collections.OrderedDict()
	c_m = {\
	'106_coupling_cam': {'server': 'tango://haspp04interm:10000/p04/tangovimba/coupling_cam', 'server_name':'TangoVimba/Coupling', 'host':'haspp04interm'},
	'107_pinhole_cam': {'server': 'tango://haspp04interm:10000/p04/tangovimba/pinhole_cam', 'server_name':'TangoVimba/Pinhole','host':'haspp04interm'  },
	'108_maxp04_cam': {'server': 'tango://haspp04interm:10000/p04/tangovimba/MaxP04_cam', 'server_name':'TangoVimba/MaxP04', 'host':'haspp04interm' },
	'205_bm_bef_PIPE': {'server': 'tango://haspp04exp2:10000/p04/tangovimba/bm_bef_pipe', 'server_name':'TangoVimba/bm_bef_pipe', 'host':'haspp04exp2' },
	'206_bm_after_PIPE': {'server': 'tango://haspp04exp2:10000/p04/tangovimba/bm_aft_pipe', 'server_name':'TangoVimba/bm_aft_pipe', 'host':'haspp04exp2' },
	'202_bm_after_PGM2': {'server': 'tango://haspp04exp2:10000/p04/tangovimba/bm_aft_pgm2', 'server_name':'TangoVimba/bm_aft_pgm2', 'host':'haspp04exp2' },
	'201_cam09_aft_SMU2': {'server': 'tango://haspp04exp2:10000/p04/tangovimba/cam09', 'server_name':'TangoVimba/cam09', 'host':'haspp04exp2' },
	'101_cam10_aft_SMU1': {'server': 'tango://haspp04exp2:10000/p04/tangovimba/cam10', 'server_name':'TangoVimba/bm_aft_smu1', 'host':'haspp04exp2' },
	'203_exsu2': {'server': 'tango://haspp04exp2:10000/p04/tangovimba/exsu2', 'server_name':'TangoVimba/exsu2', 'host':'haspp04exp2' },
	'103_exsu1': {'server': 'tango://haspp04exp1:10000/p04/tangovimba/exsu1', 'server_name':'TangoVimba/exsu1', 'host':'haspp04exp1' },
	'104_exsu1_diff': {'server': 'tango://haspp04exp2:10000/p04/tangovimba/exsu1_diff', 'server_name':'TangoVimba/exsu1_diff', 'host':'haspp04exp2' },
	'204_cam11_aft_exsu2': {'server': 'tango://haspp04exp2:10000/p04/tangovimba/cam11', 'server_name':'TangoVimba/cam11', 'host':'haspp04exp2' },
	'102_cam16_aft_pgm1': {'server': 'tango://haspp04exp2:10000/p04/tangovimba/bm_aft_pgm1', 'server_name':'TangoVimba/bm_aft_pgm1', 'host':'haspp04exp2' },
	'105_cam17_aft_exsu1': {'server': 'tango://haspp04exp2:10000/p04/tangovimba/bm_aft_exsu1', 'server_name':'TangoVimba/bm_aft_exsu1', 'host':'haspp04exp2' },
	'FF_overview_cam': {'server': 'tango://haspp04ff:10000/p04/tangovimba/cam01', 'server_name':'TangoVimba/cam01', 'host':'haspp04ff' },
	'FF_measure_cam': {'server': 'tango://haspp04ff:10000/p04/tangovimba/cam02', 'server_name':'TangoVimba/cam02', 'host':'haspp04ff' },
		
}
	
	return c_m
	
def detector_map():	
	d_m = {\
	'B1_Keithley_1': {'address': 'tango://haspp04exp1:10000/p04/keithley6517a/exp1.01', 'current': 'current', 'current_range':'CurrRange', 'plc': 'CurrIntegrationPeriod', 'source': 'VSourceOffOn', 'current_auto_range':'CurrAutoRange'},
	'Keysight_1': {'address': 'tango://haspp04exp1:10000/p04/keysightb2980/exp1.01', 'current': 'current', 'current_range':'CurrRange','plc': 'ApertureTime', 'source': 'VSourceOffOn', 'current_auto_range':'CurrentAutoRange'},
	'Keysight_2': {'address': 'tango://haspp04exp1:10000/p04/keysightb2980/keys02', 'current': 'current',
			'current_range': 'CurrRange', 'plc': 'ApertureTime', 'source': 'VSourceOffOn',
			'current_auto_range': 'CurrentAutoRange'},
	'Keysight_3': {'address': 'tango://haspp04exp1:10000/p04/keysightb2980/keys03', 'current': 'current',
			'current_range': 'CurrRange', 'plc': 'ApertureTime', 'source': 'VSourceOffOn',
			'current_auto_range': 'CurrentAutoRange'},
	'B2_Keithley_1': {'address': 'tango://haspp04exp2:10000/p04/keithley6517a/exp2.01', 'current': 'current', 'current_range':'CurrRange','plc': 'CurrIntegrationPeriod', 'source': 'VSourceOffOn', 'current_auto_range':'CurrAutoRange'},
	'B2_Keithley_2': {'address': 'tango://haspp04exp2:10000/p04/keithley6517a/keithley2_b2', 'current': 'current', 'current_range':'CurrRange','plc': 'CurrIntegrationPeriod', 'source': 'VSourceOffOn', 'current_auto_range':'CurrAutoRange'},
	'Pipe_Keithley': {'address': 'tango://haspp04exp2:10000/p04/pipekeithley/exp2.01', 'current': 'PhotoDiodeCurrent', 'current_range':'', 'plc': '', 'source': '', 'current_auto_range': ''},

}
	
	return d_m
