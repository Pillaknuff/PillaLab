import os
from datetime import datetime
 


class txtLinelogger:
    def __init__(self,name,columns,folder,firstcolumn = 'filename'): # first column only used for nomenclature, filename is historic because of mapping
        self.name = (name.replace(".txt",""))
        self.columns = columns
        self.folder = folder

        self.createUnique()
        header = ""
        for entry in columns:
            try:
                header += str(entry) + '\t'
            except:
                header += "whatever? \t"
        self.writeLine(["starting at ",str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))])
        self.writeLine([firstcolumn,columns])

    def createUnique(self):
        self.name = self.getuniquename(self.name)
        self.file = open((self.folder+'/'+self.name),'w')
        print("mapping file created: " + (self.folder+'/'+self.name))

    
    def getuniquename(self,name,i=0):
        files = dict ([(f, None) for f in os.listdir (self.folder)])
        try:
            a = files[name+'.txt']
            try:             
                a = files[name + str(i) +'.txt']
                i += 1
                name = self.getuniquename(name,i)
                return name
            except: 
                return name + str(i) +'.txt'
        except:
            return name+'.txt'



    
    def writeLine(self,entries): #takes an array of strings...please do not pass a string, this would do weird stuff
        text = ''
        for entry in entries:
            try:
                text += str(entry) + "\t"
            except:
                text += "xxx \t"
        text += '\n'
        self.file.write(text)

    def closeFile(self):
        self.file.close()
