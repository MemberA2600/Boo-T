from tkinter import *
from abc import *
import os
import sys
import re
from tkinter.filedialog import *
from tkinter import messagebox

from Dictionaries import *
from Config import *
from Monitor import *


class OptionsMenu_REAL(ABC):

    @abstractmethod
    def __init__(self, dicts, config, hammer, imgChrome, imgFFox, imgEdge, imgOpera, master, main, fontSize, monitor):
        """The most importan elemets are inherited from the main window."""

        self.__dicts=dicts
        self.__Config=config
        self.__hammerFont=hammer

        self.__imgChrome=imgChrome
        self.__imgFFox=imgFFox
        self.__imgEdge=imgEdge
        self.__imgOpera=imgOpera

        self.master=master

        self.__main=main

        self.__OptionsM = Toplevel()
        self.__OptionsM.title(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "settings"))
        self.__OptionsM.resizable(False, False)

        """The OptiomMen has only two sizes, one for extra small screens and a normal."""

        __monitor = monitor
        __s = __monitor.get_screensize()
        if __s[0] < 800:
            __w = 480
            __h = 240
        else:
            __w = 640
            __h = 380

        self.__setOptionsMenuSize(__w, __h, __s)
        self.__OptionsCreateMenu(__w, __h, __s, fontSize, hammer)


    def __OptionsCreateMenu(self, __w, __h, __s, fontSize, hammer):
        """Creates the menu where you can change the config file on GUI."""

        from tkinter.font import Font, families
        from PIL import ImageTk, Image

        self.__OptionsM.pack_propagate(False)
        hammerFont = Font(font='Hammerfat_Hun')
        hammerFont.config(size=fontSize+4)


        hammerheight = hammerFont.metrics("linespace")

        """CompilerFrame starts here."""
        self.__createCompilerFrame(__w, __h, __s)
        self.__intCompiler = IntVar()

        if self.__Config.get_Element("FortranCompiler") == "True":
            self.__intCompiler.set(2)
        else:
            self.__intCompiler.set(1)

        self.__compilerPython = Radiobutton(self.__compilerFrame, variable=self.__intCompiler, value=1,
                                            text="Python", font=self.__hammerFont)
        self.__compilerPython.place(x=10, y=round(hammerheight / 4))
        self.__imgPython = ImageTk.PhotoImage(Image.open("icons/python.png"))
        self.__imgPythonLabel = Label(self.__compilerFrame, image=self.__imgPython)
        self.__imgPythonLabel.place(x=25 + hammerFont.measure("Python"), y=hammerheight / 4 - 10)

        self.__compilerFortran = Radiobutton(self.__compilerFrame, variable=self.__intCompiler, value=2,
                                             text="Fortran", font=self.__hammerFont)
        self.__compilerFortran.place(x=round((__w) / 4), y=round(hammerheight / 4))
        self.__imgFortran = ImageTk.PhotoImage(Image.open("icons/fortran.png"))
        self.__imgFortranLabel = Label(self.__compilerFrame, image=self.__imgFortran)
        self.__imgFortranLabel.place(x=round((__w) / 4) + 15 + hammerFont.measure("Fortran"),
                                     y=(round(hammerheight / 4 - 10)))

        """Browserframe starts here"""
        __relative1 = round(__h / 10) + self.__hammerFont[1] * 2 + 5

        __bFrameWidth = round((__w) / 2) - 10

        self.__createBrowserFrame(__w, __h, __s, __relative1, __bFrameWidth, hammerFont, hammerheight)


        """BasicSettings Frame Starts here"""
        self.__createBasicSettingsFrame(__w, __h, __s, __relative1, __bFrameWidth, hammerFont, hammerheight)


        """ButtonFrame starts here"""
        self.__createButtonFrame(__w, __h, __s, hammerFont, hammerheight)

        self.__setWindowLayout()

        self.__OptionsM.wait_window()

    def __createCompilerFrame(self, __w, __h, __s):
        """Contains the two radiobuttons with the Python and Fortran logos."""
        self.__compilerFrame = LabelFrame(self.__OptionsM, width=round((__w) / 2) - 10,
                                          height=round(__h / 10) + self.__hammerFont[1] * 2,
                                          text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                            "compiler"), font=self.__hammerFont)
        self.__compilerFrame.place(x=5, y=5)
        self.__compilerFrame.bind("<Enter>", self.__OptionsCompFrameLabel)
        self.__compilerFrame.pack_propagate(False)

    def __createBrowserFrame(self, __w, __h, __s, __relative1, __bFrameWidth, hammerFont, hammerheight):
        """In this frame, the user can change location of the browsers., also change the autosearch option at startup."""

        self.__browserFrame = LabelFrame(self.__OptionsM, width=__bFrameWidth,
                                         height=round(__h / 2) + self.__hammerFont[1] * 3,
                                         text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                           "browserSettings"), font=self.__hammerFont)
        self.__browserFrame.place(x=5, y=__relative1)
        self.__browserFrame.bind("<Enter>", self.__OptionsBrowFrameLabel)
        self.__browserFrame.pack_propagate(False)

        self.__autoSearch = IntVar()
        if self.__Config.get_Element("AutoCheckForInstalledBrowsers") == "True":
            self.__autoSearch.set(1)
        else:
            self.__autoSearch.set(0)

        self.__autoS = Checkbutton(self.__browserFrame, variable=self.__autoSearch,
                                   text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                     "browserAuto"), font=self.__hammerFont)
        self.__autoS.place(x=5, y=round(hammerheight / 4) - 1)

        __buttonWidth = self.__getAmmountOfChar(__bFrameWidth, hammerFont)

        self.__iconChrome = Label(self.__browserFrame, image=self.__imgChrome, width=32, height=32)
        self.__iconChrome.place(x=5, y=round(hammerheight / 4) + hammerheight)
        self.__buttonSettingsChrome = Button(self.__browserFrame, width=__buttonWidth, command=self.__setPathChrome,
                                             text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                               "browserPathButtonText").replace(
                                                 "#browser#", "Chrome"), font=self.__hammerFont)
        self.__buttonSettingsChrome.place(x=44,
                                          y=round(hammerheight / 4) + hammerheight + round((32 - hammerheight / 2) / 8))

        self.__iconFireFox = Label(self.__browserFrame, image=self.__imgFFox, width=32, height=32)
        self.__iconFireFox.place(x=5, y=round(hammerheight / 4) + hammerheight + 40)
        self.__buttonSettingsFireFox = Button(self.__browserFrame, width=__buttonWidth, command=self.__setPathFireFox,
                                              text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                                "browserPathButtonText").replace(
                                                  "#browser#", "FireFox"), font=self.__hammerFont)
        self.__buttonSettingsFireFox.place(x=44, y=round(hammerheight / 4) + hammerheight + round(
            (32 - hammerheight / 2) / 8) + 40)

        self.__iconEdge = Label(self.__browserFrame, image=self.__imgEdge, width=32, height=32)
        self.__iconEdge.place(x=5, y=round(hammerheight / 4) + hammerheight + 80)
        self.__buttonSettingsEdge = Button(self.__browserFrame, width=__buttonWidth, command=self.__setPathEdge,
                                           text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                             "browserPathButtonText").replace(
                                               "#browser#", "Edge"), font=self.__hammerFont)
        self.__buttonSettingsEdge.place(x=44, y=round(hammerheight / 4) + hammerheight + round(
            (32 - hammerheight / 2) / 8) + 80)

        self.__iconOpera = Label(self.__browserFrame, image=self.__imgOpera, width=32, height=32)
        self.__iconOpera.place(x=5, y=round(hammerheight / 4) + hammerheight + 120)
        self.__buttonSettingsOpera = Button(self.__browserFrame, width=__buttonWidth, command=self.__setPathOpera,
                                            text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                              "browserPathButtonText").replace(
                                                "#browser#", "Opera"), font=self.__hammerFont)
        self.__buttonSettingsOpera.place(x=44, y=round(hammerheight / 4) + hammerheight + round(
            (32 - hammerheight / 2) / 8) + 120)

    def __createBasicSettingsFrame(self, __w, __h, __s, __relative1, __bFrameWidth, hammerFont, hammerheight):
        """Set basic settings for the application."""

        self.__basicSettingsFrame = LabelFrame(self.__OptionsM, width=__bFrameWidth - 5, height=__h - 86,
                                               text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                                 "basicSettings"),
                                               font=self.__hammerFont)
        self.__basicSettingsFrame.place(x=round(__w / 2) + 5, y=5)
        self.__basicSettingsFrame.pack_propagate(False)

        __languages = self.__getLanguages()
        __w_Of_Options = self.__getAmmountOfChar(round(__bFrameWidth - 5 - round((__bFrameWidth - 5) / 2.5)),
                                                 hammerFont)

        self.__labelLanguage = Label(self.__basicSettingsFrame,
                                     text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                       "language"), font=self.__hammerFont)
        self.__labelLanguage.place(x=5, y=5)

        self.__langVar = StringVar()
        self.__languageOption = OptionMenu(self.__basicSettingsFrame, self.__langVar, *tuple(__languages))
        self.__languageOption.config(font=(self.__hammerFont[0], self.__hammerFont[1] - 2), width=__w_Of_Options,
                                     justify=LEFT)
        self.__languageOption.place(x=round((__bFrameWidth - 5) / 2.5), y=3)

        self.__labelBoxSize = Label(self.__basicSettingsFrame,
                                    text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "boxSize"),
                                    font=self.__hammerFont)
        self.__labelBoxSize.place(x=5, y=10 + hammerheight)

        self.__windowSSize = tuple(["Auto", "1 (640x480)", "2 (800x600)", "3 (1600x1200)", "4"])

        self.__windowSize = StringVar()

        self.__boxOption = OptionMenu(self.__basicSettingsFrame, self.__windowSize, *self.__windowSSize)
        self.__boxOption.config(font=(self.__hammerFont[0], self.__hammerFont[1] - 2), width=__w_Of_Options,
                                justify=LEFT)

        self.__boxOption.place(
            x=round((__bFrameWidth - 5) / 2.5),
            y=10 + hammerheight)

        self.__labelBColor = Label(self.__basicSettingsFrame,
                                   text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "boxColor"),
                                   font=self.__hammerFont)
        self.__labelBColor.place(x=5, y=15 + hammerheight * 2)

        self.__boxColorVar = StringVar()

        self.__colorOption = OptionMenu(self.__basicSettingsFrame, self.__boxColorVar, *tuple([
            self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "light"),
            self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "dark")]))
        self.__colorOption.config(font=(self.__hammerFont[0], self.__hammerFont[1] - 2), width=__w_Of_Options,
                                  justify=LEFT)
        self.__colorOption.place(x=round((__bFrameWidth - 5) / 2.5), y=15 + hammerheight * 2)
        self.__changeOptionColorCOLOR("a", "b", "c")
        self.__boxColorVar.trace_add("write", self.__changeOptionColorCOLOR)

        self.__boxFontLabel=Label(self.__basicSettingsFrame, text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "boxFont"), font=self.__hammerFont)
        self.__boxFontLabel.place(x=5, y=20 + hammerheight * 3)

        self.__boxFontSize=StringVar()
        self.__boxAuto=BooleanVar()


        self.__autoBox=Checkbutton(self.__basicSettingsFrame, variable=self.__boxAuto, text="Auto", font=self.__hammerFont)
        self.__autoBox.place(x=hammerFont.measure(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "boxFont"))-20
                           , y=20 + hammerheight * 3)
        self.__boxAuto.trace_add("write", self.__checkAutoBox)

        self.__entrySize=Entry(self.__basicSettingsFrame, width=2, font=self.__hammerFont,
                               textvariable=self.__boxFontSize)

        self.__entrySize.place(x=hammerFont.measure(str(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "boxFont")+"[ ]Auto"))-15
                           , y=22 + hammerheight * 3)
        self.__checkAutoBox("a", "b", "c")

        self.__recentLabel=Label(self.__basicSettingsFrame, text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "maxRecent"), font=self.__hammerFont)
        self.__recentLabel.place(x=5, y=22 + hammerheight * 4)

        self.__recentNum=StringVar()
        self.__boxInf=BooleanVar()

        self.__boxInf.trace_add("write", self.__checkInfBox)
        self.__infBox=Checkbutton(self.__basicSettingsFrame, variable=self.__boxInf, text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "infinite"),
                                  font=self.__hammerFont)
        self.__infBox.place(x=hammerFont.measure(str(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "boxFont")+"[ ]Auto"))-30-
                              hammerFont.measure(str(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "infinite")))
                           , y=25 + hammerheight * 5)

        self.__recentEntry=  Entry(self.__basicSettingsFrame, width=2, font=self.__hammerFont,
                               textvariable=self.__recentNum)
        self.__recentEntry.place(x=hammerFont.measure(str(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "boxFont")+"[ ]Auto"))-15
                           , y=27 + hammerheight * 5)

        #self.__checkInfBox("a", "b", "c")
        self.__recentNum.trace_add("write", self.__recentCheck)
        self.__boxFontSize.trace_add("write", self.__fontSizeCheck)

        self.__boxQuick=BooleanVar()
        self.__quickNum=StringVar()
        self.__quickBox = Checkbutton(self.__basicSettingsFrame, variable=self.__boxQuick,
                                    text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                      "autoSave"),
                                    font=self.__hammerFont)
        self.__quickBox.place(x=5, y=32 + hammerheight * 6)

        self.__loadDisplay = BooleanVar()
        self.__loadDisplayBox = Checkbutton(self.__basicSettingsFrame, variable=self.__loadDisplay,
                                    text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                      "noLoadingScreen"),
                                    font=self.__hammerFont)

        self.__loadDisplayBox.place(x=5, y=32 + hammerheight * 7)

        self.__quickEntry = Entry(self.__basicSettingsFrame, width=2, font=self.__hammerFont,
                                   textvariable=self.__quickNum)
        self.__quickEntry.place(x=hammerFont.measure(
            str(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "autoSave")+"A")) - 15
                                 , y=30 + hammerheight * 6)

        self.__minutesLabel=Label(self.__basicSettingsFrame, text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "minutes"), font=self.__hammerFont)
        self.__minutesLabel.place(x=hammerFont.measure(
            str(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "autoSave")+"A[ ]")) - 15, y=32 + hammerheight * 6)

        self.__boxQuick.trace_add("write", self.__checkQuickBox)
        self.__quickNum.trace_add("write", self.__quickCheck)

        #self.__checkQuickBox("a", "b", "c")


    def __formatXY(self, the_V):
        """This prevents the user to set a not allowed value for the box.
        If a non-number character is entered, it wil be deleted, also the characters above 2 are deleted
        as well. If the user enters 0X, 0 is removed."""

        if len(the_V)>2:
            the_V=the_V[:2]
        try:
            temp=int(the_V[-1])
        except:
            the_V=the_V[:-2]
        if len(the_V)==2 and the_V[0]=="0":
           the_V=the_V[1]

        return(the_V)


    def __fontSizeCheck(self, a, b, c):
        """Checks if the entered characters are correct.
        Also won't let entering less than 12 and more then 48."""

        self.__boxFontSize.set(self.__formatXY(self.__boxFontSize.get()))

        if len(self.__boxFontSize.get())>0:
            if int(self.__boxFontSize.get())>48:
                self.__boxFontSize.set("48")
            elif int(self.__boxFontSize.get())<12:
                self.__boxFontSize.set("12")



    def __recentCheck(self, a, b, c):
        """Checks if the entered characters are correct."""

        self.__recentNum.set(self.__formatXY(self.__recentNum.get()))


    def __quickCheck(self, a, b, c):
        """Checks if the entered characters are correct."""

        self.__quickNum.set(self.__formatXY(self.__quickNum.get()))



    def __checkAutoBox(self, a, b, c):
        self.__enableDisableBox(True, self.__boxAuto.get(), self.__entrySize, self.__boxFontSize)

    def __checkInfBox(self, a, b, c):
        self.__enableDisableBox(True, self.__boxInf.get(), self.__recentEntry, self.__recentNum)

    def __checkQuickBox(self, a, b, c):
        self.__enableDisableBox(False, self.__boxQuick.get(), self.__quickEntry, self.__quickNum)


    def __enableDisableBox(self, reverse, val, entry, num):
        """Sets entry if checkbox is changed."""

        if reverse==True:
            val = not val

        if val==True:
            entry.config(state=NORMAL)
        else:
            num.set("")
            entry.config(state=DISABLED)


    def __createButtonFrame(self, __w, __h, __s, hammerFont, hammerheight):
        self.__mainButtonaForOptionsFrame = Frame(self.__OptionsM, width=__w - 20, height=hammerheight * 2, )
        self.__mainButtonaForOptionsFrame.bind("<Enter>", self.__OptionsButFrameLabel)
        self.__mainButtonaForOptionsFrame.place(x=17, y=__h - (hammerheight * 2))
        self.__mainButtonaForOptionsFrame.pack_propagate(False)

        third = self.__getAmmountOfChar(round(__w / 3) - 75, hammerFont)

        self.__mainButtonOK = Button(self.__mainButtonaForOptionsFrame, width=third,
                                     text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                       "SettingsOK"), font=hammerFont,
                                         command=self.__saveSettings)
        self.__mainButtonOK.place(x=0, y=0)

        self.__mainButtonCancel = Button(self.__mainButtonaForOptionsFrame, width=third,
                                         text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                           "Cancel"), font=hammerFont,
                                         command=self.__destroyWindow)
        self.__mainButtonCancel.place(x=round(__w / 3), y=0)

        self.__mainButtonDefaults = Button(self.__mainButtonaForOptionsFrame, width=third,
                                           text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                             "Defaults"), font=hammerFont,
                                           command=self.__loadDef)
        self.__mainButtonDefaults.place(x=round(__w / 3) * 2, y=0)


    def __changeOptionColorCOLOR(self, a, b, c):
        if self.__boxColorVar.get() ==  self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "light"):
            self.__colorOption.config(bg="white", fg="black", activebackground="white", activeforeground="black")
        else:
            self.__colorOption.config(bg="black", fg="lightgray", activebackground="black",
                                      activeforeground="lightgray")

    def __saveSettings(self):
        self.__saveSettingsToConfig()
        self.__Config.saveConfig()
        self.__setWindowLayout()
        self.__destroyWindow()
        if self.__haveToRestart==True:
            self.__resStart()

    def __saveSettingsToConfig(self):
        self.__haveToRestart=False

        if self.__intCompiler.get()==1:
            self.__Config.set_Element("FortranCompiler", "False")
        else:
            self.__Config.set_Element("FortranCompiler", "True")

        if self.__autoSearch.get()==0:
            self.__Config.set_Element("AutoCheckForInstalledBrowsers" , "False")
        else:
            self.__Config.set_Element("AutoCheckForInstalledBrowsers" , "True")

        if self.__boxColorVar.get()==self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "light"):
            self.__Config.set_Element("DarkBox", "False")
        else:
            self.__Config.set_Element("DarkBox", "True")

        temp=self.__Config.get_Element("Language")
        self.__Config.set_Element("Language", self.__langVar.get())
        if temp!=self.__Config.get_Element("Language"):
            self.__haveToRestart=True

        temp=self.__Config.get_Element("StaticSize")
        if self.__windowSize.get()=="Auto":
            self.__Config.set_Element("StaticSize", "0")
        else:
            self.__Config.set_Element("StaticSize", self.__windowSize.get()[0])
        if temp!=self.__Config.get_Element("StaticSize"):
            self.__haveToRestart=True

        if self.__boxAuto.get()==True:
            self.__Config.set_Element("BoxFontSize", "0")
        else:
            self.__Config.set_Element("BoxFontSize", self.__boxFontSize.get())

        if self.__boxInf.get()==True:
            self.__Config.set_Element("MaxRecent", "0")
        else:
            self.__Config.set_Element("MaxRecent", self.__recentNum.get())

        if self.__boxQuick.get() == False:
            self.__Config.set_Element("AutoSave", "0")
        else:
            self.__Config.set_Element("AutoSave", self.__quickNum.get())

        if self.__loadDisplay.get() == False:
            self.__Config.set_Element("noLoading", "True")
        else:
            self.__Config.set_Element("noLoading", "False")

    def __getLongest(self, __list):
        num = 0
        for item in __list:
            if len(item) > num:
                num = len(item)
        return (num)


    def __getLanguages(self):
        names = []
        for root, dirs, files in os.walk("dicts/"):
            for file in files:
                names.append(".".join(file.split(".")[:-1]))
        return (names)


    def __getAmmountOfChar(self, w, font):
        tempLen = 0
        while (font.measure((tempLen) * "A") < (w + 40)):
            tempLen += 1

        return (tempLen)


    def __destroyWindow(self):
        self.__OptionsM.destroy()


    def __loadDef(self):

        temp=self.__Config.get_Element("Language")
        temp2=self.__Config.get_Element("StaticSize")

        self.__Config.load_Config_Defaults()
        self.__Config.saveConfig()
        self.__setWindowLayout()

        if temp!=self.__Config.get_Element("Language") or temp2!=self.__Config.get_Element("StaticSize"):
            self.__resStart()


    def __resStart(self):
        m = messagebox.showinfo(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "restartTitle"),
                                self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "restartText"))
        self.master.saveQuickSave()
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    def __setWindowLayout(self):
        if self.__Config.get_Element("FortranCompiler") == "True":
            self.__intCompiler.set(2)
        else:
            self.__intCompiler.set(1)

        if self.__Config.get_Element("AutoCheckForInstalledBrowsers") == "True":
            self.__autoSearch.set(1)
        else:
            self.__autoSearch.set(0)

        self.__langVar.set(self.__Config.get_Element("Language"))

        self.__windowSize.set(self.__windowSSize[int(self.__Config.get_Element("StaticSize"))])
        if self.__Config.get_Element("DarkBox") == "True":
            self.__boxColorVar.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "dark"))
        else:
            self.__boxColorVar.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "light"))

        if self.__Config.get_Element("BoxFontSize")=="0":
            self.__boxAuto.set(True)
            self.__boxFontSize.set("")
        else:
            self.__boxAuto.set(False)
            self.__boxFontSize.set(self.__Config.get_Element("BoxFontSize"))

        if self.__Config.get_Element("MaxRecent")=="0":
            self.__boxInf.set(True)
            self.__recentNum.set("")
        else:
            self.__boxInf.set(False)
            self.__recentNum.set(self.__Config.get_Element("MaxRecent"))

        if self.__Config.get_Element("AutoSave")=="0":
            self.__boxQuick.set(False)
            self.__recentNum.set("")
        else:
            self.__boxQuick.set(True)
            self.__quickNum.set(self.__Config.get_Element("AutoSave"))

        if self.__Config.get_Element("noLoading")=="False":
            self.__loadDisplay.set(True)
        else:
            self.__loadDisplay.set(False)

        self.master.updateCodeBox()


    def __setOptionsMenuSize(self, w, h, size):
        self.__OptionsM.geometry("%dx%d+%d+%d" % (w, h, (size[0] / 2) - (w / 2), (size[1] / 2) - (h / 2) - 25))


    def __OptionsCompFrameLabel(self, event):
        self.master.create_StatLabel(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "compilerLabel"))


    def __OptionsBrowFrameLabel(self, event):
        self.master.create_StatLabel(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "browserLabel"))


    def __OptionsButFrameLabel(self, event):
        self.master.create_StatLabel(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "buttonLabel"))


    def __setPathChrome(self):
        self.__Config.set_Element("Chrome", self.__openToGetPath("Chrome"))
        self.__OptionsM.focus()


    def __setPathFireFox(self):
        self.__Config.set_Element("FireFex", self.__openToGetPath("FireFox"))
        self.__OptionsM.focus()


    def __setPathEdge(self):
        self.__Config.set_Element("Edge", self.__openToGetPath("Edge"))
        self.__OptionsM.focus()


    def __setPathOpera(self):
        self.__Config.set_Element("Opera", self.__openToGetPath("Opera"))
        self.__OptionsM.focus()


    def __openToGetPath(self, browser):
        default_path = self.__Config.get_Element(browser)
        path = ""
        if default_path == "":
            if self.__Config.get_OS()=="Windows":
                startdir = "C:\\"
            else:
                startdir = "/usr/bin/"
        else:
            startdir = "/".join(default_path.split("/")[:-1])


        path = askopenfilename(initialdir=startdir,
                               title=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "open"),
                               filetypes=(
                                   (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "executable"),
                                    "*.exe"),))

        if path == "" or path.endswith(".exe") == False:
            return (default_path)
        else:
            return (path)


class OptionsMenu(OptionsMenu_REAL):

    def __init__(self, dicts, config, hammer, imgChrome, imgFFox, imgEdge, imgOpera, master, main, fontsize, monitor):
        super().__init__(dicts, config, hammer, imgChrome, imgFFox, imgEdge, imgOpera, master, main, fontsize, monitor)