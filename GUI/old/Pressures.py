#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.26
#  in conjunction with Tcl version 8.6
#    Feb 14, 2020 08:16:01 PM CET  platform: Windows NT

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import Pressures_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1 (root)
    Pressures_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    Pressures_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font13 = "-family {Comic Sans MS} -size 30 -weight normal "  \
            "-slant roman -underline 0 -overstrike 0"
        font9 = "-family {Segoe UI} -size 20 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"

        top.geometry("863x143+743+127")
        top.minsize(120, 1)
        top.maxsize(1924, 1061)
        top.resizable(1, 1)
        top.title("New Toplevel")
        top.configure(background="#d9d9d9")

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.0, rely=-0.07, height=61, width=144)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font9)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Pressures:''')

        self.Display = tk.Label(top)
        self.Display.place(relx=0.185, rely=0.21, height=61, width=664)
        self.Display.configure(background="#d9d9d9")
        self.Display.configure(disabledforeground="#a3a3a3")
        self.Display.configure(font=font13)
        self.Display.configure(foreground="#000000")
        self.Display.configure(text='''P1: 0,000 mBar    P2: 0,000 mBar''')

        self.Graph = tk.Button(top)
        self.Graph.place(relx=0.012, rely=0.49, height=54, width=57)
        self.Graph.configure(activebackground="#ececec")
        self.Graph.configure(activeforeground="#000000")
        self.Graph.configure(background="#5f5f5f")
        self.Graph.configure(command=Pressures_support.Graph)
        self.Graph.configure(disabledforeground="#a3a3a3")
        self.Graph.configure(foreground="#000000")
        self.Graph.configure(highlightbackground="#d9d9d9")
        self.Graph.configure(highlightcolor="black")
        self.Graph.configure(pady="0")
        self.Graph.configure(text='''Graph''')

        self.Settings = tk.Button(top)
        self.Settings.place(relx=0.093, rely=0.49, height=54, width=57)
        self.Settings.configure(activebackground="#ececec")
        self.Settings.configure(activeforeground="#000000")
        self.Settings.configure(background="#5f5f5f")
        self.Settings.configure(command=Pressures_support.Settings)
        self.Settings.configure(disabledforeground="#a3a3a3")
        self.Settings.configure(foreground="#000000")
        self.Settings.configure(highlightbackground="#d9d9d9")
        self.Settings.configure(highlightcolor="black")
        self.Settings.configure(pady="0")
        self.Settings.configure(text='''Settings''')

if __name__ == '__main__':
    vp_start_gui()





