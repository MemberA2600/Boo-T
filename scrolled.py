from tkinter import *
import tkinter.scrolledtext as tkscrolled

from tkinter import *

def num(event):
   shit.config(font=(('Arial',int(event.keysym)*3)))


window = Tk()
window.geometry("%dx%d+%d+%d" % (500,400,550,300))
shit=tkscrolled.ScrolledText()
shit.pack()
shit.bind("<Key>", num)

window.mainloop()