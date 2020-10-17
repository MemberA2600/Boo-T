from tkinter import *
from abc import *
import os
import sys
import re
from tkinter.filedialog import *
from tkinter import messagebox
from tkinterhtml import HtmlFrame
import multiprocessing
import tkinter.scrolledtext as tkscrolled

sys.path.insert(1, "scr/")
from Dictionaries import *
from Config import *
from Monitor import *
from DisplayLoading import *

class Create_MainWindow_Real(ABC):
    """Creating the Main Window, loads data for application."""
    def __init__(self, main):

        self.__main=main
        self.__main.geometry("%dx%d+%d+%d" % (1, 1, 1, 1))
        self.__main.overrideredirect(True)
        self.__main.resizable(False, False)

        import pyglet
        pyglet.font.add_file('HAMMRF.ttf')
        self.__setFont(1)

        self.__dicts = Dictionaries()
        __monitor = Monitor()
        __loading_Screen = DisplayLoading(__monitor.get_screensize())
        self.__config = Config(self.__dicts)
        if self.__config.get_Element("StaticSize")=="0":
            s=self.__GetWindowSize(__monitor.get_screensize())
        else:
            s=int(self.__config.get_Element("StaticSize"))

        self.__size_Num=self.__Create_Main_Window_By_Screen_Size(s, __monitor.get_screensize(), self.__config.get_Element("Language"))

    def __setFont(self, num):
        self.__fontSize=7+(num*2)
        self.__hammerFont=("Hammerfat", self.__fontSize)

    def __GetWindowSize(self, size):
        if size[0]>1600:
            s=4
        elif size[0]>1280:
            s=3
        elif size[0]>800:
            s=2
        else:
            s=1
        return(s)

    def __Create_Main_Window_By_Screen_Size(self, s, size, lang):

        if s==4:
            self.__create_Main_Window_size4(size, s)
        elif s==3:
            self.__create_Main_Window_size3(size, s)
        elif s==2:
            self.__create_Main_Window_size2(size, s)
        else:
            self.__create_Main_Window_size1(size, s)

        self.__main.title("Boo-T")
        self.__main.overrideredirect(False)
        self.__main.iconbitmap("icons/Boots.ico")
        self.__create_Menu(lang, s)
        return(s)

    def defineWords(self, lang):
        self.__new = self.__dicts.getWordFromDict(lang, "new")
        self.__open = self.__dicts.getWordFromDict(lang, "open")
        self.__file = self.__dicts.getWordFromDict(lang, "file")
        self.__save = self.__dicts.getWordFromDict(lang, "save")
        self.__save_as = self.__dicts.getWordFromDict(lang, "save_as")
        self.__copy = self.__dicts.getWordFromDict(lang, "copy")
        self.__paste = self.__dicts.getWordFromDict(lang, "paste")

        self.__HTML = self.__dicts.getWordFromDict(lang, "HTMLCode")
        self.__settings = self.__dicts.getWordFromDict(lang, "settings")
        self.__FastTest = self.__dicts.getWordFromDict(lang, "fastTest")
        self.__FFoxTest = self.__dicts.getWordFromDict(lang, "FFoxTest")
        self.__ChromeTest = self.__dicts.getWordFromDict(lang, "ChromeTest")
        self.__EdgeTest = self.__dicts.getWordFromDict(lang, "EdgeTest")
        self.__OperaTest = self.__dicts.getWordFromDict(lang, "OperaTest")
        self.__browserNotSet = self.__dicts.getWordFromDict(lang, "browserNotSet")
        self.__help = self.__dicts.getWordFromDict(lang, "help")
        self.__about = self.__dicts.getWordFromDict(lang, "about")


    def __create_Menu(self, lang, size):
        from PIL import ImageTk, Image

        self.__buttonSize=40
        self.defineWords(lang)
        self.__setFont(size)


        self.__imgNew = ImageTk.PhotoImage(Image.open("icons/new.png"))
        self.__new_B=Button(self.__main, image=self.__imgNew, width=32, height=32)
        self.__new_B.place(x=4, y=1)
        self.__new_B.bind("<Enter>", self.on_enterNewB)
        self.__new_B.bind("<Leave>", self.on_Leave)

        self.__imgOpen = ImageTk.PhotoImage(Image.open("icons/open.png"))
        self.__open_B=Button(self.__main, image=self.__imgOpen, width=32, height=32)
        self.__open_B.place(x=self.__getButtonPoz(1), y=1)
        self.__open_B.bind("<Enter>", self.on_enterOpenB)
        self.__open_B.bind("<Leave>", self.on_Leave)

        self.__imgSave = ImageTk.PhotoImage(Image.open("icons/save.png"))
        self.__save_B=Button(self.__main, image=self.__imgSave, width=32, height=32)
        self.__save_B.place(x=self.__getButtonPoz(2), y=1)
        self.__save_B.bind("<Enter>", self.on_enterSaveB)
        self.__save_B.bind("<Leave>", self.on_Leave)

        self.__imgSaveAs = ImageTk.PhotoImage(Image.open("icons/save_as.png"))
        self.__saveAs_B=Button(self.__main, image=self.__imgSaveAs, width=32, height=32)
        self.__saveAs_B.place(x=self.__getButtonPoz(3), y=1)
        self.__saveAs_B.bind("<Enter>", self.on_enterSaveAsB)
        self.__saveAs_B.bind("<Leave>", self.on_Leave)

        self.__imgCopy = ImageTk.PhotoImage(Image.open("icons/copy.png"))
        self.__saveAs_B=Button(self.__main, image=self.__imgCopy, width=32, height=32)
        self.__saveAs_B.place(x=self.__getButtonPoz(4.25), y=1)
        self.__saveAs_B.bind("<Enter>", self.on_enterCopy)
        self.__saveAs_B.bind("<Leave>", self.on_Leave)

        self.__imgPaste = ImageTk.PhotoImage(Image.open("icons/paste.png"))
        self.__saveAs_B=Button(self.__main, image=self.__imgPaste, width=32, height=32)
        self.__saveAs_B.place(x=self.__getButtonPoz(5.25), y=1)
        self.__saveAs_B.bind("<Enter>", self.on_enterPaste)
        self.__saveAs_B.bind("<Leave>", self.on_Leave)

        self.__imgHTML = ImageTk.PhotoImage(Image.open("icons/html.png"))
        self.__HTML_B=Button(self.__main, image=self.__imgHTML, width=32, height=32)
        self.__HTML_B.place(x=self.__getButtonPoz(6.5), y=1)
        self.__HTML_B.bind("<Enter>", self.on_enterHTML)
        self.__HTML_B.bind("<Leave>", self.on_Leave)

        self.__imgFastTest = ImageTk.PhotoImage(Image.open("icons/test.png"))
        self.__FTest_B=Button(self.__main, image=self.__imgFastTest, width=32, height=32)
        self.__FTest_B.place(x=self.__getButtonPoz(7.5), y=1)
        self.__FTest_B.bind("<Enter>", self.on_enterFastTest)
        self.__FTest_B.bind("<Leave>", self.on_Leave)

        self.__imgFFox = ImageTk.PhotoImage(Image.open("icons/firefox.png"))
        self.__FFox_B=Button(self.__main, image=self.__imgFFox, width=32, height=32)
        self.__FFox_B.place(x=self.__getButtonPoz(8.5), y=1)
        self.__FFox_B.bind("<Enter>", self.on_enterFFox)
        self.__FFox_B.bind("<Leave>", self.on_Leave)

        self.__imgChrome = ImageTk.PhotoImage(Image.open("icons/chrome.png"))
        self.__Chrome_B=Button(self.__main, image=self.__imgChrome, width=32, height=32)
        self.__Chrome_B.place(x=self.__getButtonPoz(9.5), y=1)
        self.__Chrome_B.bind("<Enter>", self.on_enterChrome)
        self.__Chrome_B.bind("<Leave>", self.on_Leave)

        self.__imgEdge = ImageTk.PhotoImage(Image.open("icons/edge.png"))
        self.__Edge_B=Button(self.__main, image=self.__imgEdge, width=32, height=32)
        self.__Edge_B.place(x=self.__getButtonPoz(10.5), y=1)
        self.__Edge_B.bind("<Enter>", self.on_enterEdge)
        self.__Edge_B.bind("<Leave>", self.on_Leave)

        self.__imgOpera = ImageTk.PhotoImage(Image.open("icons/opera.png"))
        self.__Opera_B=Button(self.__main, image=self.__imgOpera, width=32, height=32)
        self.__Opera_B.place(x=self.__getButtonPoz(11.5), y=1)
        self.__Opera_B.bind("<Enter>", self.on_enterOpera)
        self.__Opera_B.bind("<Leave>", self.on_Leave)

        self.__imgSettings = ImageTk.PhotoImage(Image.open("icons/settings.png"))
        self.__Settings_B=Button(self.__main, image=self.__imgSettings, width=32, height=32)
        self.__Settings_B.place(x=self.__getButtonPoz(12.75), y=1)
        self.__Settings_B.bind("<Enter>", self.on_enterSettings)
        self.__Settings_B.bind("<Leave>", self.on_Leave)

        self.__imgHelp = ImageTk.PhotoImage(Image.open("icons/help.png"))
        self.__Help_B=Button(self.__main, image=self.__imgHelp, width=32, height=32)
        self.__Help_B.place(x=self.__getButtonPoz(13.75), y=1)
        self.__Help_B.bind("<Enter>", self.on_enterHelp)
        self.__Help_B.bind("<Leave>", self.on_Leave)

        self.__imgAbout = ImageTk.PhotoImage(Image.open("icons/about.png"))
        self.__About_B=Button(self.__main, image=self.__imgAbout, width=32, height=32)
        self.__About_B.place(x=self.__getButtonPoz(14.75), y=1)
        self.__About_B.bind("<Enter>", self.on_enterAbout)
        self.__About_B.bind("<Leave>", self.on_Leave)

        self.CheckIfValid()

        self.__Hint=StringVar()
        self.__HintText = Label(self.__main, textvariable=self.__Hint, font=self.__hammerFont)

    def __getButtonPoz(self, num):
        return(4+(self.__buttonSize)*num)

    def CheckIfValid(self):
       if self.__config.get_Element("Chrome")=="":
           self.__Chrome_B.config(state=DISABLED)
       else:
           self.__Chrome_B.config(state=NORMAL)

       if self.__config.get_Element("FireFox")=="":
           self.__FFox_B.config(state=DISABLED)
       else:
           self.__FFox_B.config(state=NORMAL)
       if self.__config.get_Element("Edge") == "":
           self.__Edge_B.config(state=DISABLED)
       else:
           self.__Edge_B.config(state=NORMAL)
       if self.__config.get_Element("Opera") == "":
           self.__Opera_B.config(state=DISABLED)
       else:
           self.__Opera_B.config(state=NORMAL)

    def __create_Main_Window_size1(self, size, s):
        self.__windowW=640
        self.__windowH=420
        self.__setMainGeo(self.__windowW, self.__windowH, size)
        self.__createCodeBox(self.__hammerFont, 480, 420-(self.__hammerFont[1]*2+55), s)


    def __create_Main_Window_size2(self, size, s):
        self.__windowW=800
        self.__windowH=688
        self.__setMainGeo(self.__windowW, self.__windowH, size)
        self.__createCodeBox(self.__hammerFont, 632, 688-(self.__hammerFont[1]*2+55), s)

    def __create_Main_Window_size3(self, size, s):
        self.__windowW=800
        self.__windowH=1150
        self.__setMainGeo(self.__windowW, self.__windowH, size)
        self.__createCodeBox(self.__hammerFont, 632, 1150-(self.__hammerFont[1]*2+55), s)

    def __create_Main_Window_size4(self, size, s):
        self.__windowW=800
        self.__windowH=1400
        self.__setMainGeo(self.__windowW, self.__windowH, size)
        self.__createCodeBox(self.__hammerFont, 632, 1400-(self.__hammerFont[1]*2+55), s)

    def __setMainGeo(self, w, h, size):
        self.__main.geometry("%dx%d+%d+%d" % (w, h, (size[0]/2)-(w/2), (size[1]/2)-(h/2)-25))

    def __createCodeBox(self, baseFont, w, h, s):
        self.__CodeBox = tkscrolled.ScrolledText(self.__main, width=1, height=1, font=baseFont)
        self.__updateCodeBox(baseFont[1], w, h, s)

    def __updateCodeBox(self, basefontsize, w, h, s):
        from tkinter.font import Font

        if (self.__config.get_Element("DarkBox")=="False"):
            color="white"
            color2="black"
        else:
            color="black"
            color2="darkgray"

        hammerFont=Font(font='HammerFat')
        hammerFont.config(size=int(self.__config.get_Element("BoxFontSize")))

        self.__CodeBox.config(font=hammerFont, bg=color, fg=color2,
                              width=self.__howMany(s),
                              height=round((h-basefontsize-58)/hammerFont.metrics('linespace')))

        #print(hammerFont.metrics())
        #print(w, round(w/int(self.__config.get_Element("BoxFontSize"))), int(self.__config.get_Element("BoxFontSize")))
        #self.__CodeBox.insert(1.0, round(w/int(self.__config.get_Element("BoxFontSize")))*"A")
        self.__CodeBox.place(x=3, y=basefontsize+56)

    def __howMany(self, s):

        if s>1:
            numbers={
                12: 67,
                13: 67,
                14: 60,
                15: 55,
                16: 55,
                17: 52,
                18: 47,
                19: 47,
                20: 43,
                21: 40,
                22: 40,
                23: 36,
                24: 36,
                25: 34}
        else:
            numbers={
                12: 53,
                13: 53,
                14: 48,
                15: 43,
                16: 43,
                17: 40,
                18: 37,
                19: 37,
                20: 34,
                21: 32,
                22: 30,
                23: 28,
                24: 28,
                25: 26}

        return(numbers[int(self.__config.get_Element("BoxFontSize"))])




    def on_Leave(self, event):
        self.__Hint.set("")

    def __setHintTextLocation(self, num):
        self.__HintText.place(x=4+(self.__buttonSize)*num, y=self.__buttonSize)

    def on_enterNewB(self, event):
        self.__Hint.set(self.__new)
        self.__setHintTextLocation(0)

    def on_enterOpenB(self, event):
        self.__Hint.set(self.__open)
        self.__setHintTextLocation(0)

    def on_enterSaveB(self, event):
        self.__Hint.set(self.__save)
        self.__setHintTextLocation(0)

    def on_enterSaveAsB(self, event):
        self.__Hint.set(self.__save_as)
        self.__setHintTextLocation(0)

    def on_enterCopy(self, event):
        self.__Hint.set(self.__copy)
        self.__setHintTextLocation(4.25)

    def on_enterPaste(self, event):
        self.__Hint.set(self.__paste)
        self.__setHintTextLocation(4.25)

    def on_enterHTML(self, event):
        self.__Hint.set(self.__HTML)
        self.__setHintTextLocation(6.5)

    def on_enterFastTest(self, event):
        self.__Hint.set(self.__FastTest)
        self.__setHintTextLocation(6.5)

    def on_enterFFox(self, event):
        if self.__config.get_Element("FireFox")=="":
            self.__Hint.set(self.__browserNotSet.replace("#browser#", "Firefox"))
        else:
            self.__Hint.set(self.__FFoxTest)
        self.__setHintTextLocation(6.5)

    def on_enterChrome(self, event):
        if self.__config.get_Element("Chrome")=="":
            self.__Hint.set(self.__browserNotSet.replace("#browser#", "Chrome"))
        else:
            self.__Hint.set(self.__ChromeTest)
        self.__setHintTextLocation(6.5)

    def on_enterEdge(self, event):
        if self.__config.get_Element("FireFox")=="":
            self.__Hint.set(self.__browserNotSet.replace("#browser#", "Edge"))
        else:
            self.__Hint.set(self.__EdgeTest)
        self.__setHintTextLocation(6.5)

    def on_enterOpera(self, event):
        if self.__config.get_Element("Opera")=="":
            self.__Hint.set(self.__browserNotSet.replace("#browser#", "Opera"))
        else:
            self.__Hint.set(self.__OperaTest)
        self.__setHintTextLocation(6.5)

    def on_enterSettings(self, event):
        self.__Hint.set(self.__settings)
        self.__setHintTextLocation(12.75)

    def on_enterHelp(self, event):
        self.__Hint.set(self.__help)
        self.__setHintTextLocation(12.75)

    def on_enterAbout(self, event):
        self.__Hint.set(self.__about)
        self.__setHintTextLocation(12.75)

class Create_MainWindow(Create_MainWindow_Real):

    def __init__(self, main):
        super().__init__(main)

if __name__=="__main__":

    Main_Window = Tk()
    Creator = Create_MainWindow(Main_Window)
    Main_Window.mainloop()

