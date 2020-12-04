#this is a python copy of the loop bult for communicaiton with the SES software over network
#we need \r\n as eol
settings = {
    "network.port" : 5020,
    "network.timeout" : 250, #ms
    "network.msglen" : 100, #bytes
}

import socket

class networkInterface:
    def __init__(self,settings):
        self.settings = settings
        self.socket = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
        self.socket.bind((socket.gethostbyname(socket.gethostname()),self.settings["network.port"]))
        
    def listen(self):
        #self.socket.connect() #server is listening not connecting!
        self.socket.listen()
        self.conn, self.addr = self.socket.accept()
        print("connected on " + str(self.addr))
        success = True
        return success
    
    def quickreceiveconn(self):
        try:
            data = self.conn.recv(2048)
            data = data.decode('UTF-8')
            if data == '':
                self.listen()
        except:
            data = 'disconnected'
            self.listen()
        return data
    
    def sendonconnection(self,datastring):
        datastring = datastring.encode('UTF-8')
        self.conn.sendall(datastring)
    
    def closeconnection(self):
        self.socket.close()

    # def myreceiveorig(self):
    #     MSGLEN = self.settings["network.msglen"]
    #     chunks = []
    #     bytes_recd = 0
    #     while bytes_recd < MSGLEN:
    #         chunk = self.socket.recv(min(MSGLEN - bytes_recd, 2048))
    #         if chunk == b'':
    #             raise RuntimeError("socket connection broken")
    #         chunks.append(chunk)
    #         bytes_recd = bytes_recd + len(chunk)
    #     return b''.join(chunks)

    # def myreceive(self):
    #     MSGLEN = self.settings["network.msglen"]
    #     chunks = []
    #     bytes_recd = 0
    #     while bytes_recd < MSGLEN:
    #         chunk = self.socket.recv(min(MSGLEN - bytes_recd, 2048))
    #         if chunk == b'':
    #             break
    #         chunks.append(chunk)
    #         bytes_recd = bytes_recd + len(chunk)
    #     return b''.join(chunks)
    
    # def recieveonconnection(self):
    #     MSGLEN = self.settings["network.msglen"]
    #     chunks = []
    #     bytes_recd = 0
    #     while bytes_recd < MSGLEN:
    #         chunk = self.conn.recv(min(MSGLEN - bytes_recd, 2048))
    #         if chunk == b'':
    #             break
    #         chunks.append(chunk)
    #         bytes_recd = bytes_recd + len(chunk)
    #     return b''.join(chunks)
    


import numpy as np
import time
import threading
from functools import partial
class dummycontroller:
    def __init__(self,settings):
        self.settings = settings
        self.states = np.zeros(6)
        self.stable = True
        self.speeds = np.ones(6)*0.1

        self.server = networkInterface(self.settings)

    def runlistener(self):
        success = self.server.listen()
        if success:
            while True:
                #dat = myServer.recieveonconnection()
                dat = self.server.quickreceiveconn()
                print("received: " + dat)
                self.commandin(dat)
        else:
            print("listening not successfull")

    def moveabs(self,vec):
        vec = np.array(vec,dtype='float')
        mvvec = vec - self.states
        waittime = np.divide(abs(mvvec),self.speeds).max()
        stepdiv = 100
        self.stable = False
        for i in range(stepdiv):
            self.states += mvvec/stepdiv
            time.sleep(waittime/100)
        self.states = vec
        self.stable = True
    
    def stop(self):
        self.stable = True
    
    def commandin(self,command):
        action = command[0:3]
        whichval = command[4:7]
        
        if action == 'set':
            if whichval == 'pos':
                values = command[7:]
                values = np.fromstring(values,dtype=float,sep=';')
                mythread = threading.Thread(target=partial(self.moveabs,values))
                mythread.start()
                self.answer('done')
            elif whichval == 'stp':
                self.stop()
                self.answer('done')
        elif action == 'get':
            if whichval == 'pos':
                stvec = self.states
                outstr = np.array2string(stvec,formatter={'float_kind':lambda x: "%.2f;" % x}).replace('[','').rstrip(';]') #format to desired listtype
                self.answer(outstr)
                
            elif whichval == 'sts':
                ret = str(int(not self.stable))
                self.answer(ret)

    def answer(self,answerstring):
        answerstring += '\r\n'
        self.server.sendonconnection(answerstring)





if __name__ == '__main__':
    mycontroller = dummycontroller(settings)
    mycontroller.runlistener()
