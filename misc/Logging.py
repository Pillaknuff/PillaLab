import h5py
import time
import sys
import numpy as np
from datetime import datetime

class Loggingmachine:
    def __init__(self,settings):
        self.settings = settings
        self.filename = self.settings["logging.filename"]
        self.path = self.settings["logging.folder"]
        self.groupnamemask = self.settings["logging.groupname"]
        self.hf = h5py.File(self.path+self.filename, 'a')

        i=0
        while True: # create group in loop
            groupname = self.groupnamemask + str(i) 
            try:
                self.g1 = self.hf.create_group(groupname)
                break
            except:
                i+=1
        
        self.timestamp = self.g1.create_dataset("time", (0,), maxshape=(None,))
        lenpressures = len(self.settings["pressures.names"])
        self.pressures = self.g1.create_dataset("pressures", (0,lenpressures), maxshape=(None,6))
    
    def logpressures(self,pressures):
        shape = self.timestamp.shape
        shape = (shape[0] + 1 ,)
        self.timestamp.resize(shape)
        self.timestamp[shape[0]-1] = time.time()

        shape = self.pressures.shape
        shape = (shape[0] + 1 ,shape[1])
        self.pressures.resize(shape)
        self.pressures[shape[0]-1] = pressures

import os.path
from os import path
class UniversalLoggingTool:
        def __init__(self,settings,filename,user="",groupmask="dataset"):
            self.settings = settings
            self.path = self.settings["logging.folder"]
            
            if not user == "":                                      # user specific directories
                user = user.strip()
                self.path=self.path + user + "/"
            
            if not path.exists(self.path):
                os.mkdir(self.path)
            self.path = self.path + filename + ".h5"                # full file path

            self.groupnamemask = groupmask
            self.hf = h5py.File(self.path, 'a')                     # create or open file

            i=0
            while True: # create group in loop                      # always log into unique group
                groupname = self.groupnamemask + str(i) 
                try:
                    self.g1 = self.hf.create_group(groupname)
                    break
                except:
                    i+=1
            
            # self.timestamp = self.g1.create_dataset("time", (0,), maxshape=(None,))
            # lenpressures = len(self.settings["pressures.names"])
            # self.pressures = self.g1.create_dataset("pressures", (0,lenpressures), maxshape=(None,6))

            self.datasetdict = {}
        
        def logEntry(self,what,data):

            if what in self.datasetdict.keys():
                dataset = self.datasetdict[what]
                timestamp = self.datasetdict[what+"_timestamp"]
            else:                                               # if entry not existing yet, create new dataset
                if type(data) == type("abd"):
                    datatype = 'string'
                else:
                    try:                                            # datatype detection, defenitely to be improved!
                        datasetsize = len(data)
                        datatype = 'array'
                    except:
                        datatype = 'single'
                
                if datatype == 'single':                        # create dataset by datatype
                    dataset = self.g1.create_dataset(what, (0,), maxshape=(None,))
                elif datatype == 'array':
                    dataset = self.g1.create_dataset(what, (0,datasetsize), maxshape=(None,datasetsize))
                elif datatype == "string":
                    dt = h5py.special_dtype(vlen=str)
                    dataset = self.g1.create_dataset(what, (0,), maxshape=(None,),dtype=dt)
                timestamp = self.g1.create_dataset(what+"_timestamp", (0,), maxshape=(None,))

                self.datasetdict[what] = dataset
                self.datasetdict[what+"_timestamp"] = timestamp
            

            shape = timestamp.shape                        # the actual logging part
            shape = (shape[0] + 1 ,)
            timestamp.resize(shape)
            timestamp[shape[0]-1] = time.time()

            shape = dataset.shape
            shape = list(shape) #(shape[0] + 1 ,shape[1])
            shape[0] +=1
            shape = tuple(shape)
            dataset.resize(shape)
            dataset[shape[0]-1] = data
        
        def stoplog(self):
            self.hf.close()
            self.datasetdict = {}
