from tkinter import *
import os
import re
from tkinter.filedialog import *
from tkinter import messagebox

class OptionsMenu():

    def __init__(self, dicts, config, hammer, imgChrome, imgFFox, imgEdge, imgOpera, master, main, fontSize, monitor):
        """The most importan elemets are inherited from the main window."""

        self.__dicts=dicts
        self.__Config=config
        self.__hammerFont=hammer

        self.__imgChrome=imgChrome
        self.__imgFFox=imgFFox
        self.__imgEdge=imgEdge
        self.__imgOpera=imgOpera

        self.__master=master

        self.__main=main

        self.__OptionsM = Toplevel()
        self.__OptionsM.title(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "settings"))
        self.__OptionsM.resizable(False, False)

        """The OptiomMen has only two sizes, one for extra small screens and a normal."""

        __monitor = monitor
        __s = __monitor.get_screensize()
        if __s[0] < 800 or __s[1] < 600:
            __w = 480
            __h = 240
        else:
            __w = 640
            __h = 380

        self.__setOptionsMenuSize(__w, __h, __s)
        self.__OptionsCreateMenu(__w, __h, __s, fontSize)


    def __OptionsCreateMenu(self, __w, __h, __s, fontSize):
        """Creates the menu where you can change the config file on GUI."""

        from tkinter.font import Font, families

        self.__OptionsM.pack_propagate(False)
        hammerFont = Font(font='Hammerfat_Hun')
        hammerFont.config(size=fontSize+4)


        hammerheight = hammerFont.metrics("linespace")

        """CompilerFrame starts here."""
        self.__createCompilerFrame(__w, __h, __s)
        self.__intCompiler = IntVar()

        if self.__Config.get_Element("FortranCompiler") == "True" and self.__Config.get_OS_Name()!="Linux":
            self.__intCompiler.set(2)
        else:
            self.__intCompiler.set(1)

        """Had to put these two here, instead of '__createCompilerFrame', they don't work properly that way, reason unknown"""
        self.__compilerPython, self.__imgPython, self.__imgPythonLabel = self.__compilerLabelButton(1, "Python", 10, hammerheight, hammerFont, "icons/python.png")
        self.__compilerFortran, self.__imgFortran, self.__imgFortranLabel = self.__compilerLabelButton(2, "Fortran", round((__w) / 4), hammerheight, hammerFont, "icons/fortran.png")

        if self.__Config.get_OS_Name()=="Linux":
            self.__compilerFortran.config(state="disabled")
            self.__imgFortranLabel.config(state="disabled")


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

    def __compilerLabelButton(self, value, text, placeX, hammerheight, hammerFont, imgpath):
        """Creates the radiobutton, label of images and texts for the compiler choices."""


        from PIL import ImageTk, Image

        radio = Radiobutton(self.__compilerFrame, variable=self.__intCompiler, value=value,
                                            text=text, font=self.__hammerFont)
        radio.place(x=placeX, y=round(hammerheight / 4))
        img = ImageTk.PhotoImage(Image.open(imgpath))
        label = Label(self.__compilerFrame, image=img)
        label.place(x=placeX + 15 + hammerFont.measure(text), y=hammerheight / 4 - 10)

        return(radio, img, label)

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

        self.__iconFireChrome, self.__buttonSettingsChrome = self.__createBrowserLabelButton(
            self.__imgChrome, hammerheight, __buttonWidth, 0, self.__setPathChrome, "Chrome")

        self.__iconFireFox, self.__buttonSettingsFireFox = self.__createBrowserLabelButton(
            self.__imgFFox, hammerheight, __buttonWidth, 40, self.__setPathFireFox, "Firefox")

        self.__iconEdge, self.__buttonSettingsEdge = self.__createBrowserLabelButton(
            self.__imgEdge, hammerheight, __buttonWidth, 80, self.__setPathEdge, "Edge")

        self.__iconOpera, self.__buttonSettingsOpera = self.__createBrowserLabelButton(
            self.__imgOpera, hammerheight, __buttonWidth, 120, self.__setPathOpera, "Opera")

    def __createBrowserLabelButton(self, image, hammerheight, w, plus, command, browsername):
        """Creates the browser icon label and the button that allows the user
        to set the path to the tester browsers."""

        icon = Label(self.__browserFrame, image=image, width=32, height=32)
        icon.place(x=5, y=round(hammerheight / 4) + hammerheight + plus)
        button = Button(self.__browserFrame, width=w, command=command,
                                            text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                              "browserPathButtonText").replace(
                                                "#browser#", browsername), font=self.__hammerFont)
        button.place(x=44, y=round(hammerheight / 4) + hammerheight + round(
            (32 - hammerheight / 2) / 8) + plus)
        return(icon, button)


    def __createBasicSettingsFrame(self, __w, __h, __s, __relative1, __bFrameWidth, hammerFont, hammerheight):
        """Set basic settings for the application."""

        self.__basicSettingsFrame = LabelFrame(self.__OptionsM, width=__bFrameWidth - 5, height=__h - 65,
                                               text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                                 "basicSettings"),
                                               font=self.__hammerFont)
        self.__basicSettingsFrame.place(x=round(__w / 2) + 5, y=5)
        self.__basicSettingsFrame.pack_propagate(False)
        self.__basicSettingsFrame.bind("<Enter>", self.__BasicSettingsFrameLabel)


        __w_Of_Options = self.__getAmmountOfChar(round(__bFrameWidth - 5 - round((__bFrameWidth - 5) / 2.5)),
                                                 hammerFont)

        __languages = self.__getLanguages()

        self.__labelLanguage, self.__langVar, self.__languageOption = \
            self.__createLabelOptionMenu(__w_Of_Options, __bFrameWidth, "language", hammerheight, 1, self.__getLanguages())


        self.__windowSSize = tuple(["Auto", "1 (640x480)", "2 (800x600)", "3 (1600x1200)", "4 (XXL)"])

        self.__labelBoxSize, self.__windowSize, self.__boxOption = \
            self.__createLabelOptionMenu(__w_Of_Options, __bFrameWidth, "boxSize", hammerheight, 2, self.__windowSSize)

        self.__labelBColor, self.__boxColorVar, self.__colorOption = \
        self.__createLabelOptionMenu(__w_Of_Options, __bFrameWidth, "boxColor", hammerheight, 3, tuple([
                                             self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                          "light"),
                                             self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                          "dark")]))

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
                           , y=20 + hammerheight * 5)

        self.__recentEntry=  Entry(self.__basicSettingsFrame, width=2, font=self.__hammerFont,
                               textvariable=self.__recentNum)
        self.__recentEntry.place(x=hammerFont.measure(str(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "boxFont")+"[ ]Auto"))-15
                           , y=22 + hammerheight * 5)

        #self.__checkInfBox("a", "b", "c")
        self.__recentNum.trace_add("write", self.__recentCheck)
        self.__boxFontSize.trace_add("write", self.__fontSizeCheck)

        self.__boxQuick=BooleanVar()
        self.__quickNum=StringVar()
        self.__quickBox = self.__createBox(self.__boxQuick,
                          self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),"autoSave"), 32 + hammerheight * 6)

        self.__loadDisplay = BooleanVar()
        self.__loadDisplayBox = self.__createBox(self.__loadDisplay,
                                self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),"noLoadingScreen"),
                                32 + hammerheight * 7)

        self.__quickEntry = Entry(self.__basicSettingsFrame, width=2, font=self.__hammerFont,
                                   textvariable=self.__quickNum)
        self.__quickEntry.place(x=hammerFont.measure(
            str(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "autoSave")+"A")) - 15
                                 , y=32 + hammerheight * 6)

        self.__minutesLabel=Label(self.__basicSettingsFrame, text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "minutes"), font=self.__hammerFont)
        self.__minutesLabel.place(x=hammerFont.measure(
            str(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "autoSave")+"A[ ]")) - 15, y=32 + hammerheight * 6)

        self.__loadTemplate = BooleanVar()
        self.__loadTemplateBox = self.__createBox(self.__loadTemplate,
                                 self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "template"), 32 + hammerheight * 8)

        self.__boxQuick.trace_add("write", self.__checkQuickBox)
        self.__quickNum.trace_add("write", self.__quickCheck)

        #self.__checkQuickBox("a", "b", "c")

    def __createLabelOptionMenu(self, __w_Of_Options, __bFrameWidth, word, hammerheight, multi, tuple):
        """Creates text label with optionmenu and the choices included."""

        label = Label(self.__basicSettingsFrame,
                                    text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), word),
                                    font=self.__hammerFont)
        label.place(x=5, y=5*multi + hammerheight * (multi-1))

        var = StringVar()

        option = OptionMenu(self.__basicSettingsFrame, var, *tuple)
        option.config(font=(self.__hammerFont[0], self.__hammerFont[1] - 2), width=__w_Of_Options,
                                justify=LEFT)

        option.place(
            x=round((__bFrameWidth - 5) / 2.5), y=5*multi + hammerheight * (multi-1))

        return(label, var, option)

    def __createBox(self, var, text, Y):
        """Helps to set attributes for the three very alike checkboxes."""

        box = Checkbutton(self.__basicSettingsFrame, variable=var, text=text, font=self.__hammerFont)
        box.place(x=5, y=Y)
        return(box)

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
        """Creates the three buttons at the bottom of the window."""

        self.__mainButtonaForOptionsFrame = Frame(self.__OptionsM, width=__w - 20, height=hammerheight * 2, )
        self.__mainButtonaForOptionsFrame.bind("<Enter>", self.__OptionsButFrameLabel)
        self.__mainButtonaForOptionsFrame.place(x=17, y=__h - (hammerheight * 2))
        self.__mainButtonaForOptionsFrame.pack_propagate(False)

        third = self.__getAmmountOfChar(round(__w / 3) - 75, hammerFont)

        self.__mainButtonOK = self.__createBottomButton(third, "SettingsOK", hammerFont, self.__saveSettings, 0, __w)
        self.__mainButtonCancel = self.__createBottomButton(third, "Cancel", hammerFont, self.__destroyWindow, 1, __w)
        self.__mainButtonDefaults = self.__createBottomButton(third, "Defaults", hammerFont, self.__loadDef, 2, __w)


    def __createBottomButton(self, third, word, hammerFont, command, multi, __w):
        """Creating a button."""

        button = Button(self.__mainButtonaForOptionsFrame, width=third,
                                     text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                       word), font=hammerFont,
                                     command=command)
        button.place(x=round(__w / 3) * multi, y=0)
        return(button)

    def __changeOptionColorCOLOR(self, a, b, c):
        """Changes color of the optionmenu to white or black, depending on it's value"""
        if self.__boxColorVar.get() ==  self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "light"):
            self.__colorOption.config(bg="white", fg="black", activebackground="white", activeforeground="black")
        else:
            self.__colorOption.config(bg="black", fg="lightgray", activebackground="black",
                                      activeforeground="lightgray")

    def __saveSettings(self):
        self.__saveSettingsToConfig()
        self.__Config.saveConfig()
        self.__setWindowLayout()
        if self.__haveToReSize==True:
            self.__setSizeAgain()

        self.__destroyWindow()


    def __saveSettingsToConfig(self):
        self.__haveToReSize=False

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

        temp=self.__Config.get_Element("StaticSize")
        if self.__windowSize.get()=="Auto":
            self.__Config.set_Element("StaticSize", "0")
        else:
            self.__Config.set_Element("StaticSize", self.__windowSize.get()[0])
        if temp!=self.__Config.get_Element("StaticSize"):
            self.__haveToReSize=True

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

        if self.__loadTemplate.get() == True:
            self.__Config.set_Element("loadTemplate", "True")
        else:
            self.__Config.set_Element("loadTemplate", "False")

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

        temp=self.__Config.get_Element("StaticSize")

        self.__Config.load_Config_Defaults()
        self.__Config.saveConfig()
        self.__setWindowLayout()
        if temp != self.__Config.get_Element("StaticSize"):
            self.__setSizeAgain()

    def __setSizeAgain(self):
        self.__master.createMainWindow()


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

        if self.__Config.get_Element("loadTemplate")=="True":
            self.__loadTemplate.set(True)
        else:
            self.__loadTemplate.set(False)

        self.__master.updateCodeBox()


    def __setOptionsMenuSize(self, w, h, size):
        self.__OptionsM.geometry("%dx%d+%d+%d" % (w, h, (size[0] / 2) - (w / 2), (size[1] / 2) - (h / 2) - 25))


    def __OptionsCompFrameLabel(self, event):
        """Writes the label of the main window to show info about the frame."""
        self.__master.create_StatLabel(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "compilerLabel"))


    def __OptionsBrowFrameLabel(self, event):
        """Writes the label of the main window to show info about the frame."""
        self.__master.create_StatLabel(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "browserLabel"))


    def __OptionsButFrameLabel(self, event):
        """Writes the label of the main window to show info about the frame."""
        self.__master.create_StatLabel(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "buttonLabel"))

    def __BasicSettingsFrameLabel(self, event):
        """Writes the label of the main window to show info about the frame."""
        self.__master.create_StatLabel(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "basicSettings"))

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

        if self.__Config.get_OS_Name()=="Windows":
            path = askopenfilename(initialdir=startdir,
                               title=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "open"),
                               filetypes=(
                                   (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "executable"),
                                    "*.exe"),))
        else:
            path = askopenfilename(initialdir=startdir,
                               title=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "open"),
                               filetypes=(
                                   (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "fileAll"),
                                    "*.*"),))

        if path == "" or path.endswith(".exe") == False:
            return (default_path)
        else:
            return (path)