# # # from tkinter import *

# # # def click():
# # #     MainTextBox.delete(0, END)  
# # #     OutputBox.delete('1.0', END) 

# # # GUI = Tk()
# # # MainTextBox = Entry(GUI, width = 20, bg = "white")
# # # MainTextBox.grid(row = 0, column = 0, sticky = W)
# # # Button(GUI, text = "SUBMIT", width = 6, command = click).grid(row = 1, column = 0, sticky = W)
# # # OutputBox = Text(GUI, width = 100, height = 10, wrap = WORD, background = "orange")
# # # OutputBox.grid(row = 4, column = 0, sticky = W)
# # # OutputBox.insert(END, "Example text")

# # # GUI.mainloop()


# # # from tkinter import *

# # # def onclick():
# # #    pass

# # # root = Tk()
# # # text = Text(root)
# # # text.insert(INSERT, "Hello.....")
# # # text.insert(END, "Bye Bye.....")
# # # text.pack()

# # # text.tag_add("here", "1.0", "1.4")
# # # text.tag_add("start", "1.8", "1.13")
# # # text.tag_config("here", background="yellow", foreground="blue")
# # # text.tag_config("start", background="black", foreground="green")
# # # root.mainloop()


# # # def definename():
# # #     global a
# # #     a = 1

# # # definename()
# # # print(a)
# # # import testing2
# # # testing2.printa()

# # # import importlib.util
# # # spec = importlib.util.spec_from_file_location("randomprogramm",'C:\\Users\\Philipp\\Documents\\01_PhD_Unterlagen\\05_ProgrammingStuff\\04_page\\Versuche\\ExampleProgramm.py')
# # # mod = importlib.util.module_from_spec(spec)
# # # spec.loader.exec_module(mod)

# # # class eeeehm:
# # #     def __init__(self):
# # #         self.bla  = "bla"

# # # aneehm = eeeehm()
# # # theobj = mod.Programm(aneehm)
# # # theobj.printit()

# # # pr = {}
# # # pr["affe"]  = 1

# # # if "aff" in pr:
# # #     print("hey")

# # # a = "affe"
# # # if not a == [0,0]:
# # #     print(a)

# # import tkinter

# # from matplotlib.backends.backend_tkagg import (
# #     FigureCanvasTkAgg, NavigationToolbar2Tk)
# # # Implement the default Matplotlib key bindings.
# # from matplotlib.backend_bases import key_press_handler
# # from matplotlib.figure import Figure

# # import numpy as np


# # root = tkinter.Tk()
# # root.wm_title("Embedding in Tk")

# # fig = Figure(figsize=(5, 4), dpi=100)
# # t = np.arange(0, 3, .01)
# # fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

# # canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
# # canvas.draw()
# # canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# # toolbar = NavigationToolbar2Tk(canvas, root)
# # toolbar.update()
# # canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


# # def on_key_press(event):
# #     print("you pressed {}".format(event.key))
# #     key_press_handler(event, canvas, toolbar)


# # canvas.mpl_connect("key_press_event", on_key_press)


# # def _quit():
# #     root.quit()     # stops mainloop
# #     root.destroy()  # this is necessary on Windows to prevent
# #                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate


# # button = tkinter.Button(master=root, text="Quit", command=_quit)
# # button.pack(side=tkinter.BOTTOM)

# # tkinter.mainloop()
# # # If you put root.destroy() here, it will cause an error if the window is
# # # closed with the window manager.

# import random
# import sys

# import matplotlib

# matplotlib.use('Qt5Agg')
# from PyQt5 import QtCore, QtWidgets
# from PyQt5.QtWidgets import QGridLayout

# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# from matplotlib.figure import Figure


# class MyMplCanvas(FigureCanvas):

#     def __init__(self, parent=None, width=5, height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.fig = fig  ###
#         self.axes = fig.add_subplot(111)

#         #self.axes.hold(False)

#         self.compute_initial_figure()

#         FigureCanvas.__init__(self, fig)
#         self.setParent(parent)

#         FigureCanvas.setSizePolicy(self,
#                                    QtWidgets.QSizePolicy.Expanding,
#                                    QtWidgets.QSizePolicy.Expanding)
#         FigureCanvas.updateGeometry(self)
#         self.xlim = self.axes.get_xlim()
#         self.ylim = self.axes.get_ylim()
#         self.mpl_connect('draw_event', self.on_draw)

#     def on_draw(self, event):
#         self.xlim = self.axes.get_xlim()
#         self.ylim = self.axes.get_ylim()

#     def compute_initial_figure(self):
#         pass


# class MyDynamicMplCanvas(MyMplCanvas):
#     def __init__(self, *args, **kwargs):
#         MyMplCanvas.__init__(self, *args, **kwargs)
#         timer = QtCore.QTimer(self)
#         timer.timeout.connect(self.update_figure)
#         timer.start(1000)

#     def compute_initial_figure(self):
#         self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'b')

#     def update_figure(self):
#         l = [random.randint(0, 10) for i in range(4)]
#         self.axes.cla()
#         self.axes.plot([0, 1, 2, 3], l, 'b')
#         self.axes.set_xlim(self.xlim)
#         self.axes.set_ylim(self.ylim)
#         self.draw()


# class P1(QtWidgets.QWidget):

#     def __init__(self, parent=None):
#         super(P1, self).__init__(parent)
#         layout = QGridLayout(self)

#         self.plot_canvas = MyDynamicMplCanvas(self, width=5, height=4, dpi=100)
#         self.navi_toolbar = NavigationToolbar(self.plot_canvas, self)

#         layout.addWidget(self.plot_canvas, 1, 1, 1, 1)
#         layout.addWidget(self.navi_toolbar, 2, 1, 1, 1)


# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent)
#         self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

# # #         self.stack = QtWidgets.QStackedWidget(self)
# # #         P1f = P1(self)
# # #         self.stack.addWidget(P1f)
# # #         self.setCentralWidget(self.stack)


# # # if __name__ == '__main__':
# # #     qApp = QtWidgets.QApplication(sys.argv)
# # #     aw = MainWindow()
# # #     aw.show()
# # #     sys.exit(qApp.exec_())

# # # import testingconfig

# # # import testing2

# # # import testing3


# # # #testing2.definesomething()
# # # testing2.definesomething(testingconfig)
# # # testing3.printsomething(testingconfig)

# # # inputpanel.py derived and improved from my Coolprop GUI on github
# # #
# # from tkinter import *
# # import tkinter.ttk as ttk

# # class InputFrame(LabelFrame):
# #     #
# #     # This input frame creates Entries and selects for Variables
# #     # contained in a Dictionary structure. It traces the inputs 
# #     # and keeps the values updated according to the type of the value.
# #     # 
# #     # datadict needs at least the three dicts and the list below
# #     # for one key must be an entry in every dict
# #     # the list order is used for processing
# #     # You can pass a list order with only one field e.g. to init
# #     # and only this field will be processed
# #     #  
# #     # datadict={
# #     #             'verbose_names':{},
# #     #             'values':{},
# #     #             'callback_vars':{},
# #     #             'order':[],
# #     #             }
# #     # 
# #     # if a dict units is added to the datadict, the units will be displayed behind the entry widgets
# #     #

# #     def __init__(self, parent,cnf={}, title=None,datadict=None,order=None,frameborder=5, InputWidth=60,**kwargs):
# #         #
# #         LabelFrame.__init__(self, parent)
# #         #
# #         self.InputWidth=InputWidth
# #         if datadict :
# #             self.datadict=datadict
# #         else:
# #             self.datadict={
# #                 'verbose_names':{},
# #                 'values':{},
# #                 'callback_vars':{},
# #                 'order':[],
# #                 }
# #         #
# #         if order :
# #             self.order=order
# #         else:
# #             self.order=self.datadict['order']
# #         #
# #         if title :
# #             self.IFrame = LabelFrame(parent, relief=GROOVE, text=title,bd=frameborder,font=("Arial", 10, "bold"))
# #         else:
# #             self.IFrame = LabelFrame(parent, relief=GROOVE,bd=frameborder,font=("Arial", 10, "bold"))
# #         #
# #         self.IFrame.grid(row=1,column=1,padx=8,pady=5,sticky=W)
# #         #
# #         self.InputPanel(self.IFrame)

# #     def InputPanel(self, PanelFrame, font=("Arial", 10, "bold")):
# #         '''
# #         '''
# #         #
# #         order_number=1
# #         for Dkey in self.order :
# #             if self.datadict['verbose_names'][Dkey] :
# #                 #
# #                 self.datadict['callback_vars'][Dkey].trace("w", lambda name, index, mode,
# #                                                          var=self.datadict['callback_vars'][Dkey],
# #                                                          value=self.datadict['values'][Dkey],
# #                                                          key=Dkey: self.InputPanelUpdate(var, key, value)
# #                                                          )
# #                 Label(PanelFrame, text=self.datadict['verbose_names'][Dkey], font=font).grid(column=1, row=order_number, padx=8, pady=5, sticky=W)
# #                 if type(self.datadict['values'][Dkey])==type(True):
# #                     Checkbutton(PanelFrame, width=self.InputWidth, variable=self.datadict['callback_vars'][Dkey], font=font).grid(column=2, row=order_number, padx=8, pady=5, sticky=W)
# #                 else:
# #                     Entry(PanelFrame, width=self.InputWidth, textvariable=self.datadict['callback_vars'][Dkey], font=font).grid(column=2, row=order_number, padx=8, pady=5, sticky=W)
# #                 try:
# #                     Label(PanelFrame, text=self.datadict['units'][Dkey],font=font).grid(column=3, row=order_number,padx=8,pady=5,sticky=W)
# #                 except KeyError :
# #                     Label(PanelFrame, text='       ',font=font).grid(column=3, row=order_number,padx=8,pady=5,sticky=W)
# #             else :
# #                 Label(PanelFrame, text=' ', font=font).grid(column=1, row=order_number, padx=8, pady=5, sticky=W)
# #             #
# #             order_number+=1

# #     def InputPanelUpdate(self, tkVar, key, value):
# #         #
# #         # Called on ever button press in an entry or click in a Checkbutton
# #         #
# #         if type(self.datadict['values'][key])==type(True):
# #             # For booleans we misuse a string because it is so easy
# #             self.datadict['values'][key] = True if tkVar.get()=='1' else False
# #         elif type(self.datadict['values'][key])==type(1): 
# #             # int
# #             self.datadict['values'][key] = int(tkVar.getint())
# #         elif type(self.datadict['values'][key])==type(1.1):
# #             # float
# #             self.datadict['values'][key] = float(tkVar.getdouble())
# #         else:
# #             # all the rest
# #             self.datadict['values'][key] = tkVar.get()

# from tkinter import *

# root = Tk()
# sv = StringVar()

# def callback():
#     print(sv.get())
#     return True

# e = Entry(root, textvariable=sv, validate="focusout", validatecommand=callback)
# e.grid()
# e = Entry(root)
# e.grid()
# root.mainloop()

# import win32gui

# def windowEnumerationHandler(hwnd, top_windows):
#     top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

# if __name__ == "__main__":
#     results = []
#     top_windows = []
#     win32gui.EnumWindows(windowEnumerationHandler, top_windows)
#     for i in top_windows:
#         if i[1] == "SES":
#         #if "SES".lower() in i[1].lower():
#             print(i)
#             win32gui.ShowWindow(i[0],5)
#             win32gui.SetForegroundWindow(i[0])
#             break

# import threading
# import time
# import random

# class dummy:
#     def __init__(self):
#         self.num = 1
#         self.startsetnum()
#         self.read()
    
#     def startsetnum(self):
#         thr = threading.Thread(target=self.setnum)
#         thr.start()

#     def read(self):
#         while True:
#             print(self.num)
#             time.sleep(1)

#     def setnum(self):
#         self.num = random.random()
#         time.sleep(0.5)
#         self.setnum()

# a = dummy()

