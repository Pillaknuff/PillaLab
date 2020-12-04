

# def import_driver(apath):
#     apath = apath.rstrip()
    
#     import importlib.util
#     spec = importlib.util.spec_from_file_location("stepperdriver",apath)
#     automatizer = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(automatizer)

#     return automatizer

# paths = ["./testing/theimportthing.py","./testing/thesecondimportthing.py"]
# objectlist = []
# for path in paths:
#     mymodule = import_moduleAndText(path)
#     myobject = mymodule.mytext()
#     objectlist.append(myobject)

# for obj in objectlist:
#     obj.printdatthing()

try:
    import drivers.PyTangoReader as TangoRead
except:
    from drivers import PyTangoReader as TangoRead

settings = {}

settings["PyTango.deviceadresses"] = 'hassppa3control:1000/asphere/test/keithley6517a'
settings["PyTango.devicetypes"]  = 'Keithley_standard'
settings["PyTango.devicename"] = 'Keithley1'

myDriver = TangoRead.PyTangoWrapper(settings)
err,val = myDriver.ReadDeviceByName('Keithley1')
print(val)