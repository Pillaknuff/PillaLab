'''
the motion module, module, that can import stepper drivers and use them
The methods work as following: positions are organized in groups
ports and other things are defined for each group

'''
import numpy as np

class MotionModule:
    def __init__(self,settings):
        self.settings = settings
        self.interfaces = {}
        self.controllers = np.zeros(max(self.settings["motion.controllers"])+1).tolist()

        #print("Initializing motion Module with settings: " + str(self.settings))

        for i in range(len(self.settings["motion.names"])):
            conum = settings["motion.controllers"][i]
            if self.controllers[conum] == 0: #then init, otherwise just enter
                settingsRs = self.translateSettings(conum)
                stepperdriverfile = self.import_driver(self.settings["motion.driverfiles"][conum])
                steppermodule = stepperdriverfile.Stepper(settingsRs)

                #convention: interface, channel, type
                self.interfaces[self.settings["motion.names"][i]] = [steppermodule,self.settings["motion.channels"][i]]
                self.controllers[conum] = steppermodule
            else:
                steppermodule = self.controllers[conum]
                self.interfaces[self.settings["motion.names"][i]] = [steppermodule,self.settings["motion.channels"][i]]

        
    def translateSettings(self,conum):
        settingsRs = {}
        transferlist = ["baud","com","bits","timeout","stopbits","parity","velocities"]
        for element in transferlist:
            try:
                settingsRs['steppers.'+element] = self.settings['motion.'+element][conum]
            except:
                print("key not found - " + element)
        namelist = []
        stepsperunitlist = []
        channellist = []
        for i in range(len(self.settings["motion.names"])):
            if self.settings["motion.controllers"][i] == conum:
                namelist.append(self.settings["motion.names"][i])
                stepsperunitlist.append(self.settings["motion.stepsperunit"][i])
                channellist.append(self.settings["motion.channels"][i])

        settingsRs["steppers.names"] = channellist
        settingsRs["steppers.stepsperunit"] = stepsperunitlist
        settingsRs["steppers.channels"] = channellist
        return settingsRs

    def import_driver(self,apath):
        apath = apath.rstrip()
        
        import importlib.util
        spec = importlib.util.spec_from_file_location("stepperdriver",apath)
        automatizer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(automatizer)

        return automatizer

    def go_abs(self,motname,pos):
        print("asked to move something")
        interface,channel = self.interfaces[motname]
        #print(interface)
        err = interface.go_abs(channel,pos)
        return err

    def go_rel(self,motname,pos):
        interface,channel = self.interfaces[motname]
        err = interface.go_rel(channel,pos)
        return err

    def go_abs_all(self,pos):
        error = False
        for motname in self.settings["motion.names"]:
            motindex = self.settings["motion.names"].index(motname)
            interface,channel = self.interfaces[motname]
            err = interface.go_abs(channel,pos[motindex])
            if err:
                error = True
        return error
    def go_rel_all(self,pos):
        error = False
        for motname in self.settings["motion.names"]:
            motindex = self.settings["motion.names"].index(motname)
            interface,channel = self.interfaces[motname]
            err = interface.go_rel(channel,pos[motindex])
            if err:
                error = True
        return error

    def set_pos(self,motname,newstate):
        interface,channel = self.interfaces[motname]
        try:
            interface.set_pos(channel,newstate)
        except Exception as e:
            print("probably set pos not implemented: " + str(e))

    def get_pos(self,motname):
        interface,channel = self.interfaces[motname]
        return interface.get_pos(channel)
        
    
    def get_pos_all(self):
        errlist = []
        poslist = []
        movlist = []
        for motname in self.settings["motion.names"]:
            err, pos, mov = self.get_pos(motname)
            errlist.append(err)
            poslist.append(pos)
            movlist.append(mov)
        return errlist, poslist, movlist
    
    def group_move_abs(self,group,pos):
        j = 0 #iterator for positions
        error = False
        for i in range(len(self.settings["motion.groups"])):
            if group == self.settings["motion.groups"]:
                motname = self.settings["motion.names"][i]
                whereto = pos[j]

                err = self.go_abs(motname,whereto)
                if err:
                    error = True
        return error

    def group_move_rel(self,group,pos):
        j = 0 #iterator for positions
        error = False
        for i in range(len(self.settings["motion.groups"])):
            if group == self.settings["motion.groups"]:
                motname = self.settings["motion.names"][i]
                whereto = pos[j]

                j += 1

                err = self.go_rel(motname,whereto)
                if err:
                    error = True
        return error
    
    def group_get_pos(self,group):
        error = False
        poslist = []
        movlist = []
        j = 0 #iterator for positions
        error = False
        posarray = []
        for i in range(len(self.settings["motion.groups"])):
            if group == self.settings["motion.groups"]:
                motname = self.settings["motion.names"][i]
                err, pos, mov = self.get_pos(motname)
                if err:
                    error = True
                poslist.append(pos)
                movlist.append(mov)
        return error, poslist, movlist



