"""

Implements a class to read a set of Tango variables via server-side polling. values read are buffered internally. 
statistics (no. of points, min,mean,max,std, trend) are returned to stdout triggered by stdin (pipe or keyboard). 
When the name of an existing file is entered, the output will be appended to the file. Otherwise, it will be dumped to stdout
This can nicely be triggered by inotifywait when configured to output just the name of a file that triggered an event. 
In this way, the tool is used to amend elecion's .info files with up-to-date beamline status from Tango variables 
specified as command line arguments. Instead of passing the full Tango path and attribute names, the shortcut as defined in 
P04variables must be specified for each observable.

features:
 - after no new data was received for some period defined by the timeout property, the connection will be closed an reopened. 
   This should allow to recover after a Tango server was restarted
 - basic time unit used for polling is ms, timestamps are converted to seconds (float)
 - the internal buffer has a fixed size. once it is full, the oldest data points will be overwritten
  - the output style can be 
      'python' (native i.e. like a dict is displayed), 
      'elecion' (to append to .info files), 
      'lablog' (formatted as table for lab log),
      'tabdelim' ( create tab-delimited ASCII) 
 
usage:
1. create TangoMonitor object with tango dev name and attribute to be observed -> polling is immediately activated and runs in the background
2. read statistics of buffered data and flush the buffer at once using the FetchData()
   alternatively, a string representation implicitly uses FetchData() and converts the data into some string representation,
   depending on the 'style' setting 

 - to read the evaluated buffer contents without erasing it, use EvalCurrent(), which will return a dictionary holding the results
 - to empty the buffer without reading, call ResetBuffer()
 - ShutdownInterface/StartInterface can be used manually to control the polling
 - OutputHeader creates a headerline for the current output style if applicable
 
  - requires numpy>=1.16 !
 
 
  (... old log from TangoMonitor skipped here ...)
  
Apr 7, 2020
  - started Tangomonitor2 as a reworked version to make use of Tango's server-side buffering
  - deleted some obsolete code (commented out before)
  - removed event-based readout functionality
  - removed event callback 
   - introduced new class implementing an upgraded AttributeProxy. Some methods are added to give more convenient access to the poll ring buffer
   - Tangomonitor is now using this class 
   - TangoMonitor now reads data via the poll ring buffer. When moving large chunks of data, transfer time < 1ms per point can be achieved even from the VPN!!!
   - modified FetchData to work with new data source
   - Added a number of filter options to FetchData
   - completely replaced Shutdowninterface: is now quite trivial
   - made first attempts to run this: no deep testing yet, but initial operation succeeded
   - cleanup code: remove commented stuff
  
Apr 8, 2020
 - removed bug that triggered restart of device on every Resize (even when buffer size didnt change)
 - added some debugging printout to PolLRingBufferClient.RestartDevice()
 - Tangomonitor.__str__() is not calling fetchData any longer and instead accesses the stored last read
 - introduced some new fields in Tangomonitor to store results and raw data from the last call of FetchData()
  - updated main() to work with the slightly new conventions
  
to do:
 - manage privacy of some variables
 - review status as class or instance variables of some members
 
 currently open (old items, need to review if still applicable):
  - hardcoded polling time, output detail and output style
  - need more flexibility to operate this via pipe and via user input
  - cannot nicely make use of automatic output header generation
  - timeout/reconnection is not tested
  - floating time format: following which standard?
  - configure poll time and output detail in P04Variables?
  - indivudal datapoints are buffered, but cannot be accessed other than by the property of the class directly-> need interface
  
 
readout strategies:
 - use FetchData only, add by some more parameters:
     - unique points (for statistics)
     - equidistant samples (for analysis in tome domain)
     - all data (including overlapped for performance, debugging)
     - either specify no of points to retrieve or time interval
 - Retardomat must use a local timer for the readout, no hookup to event loop any more, because no event loop
"""

from PyTango import DeviceProxy, AttributeProxy, EventType, DevError, TimeVal
import tango, PyTango

import numpy as np
import sys, os, traceback, time

from P04variables import GetP04Var 

# class holds some handy tools to work with the poll ring buffer
# even though poll ring depth is a device-wide setting, we derive this class from AttributeProxy as there is some attribute-specific stuff in it
class PollRingBufferClient( AttributeProxy ):
    
    def __init__(self, *args ):
        super(PollRingBufferClient, self).__init__(*args)
        
        self.__old_status = self.GetBufferConfig()
        self.__buff_param = self.__old_status
        
    def __del__(self):
        # restore old buffer settings
        self.ResizeBuffer(N_buffer = self.__old_status['N_buffer'], 
                          sample_period  = self.__old_status['sample_period'])
        if not self.__old_status['poll_active']: self.stop_poll()
        
        super(PollRingBufferClient, self).__del__()
        
    # crate full tango name of the device hosting this attribute
    # didnt care to look this up somewhere in the Tango API (certainly exists)
    def FullDevicePath(self):
        dp  = self.get_device_proxy()
        return 'tango://{:s}:{:s}/{:s}'.format(dp.get_db_host(), 
                                               dp.get_db_port(), 
                                               dp.dev_name())       
    def FullAttributePath(self):
        return self.FullDevicePath() + '/' + self.name()
        
    #restart tangoDevice server. 
    #becomes necessary when changes to the poll ring buffer are applied    
    def RestartDevice(self):
        #get proxy of administering device and trigger restart
        t0 = time.time()
        print('restarting device ' + self.FullDevicePath())
        self_adm = DeviceProxy( self.get_device_proxy().adm_name() )
        self_adm.DevRestart( self.FullDevicePath() )
        print('\t\t...took {} ms.'.format((time.time()-t0)*1.e3))
        
    # sets poll rate and buffer size given two out of the three keyword arguments
    # returns buffer size, sample rate and total time interval covered by the buffer
    # use sample period in s (unlike Tango style)
    # use total time in s     
    def ResizeBuffer(self, N_buffer = None, sample_period = None, total_time = None):
        
        assert np.sum( np.array((N_buffer == None, 
                                 sample_period==None, 
                                 total_time == None)
                                 )) == 1, 'need exactly two defined parameters' 
        assert N_buffer == None or type(N_buffer) == int or N_buffer.is_integer(), 'N_buffer must be integer'
        
        if N_buffer == None:    N_buffer = np.ceil(  total_time / sample_period )
        if sample_period == None: sample_period = total_time / N_buffer
        if total_time == None: total_time = sample_period*N_buffer  

        assert N_buffer>=10 and N_buffer<=1e6, 'invalid buffer size'
        assert sample_period >= 5e-3, 'sample period too small for Tango'
        assert total_time >=0, 'invalid total time'
        
        dp = self.get_device_proxy()
        
        # set buffer size,
        # restart if size has changed
        
        #N_buffer_curr =  dp.get_property('poll_ring_depth' )['poll_ring_depth']        
        #an empty list is returned in case the device is still working on default size (==10)
        #N_buffer_curr = N_buffer_curr[0] if len(N_buffer_curr) ==1 else 10         
        N_buffer_curr = self.GetBufferConfig()['N_buffer']            
        N_buffer_new = str(int( N_buffer ))
        if float(N_buffer_new) != float(N_buffer_curr): 
            self.get_device_proxy().put_property({'poll_ring_depth':[N_buffer_new]})
            self.RestartDevice()  
        
        # set poll rate, enable poll (given in seconds, needs ms!)
        self.poll( int( sample_period*1e3) )
                
        #remember settings in case it needs to be restored later 
        self.__buff_param = self.GetBufferConfig()
        return self.__buff_param
            
    # get current buffer-relevant settings from tango classes
    def GetBufferConfig(self):
        prop = self.get_device_proxy().get_property('poll_ring_depth' )['poll_ring_depth']       
        N_buf = int( prop[0]) if len(prop)==1 else 10   #10 is the currently known default value, if set to default, it cannot be inquired here
        poll_period = self.get_poll_period()*1.e-3        #get in ms, save time in s
        poll_active = self.is_polled()
        return {'N_buffer':N_buf,
                'sample_period':poll_period,
                'poll_active':poll_active,
                'total_time': (N_buf*poll_period)
                }
            
    # clear buffer, prepare for new accumulation
    # tbd: check if there is a less invasive way
    def ResetBuffer(self):
        self.RestartDevice()

    # get contents of poll buffer and filter everything but value and timestamp
    # return numpy array of values (N x 2) and field names
    def ReadBuffer(self, N_points_max = None):
        if N_points_max == None: N_points_max = self.GetBufferConfig()['N_buffer']
        try:
            d = self.get_device_proxy().attribute_history(self.name(), int( N_points_max) )            
            return np.array( [(j.value, j.time.totime())  for j in  d], dtype = np.double), (self.name()[-7:], 'time_' + self.name()[-7:])
        except PyTango.DevFailed:   #raised when no data available
            return np.ndarray((0,2), dtype = np.double), (self.name()[-7:], 'time_' + self.name()[-7:])

class TangoMonitor(object):
    
    buf_max = 1024;   #default maximum size of ring buffer used (can be overridden in constructor)
 
    # tango device and tangoattribute can be specified either as existing objects or by its string names  
    def __init__(self, 
                 TangoDevice,
                 TangoAttribute,
                 PollingPeriod = 200,
                 style = 'elecion',
                 channel_tag = '',
                 detail = 'full',
                 buf_max = buf_max):
    
        self.style = style
        self.detail = detail
        if channel_tag == '':
            # no channel given: create a random sequence of characters as tag
            r = np.random.randint(65,91,(5,))
            s = '';
            for j in r:
                s += chr(j)
            self.channel_tag = s
        else:
            self.channel_tag = channel_tag  
        
        self.buffer = np.ndarray((),dtype = np.double)
        self.buf_max = buf_max
        self.buf_count = 0
        self.interface_active = False
        
        #fields to accept all results and intermediates form the last call to FetchData() 
        self.last_read = time.time()   # needed for 'onlynew' filter in FetchData        
        self.last_results = {}
        self.last_raw_data =np.ndarray((),dtype = np.double) 
        self.last_filter_data = {}
                
        #self.ResetBuffer()
        self.last_result = {}
        
        self.PollingPeriod = PollingPeriod
        self.StartInterface(TangoDevice = TangoDevice, TangoAttribute = TangoAttribute)            
       
    def __del__(self):
        # stop polling, unregister callback
        print "shut down " + self.channel_tag
        self.ShutdownInterface()
 
    def ShutdownInterface(self):
        if not self.interface_active:
            return
                
        #tbd : what needs to ge hoere actually?
        # reset buffer size to initial one
        #reset polling state        
        # ...
        
        #destroy attribute proxy -> reset polling and buffer status
        if self.TangoDevAttr != None:
            self.TangoDevAttr = None
        
        self.interface_active = False
        return self.interface_active
            
        
    # setup the Tango part, start polling
    # this can use either prefabricated proxies of the device and attribute
    # or create its own objects from their string specifications
    # works indendently for deviceproxy and attributeproxy 
    def StartInterface(self, TangoDevice = None, TangoAttribute = None):
        
        if self.interface_active:
            return True
        
        # try to recover from stored string if none specified        
        if TangoDevice == None:            
            TangoDevice = self.TangoDev
            #assert(type(TangoDevice) == DeviceProxy)
            assert(issubclass( type(TangoDevice), DeviceProxy))
        
        # set up device proxy, enable polling, register callback, start buffering    
        if type(TangoDevice) == str:        # device proxy to be created
            self.TangoDev  = DeviceProxy(TangoDevice)
            self.TangoDev_str =  TangoDevice        
        elif issubclass(type(TangoDevice), DeviceProxy):
            self.TangoDev = TangoDevice
            self.TangoDev_str = self.TangoDev.get_db_host() + ':' + str(self.TangoDev.get_db_port()) + '/' + self.TangoDev.dev_name() 
        else:            
            raise Exception('unknown tango device specification') 
        
        #try to recover from stored string if none specified        
        if TangoAttribute == None:            
            TangoAttribute = self.TangoDevAttr
            #assert(type(TangoAttribute) == AttributeProxy)
            assert(issubclass(type(TangoAttribute), PollRingBufferClient ))
        
        #set up related attribute in the same manner
        if type(TangoAttribute) == str:     # attribute proxy to be created
            if TangoAttribute in self.TangoDev.get_attribute_list():
                # only attribute name provided -> make full name
                TangoAttribute = self.TangoDev_str + '/'  + TangoAttribute            
            #assume that full name is provided
            self.TangoDevAttr  = PollRingBufferClient( TangoAttribute )
            self.TangoAttr_str =  TangoAttribute                        
        elif issubclass(TangoAttribute, PollRingBufferClient):
            self.TangoDevAttr = TangoAttribute
            self.TangoDevAttr_str = self.TangoDevAttr.name() 
        else:            
            raise Exception('unknown tango attribute specification')
        
        # set buffer size
        # this implicitly clears the buffer if really resized
        # and also starts polling
        self.TangoDevAttr.ResizeBuffer(N_buffer = self.buf_max, 
                                       sample_period = self.PollingPeriod*1.e-3  )      
        return True
    
    # stop polling, close deviceproxy
    def ResetInterface(self):
        self.ShutdownInterface()
        self.StartInterface()      
    
    def EvalCurrent(self):
        #return a dict with stats on current data
        # SLP it the 'slope', i.e. the linear trend in the data  
        if self.buf_count == 0:
            #no new points gathered-> use last known result            
            # update other values as well?
            if self.last_result.has_key('NPT'):
                self.last_result['NPT'] = 1            
            return self.last_result        
        else:            
            d = self.buffer
            ts = self.buf_timestamp        
                      
        # filter out bad data points
        k = np.isfinite(ts) & np.isfinite(d)
        if any(k == False):
            print >>sys.stderr, 'warning: bad data in ring buffer (TangoMonitor)'
        n_valid = np.sum(k)
        d = d[k]
        ts = ts[k]

	if n_valid == 0:
            d = np.array(np.nan)
            ts = np.array(np.nan)
                         
        if self.detail in ('medium', 'full') and n_valid > 2:
            slp = np.polyfit(ts, d, 1)[0]
        else:
            slp = np.nan
        
        if self.detail == 'min':
            self.last_result = {'AVG':np.nanmean(d)}
        elif self.detail == 'less':
            self.last_result = {'MIN':np.nanmin(d),
                                'MAX':np.nanmax(d),
                                'AVG':np.nanmedian(d)}
        elif self.detail == 'medium':
            self.last_result = {'MIN':np.nanmin(d),
                                'MAX':np.nanmax(d),
                                'AVG':np.nanmedian(d),
                                #'STD':np.nanstd(d, ddof = 1) if n_valid>1 else np.nan,
                                'STD': 0.5*np.diff( np.nanpercentile(d,(15.87, 84.13))  )[0],
                                'SLP':slp}
        elif self.detail == 'full':
            self.last_result = {'MIN':np.nanmin(d),
                                'MAX':np.nanmax(d),
                                'AVG':np.nanmedian(d),
                                #'STD':np.nanstd(d, ddof = 1) if n_valid>1 else np.nan,
                                'STD': 0.5*np.diff( np.nanpercentile(d,(15.87, 84.13))  )[0],
                                'NPT':n_valid,   
                                'SLP':slp,   
                                'T__':np.nanmedian(ts),
                                'DT_':np.nanmax(ts) - np.nanmin(ts)}

        return self.last_result
    
    # read analysed data, then clear buffer
    # clear_buffer allows to specify if the buffer is emptied after evaluation and a new acquisition is started
    # to do: set style of returned information (dict, formatted string, etc.)
    #
    # filter options:
    # unique: filter out repeated, identical readings whcih are typical a result of the device 
    #        communicating slowly (opposite: return equidistant points with sample_period spcing)
    # oldest = POSIX timestamp specifying the oldest accepted data point
    # newest = POSIX timestamp specifying the newest accepted data point
    # latest = accept points from maximum the number of seconds specified ago
    # more tbd.   
    def FetchData(self, 
                  clear_buffer = False,
                  unique = False,
                  onlynew = False, 
                  oldest = None,
                  newest = None,
                  latest = None, 
                  maxN = None):
                
        # read from server,  
        # filter as requested,
        # write internal data so EvalCurrent can work 
        data, tag = self.TangoDevAttr.ReadBuffer(maxN)   
        
        self.buffer = data[:,0]
        self.buf_timestamp = data[:,1] 
        
        filter_idx = np.ndarray(self.buffer.shape, dtype = np.bool)
        filter_idx[:]=True
        if unique         : filter_idx &= np.diff(self.buffer, prepend = np.NaN) != 0
        if onlynew        : filter_idx &= self.buf_timestamp > self.last_read
        if latest  != None: filter_idx &= self.buf_timestamp-time.time() <= latest
        if oldest  != None: filter_idx &= self.buf_timestamp >= oldest
        if newest  != None: filter_idx &= self.buf_timestamp <= newest
         
        #(...)
        
        #remove all points that didnt pass the filter combo
        self.buffer = self.buffer[filter_idx]
        self.buf_timestamp = self.buf_timestamp[filter_idx]
        self.buf_count = self.buffer.shape[0]
        
        res = self.EvalCurrent()
        
        if clear_buffer:
            self.TangoDevAttr.ResetBuffer()
                      
        # store for delayed access
        self.last_read = time.time()        
        self.last_raw_data = data
        self.last_filter_data = self.buffer
        
        return res
    
    # string representation of analysis of last read data    
    def __str__(self):
        d = self.last_result        
      
        # format output data
        # to do: styles: elecion .info, lab log, tab-separated,...
        if self.style in ('python','raw'):
            return str( d )
        elif self.style == 'elecion':
            s = ''
            for k in d: s += self.channel_tag + "_" + k + '\t' + ("%0.6e" % d[k]) + '\n'            
        elif self.style == 'lablog':
            # human readable, formatted for copy/paste into lab logbook
            s = ' | ' + self.channel_tag
            for k in d: s += ' | ' + ("%10.3e" % d[k])             
        elif self.style == 'tabdelim':
            #tab delimited ASCII
            s = ''
            for k in d: s += ("%15.8e" % d[k]) + '\t'            
        else:
            return str( d )
        
        return s
    
    # for tabulated output, create a header line
    def OutputHeader(self):       
        r = self.EvalCurrent()
        
        if self.style == 'lablog':
            # human readable, formatted for copy/paste into lab logbook
            # first cell is empty to align with contents
            h = ' | '
            for k in r: h += ' | ' + ("%10s" % k)
            return h +'\n'         
        elif self.style == 'tabdelim':
            #tab delimited ASCII
            h = ''
            for k in r:  h += self.channel_tag + '_' + k + '\t'
            return h + '\n'
        else:
            return ''

"""
# debug only, delete later
if __name__ == '__main__':
    a = PollRingBufferClient('haspp04exp2:10000/p04/hviseg/exp2.01/MeasSenseVoltage')
    
    print a.FullDevicePath()
    print a.GetBufferConfig()
    a.ResizeBuffer(total_time = 3600, sample_period = 0.5)
    print a.GetBufferConfig()
    
    while True:
        time.sleep(10)    
        t0 = time.time()
        x,_ = a.ReadBuffer()
        print x.shape
        print time.time()-t0
"""


#when used as standalone: 
#set up set of vars, monitor, make output to stdout on trigger from stdin
if __name__=='__main__':
    
    # get Tango variables to observe from command line args
    # multiple attributes per Tango server are supported
    d = ();
    for a in sys.argv[1:]:
        try:
            v = GetP04Var(a)
            sys.stderr.write('creating {} = {}\n'.format(a, v['path']))
                        
            for id_ in v['valID']:
                sys.stderr.write('\t\t...' + id_ +'\n')
                d += (TangoMonitor(v['path'],
                                   id_, 
                                   style = 'elecion', 
                                   PollingPeriod = 1000, 
                                   channel_tag = a, 
                                   detail = 'full'), )
        except:        
            t = sys.exc_info()[2]                
            print traceback.format_exc(t)
    
    if len(d)==0:
        sys.stderr.write('no observables created. quitting.' + '\n')  
        exit()
        
    try:
        print d[0].OutputHeader()
        while True:
            try:              
                #wait for trigger via stdin
                input_ = sys.stdin.readline().rstrip()                
                
                #read all recent data and 
                #create output string (multi-line)
                output = ''
                for i in d:
                    i.FetchData( onlynew = True )
                    output += str(i) +'\n'
                                        
                if len(input_)==0 or not os.path.exists(input_):
                    #write to stdout unless the name of an existing file was specified
                    print output
                else:
                    # append to file with given name                    
                    f = open(input_, 'a')
                    f.write( output )
                    f.close()
                    
                    # ignore the next incoming event (was triggered from previous line)
                    # only makes sense when used with a pipe from inotifywait 
                    #(breaks the infinite loop triggered otherwise), is annoying when used interactively
                    input_ = sys.stdin.readline().rstrip()                
            except KeyboardInterrupt:
                break;
            except:        
                t = sys.exc_info()[2]                
                sys.stderr.write( traceback.format_exc(t) )
    finally:
        sys.stderr.write("stopping system\n")
        for j in d:
            j.ShutdownInterface();
