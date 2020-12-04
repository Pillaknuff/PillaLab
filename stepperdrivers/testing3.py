#import testingconfig

# def printsomething(testingconfig):
#     print(testingconfig.a)

import tkinter

root = tkinter.Tk()
myvar = tkinter.StringVar()
myvar.set('')
myvar2 = tkinter.StringVar()
myvar2.set('')
mywidget = tkinter.Entry(root,textvariable=myvar,width=10)
mywidget.pack()
mywidget2 = tkinter.Entry(root,textvariable=myvar2,width=10)
mywidget2.pack()

def oddblue(a,b,c):
    widlist = [mywidget,mywidget2]
    for wid in widlist:
        if len(myvar.get())%2 == 0:
            wid.config(bg='red')
            wid.delete(0,tkinter.END)
            wid.insert(0,"red")
        else:
            wid.config(bg='blue')
            wid.delete(0,tkinter.END)
            wid.insert(0,"blue")
        wid.update_idletasks()


myvar.trace('w',oddblue)
myvar2.trace('w',oddblue)

root.mainloop()