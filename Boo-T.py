#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from abc import *
import os

from tkinter.filedialog import *
from tkinter import messagebox
from tkinterhtml import HtmlFrame
import multiprocessing
import time

from sys import path
path.insert(1, "scr/")

class MainWindow_Real(ABC):
    """Creating the Main Window, loads data for application."""

    def __init__(self):

        self.__main = Tk()
        self.__main.withdraw() #The Window is hidded while the
        self.__main.overrideredirect(True)
        self.__main.resizable(False, False)

        self.__opened = False
        self.__modified = False
        self.__saved = False
        self.__configChanged = False
        self.__path = ""

        import Dictionaries
        import Config
        import SyntaxList

        self.__dicts = Dictionaries.Dictionaries()
        self.__Config = Config.Config(self.__dicts)
        self.__Syntax = SyntaxList.SyntaxList()

        """Creates monitor object for getting the actual screensize, so the most
        suitable window sizes can be created.
        
        Here we create the Loading Screen that is only for show and presented for a short time.
        Setting 'noLoading' True will prevent this display."""
        import Monitor

        self.__monitor = Monitor.Monitor(self.__Config.get_OS_Name())
        if self.__Config.get_Element("noLoading")=="False":
            import DisplayLoading

            __loading_Screen = DisplayLoading.DisplayLoading(self.__monitor.get_screensize())

        from pyglet import font as PyFont
        PyFont.add_file('HammerFat.ttf')

        if self.__Config.get_OS_Name()=="Linux":
            """On Linux, you can only use fonts those are already installed in the system, so
            the appliaction checks if it is installed, then asks the user if he want to install it
             foe the better display. Also it tries to use three kind of linux font viewer
             to install the font manually."""

            from tkinter import font
            if "HammerFat_Hun" in font.families():

                ham=messagebox.askyesno("HammerFat_Hun", self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "linuxFontError"))
                if ham==True:
                    Done=self.__linuxTryToOpenFontViewer("font-manager")
                    if Done==False:
                        Done=self.__linuxTryToOpenFontViewer("gnome-font-viewer")
                    if Done==False:
                        Done=self.__linuxTryToOpenFontViewer("display")

                    if Done==False:
                        messagebox.showerror(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                          "noFontApp"),
                                             self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                          "linuxNoGnome").replace("#path#",
                                                                                                  '"' + os.getcwd() + '/HammerFat.ttf"'))

        self.__setFont(1)

        if self.__Config.get_Element("StaticSize") == "0":
            s = self.__GetWindowSize(self.__monitor.get_screensize())
        else:
            s = int(self.__Config.get_Element("StaticSize"))


        """This function will start builing up the main window."""
        self.__size_Num = self.__Create_Main_Window_By_Screen_Size(s, self.__monitor.get_screensize(),
                                                                   self.__Config.get_Element("Language"))


        self.updateCodeBox() #Needed for the correct text-size, reason unknown!

        "Bind function keys for hotkeys."
        self.__main.bind("<F1>", self.__F1)
        self.__main.bind("<F2>", self.__F2)
        self.__main.bind("<F3>", self.__F3)
        self.__main.bind("<F4>", self.__F4)
        self.__main.bind("<F5>", self.__F5)
        self.__main.bind("<F6>", self.__F6)
        self.__main.bind("<F7>", self.__F7)


        """
        self.__main.bind("<F8>", self.__F8)
        self.__main.bind("<F9>", self.__F9)
        self.__main.bind("<F10>", self.__F10)
        self.__main.bind("<F11>", self.__F11)
        self.__main.bind("<F12>", self.__F12)
        """

        "Makes the main window visible again."

        self.__main.bind("<Key>", self.code_Key_Pressed)
        self.__main.bind("<KeyRelease>", self.code_Key_Released)

        self.__main.deiconify()
        self.create_StatLabel(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "welcome"))
        self.__main.after(int(self.__Config.get_Element("AutoSave"))*60000, self.autoS)
        self.__main.mainloop()

    def __linuxTryToOpenFontViewer(self, app):
        """If the selected font viewer is present in Linux, open our font in it, allowing the user to install it."""

        if ((os.popen(str("whereis "+app)).read()).split(":")[1].replace("\n", "")) != "":
            #os.popen(app + ' "' + os.getcwd() + '/HammerFat.ttf"')
            import subprocess
            subprocess.run(app + ' "' + os.getcwd() + '/HammerFat.ttf"')

            return (True)
        else:
            return (False)


    def autoS(self):
        """Recursively calls itself and does autosave in the given period."""
        if int(self.__Config.get_Element("AutoSave"))>0:
            self.create_StatLabel(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "autoSaveDone"))
            self.saveQuickSave()
            self.__main.after(int(self.__Config.get_Element("AutoSave")) * 60000, self.autoS)
        else:
            self.__main.after(60000, self.autoS)

    def __setFont(self, num):
        """The font side is set based on the screensize you got at '__GetWindowSize' """
        self.__fontSize = 7 + (num * 2)
        self.__hammerFont = ("HammerFat_Hun", self.__fontSize)

    def __GetWindowSize(self, size):
        if size[0] > 1600:
            s = 4
        elif size[0] > 1280:
            s = 3
        elif size[0] > 800:
            s = 2
        else:
            s = 1
        return (s)

    def __Create_Main_Window_By_Screen_Size(self, s, size, lang):
        """Based on the screen size, the main window will be created and get it's attributes.
        Some of them are restored because at the beginning, the window gets a 1x1 size at startup."""

        if s == 1:
            self.__create_Main_Window_by_size(size, s, 640, 420, 480)
        elif s == 2:
            self.__create_Main_Window_by_size(size, s, 800, 580, 632)
        elif s == 3:
            self.__create_Main_Window_by_size(size, s, 800, 1100, 632)
        else:
            self.__create_Main_Window_by_size(size, s, 800, 1400, 632)

        self.__main.title("Boo-T")
        self.__main.overrideredirect(False)
        try:
            self.__main.iconbitmap("icons/Boots.ico")
        except:
            """Linux cannot handle ico-s"""
            from tkinter import PhotoImage
            self.__main.iconphoto(True, PhotoImage("icons/Boots.png"))

        self.__create_Menu(lang, s)

        return (s)

    def __create_Menu(self, lang, size):
        """Loads the icons amd creates the 32y32 buttons one by one. If the mouse enters
        an icon, it will display it's puprose. These are static on every window size!"""
        from PIL import ImageTk, Image

        self.__buttonSize = 40
        self.__setFont(size)

        self.__imgNew = ImageTk.PhotoImage(Image.open("icons/new.png"))
        self.__new_B = self.__createButton(self.__imgNew, self.__doNew, self.__on_enterNewB, 0)

        self.__imgOpen = ImageTk.PhotoImage(Image.open("icons/open.png"))
        self.__open_B = self.__createButton(self.__imgOpen, self.__doOpen, self.__on_enterOpenB, 1)

        self.__imgSave = ImageTk.PhotoImage(Image.open("icons/save.png"))
        self.__save_B = self.__createButton(self.__imgSave, self.__doSave, self.__on_enterSaveB, 2)

        self.__imgSaveAs = ImageTk.PhotoImage(Image.open("icons/save_as.png"))
        self.__saveAs_B = self.__createButton(self.__imgSaveAs, self.__doSaveAs, self.__on_enterSaveAsB, 3)

        self.__imgCopy = ImageTk.PhotoImage(Image.open("icons/copy.png"))
        self.__Copy_B = self.__createButton(self.__imgCopy, self.__doCopy, self.__on_enterCopy, 4.25)

        self.__imgPaste = ImageTk.PhotoImage(Image.open("icons/paste.png"))
        self.__Paste_B = self.__createButton(self.__imgPaste, self.__doPaste, self.__on_enterPaste, 5.25)

        self.__imgHTML = ImageTk.PhotoImage(Image.open("icons/html.png"))
        self.__HTML_B = self.__createButton(self.__imgHTML, self.__getCodeOnly, self.__on_enterHTML, 6.5)

        self.__imgFastTest = ImageTk.PhotoImage(Image.open("icons/test.png"))
        self.__FTest_B = self.__createButton(self.__imgFastTest, None, self.__on_enterFastTest, 7.5)

        self.__imgFFox = ImageTk.PhotoImage(Image.open("icons/firefox.png"))
        self.__FFox_B = self.__createButton(self.__imgFFox, None, self.__on_enterFFox, 8.5)

        self.__imgChrome = ImageTk.PhotoImage(Image.open("icons/chrome.png"))
        self.__Chrome_B = self.__createButton(self.__imgChrome, None, self.__on_enterChrome, 9.5)

        self.__imgEdge = ImageTk.PhotoImage(Image.open("icons/edge.png"))
        self.__Edge_B = self.__createButton(self.__imgEdge, None, self.__on_enterEdge, 10.5)

        self.__imgOpera = ImageTk.PhotoImage(Image.open("icons/opera.png"))
        self.__Opera_B = self.__createButton(self.__imgOpera, None, self.__on_enterOpera, 11.5)

        self.__imgSettings = ImageTk.PhotoImage(Image.open("icons/settings.png"))
        self.__Settings_B = self.__createButton(self.__imgSettings, self.__OptionsMenu, self.__on_enterSettings, 12.75)

        self.__imgHelp = ImageTk.PhotoImage(Image.open("icons/help.png"))
        self.__Help_B = self.__createButton(self.__imgHelp, None, self.__on_enterHelp, 13.75)

        self.__imgAbout = ImageTk.PhotoImage(Image.open("icons/about.png"))
        self.__About_B = self.__createButton(self.__imgAbout, self.__AboutMenu, self.__on_enterAbout, 14.75)

        self.CheckIfValid()

        self.__Hint = StringVar()
        self.__HintText = Label(self.__main, textvariable=self.__Hint, font=self.__hammerFont)

    def __createButton(self, image, command, on_Enter, buttonpoz):
        """Generates Button from given data. Image, cannad and enter-message generation is unique."""

        button = Button(self.__main, image=image, width=32, height=32, command=command)
        button.place(x=self.__getButtonPoz(buttonpoz), y=1)
        button.bind("<Enter>", on_Enter)
        button.bind("<Leave>", self.__on_leave)
        return(button)

    def __doNew(self):
        """if box was modified, asks if you want to save your file, amd deletes the box."""
        if self.__modified == True:
            self.__askForSave()

        self.__deleteBox()
        self.__opened = False
        self.__path = ""

        if os.path.exists("templates/new_file.txt") and self.__Config.get_Element("loadTemplate")=="True":
            self.__openFile("templates/new_file.txt", False)


    def __doOpen(self):
        """If box was modified, asks for save, then asks for a .boo, .txt or any file that it tries to load. If it fails,
        it shows you an erre message and prints the exception."""

        if self.__modified == True:
            self.__askForSave()
        openname = askopenfilename(initialdir="*",
                                   title=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "open"),
                                   filetypes=(
                                       (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "fileBoot"),
                                        "*.boo"),
                                       (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "fileTxT"),
                                        "*.txt"),
                                       (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "fileAll"),
                                        "*.*"),
                                   ))
        try:
            self.__openFile(openname,True)
        except Exception as e:
            messagebox.showerror(
                self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "fileOpenErrorTitle"),
                self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "fileOpenError").replace("#path#",
                                                                                                             openname) + "\n" + str(e))

    def __openFile(self, openname, addRecent):
        if "new_file" in openname:
            addRecent = False
            self.__opened = False

        else:
            self.__opened = True

        opened = open(openname, "r")
        self.__insertBox(opened.read())
        self.updateCodeBox()

        opened.close()
        if addRecent==True:
            self.__addToRecent(openname)
        self.__path = openname

    def __askForSave(self):
        """Asks if you want to save the file."""
        M = messagebox.askyesno(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "Unsaved"),
                                self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "DoYouSave"))

        if M == True:
            self.__doSave()

    def __deleteBox(self):
        self.__CodeBox.delete(0.0, END)

    def __insertBox(self, text):
        self.__deleteBox()
        self.__CodeBox.insert(0.0, text)

    def __doSave(self):
        """Calls saver directly, if a file is already opened."""
        if self.__opened == True:
            savename = self.__path
            self.__Saver(savename)
        else:
            self.__doSaveAs()

    def __doSaveAs(self):
        savename = asksaveasfilename(initialdir="*",
                                     title=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "save"),
                                     filetypes=((self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                              "fileBoot"), "*.boo"),
                                                (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                              "fileTxT"), "*.txt")))

        self.__Saver(savename)

    def __Saver(self, savename):


        try:

            if savename!="" and ("new_file" not in savename):
                if savename.endswith(".boo") == False or savename.endswith(".txt"):
                    savename += ".boo"
                opened = open(savename, "w")
                opened.write(self.__getCodeFromBox())
                opened.close()
                #self.saveQuickSave()
                self.__addToRecent(savename)
                self.__opened = True
                self.__path = savename
                self.__deleteQuick()



        except Exception as e:
            messagebox.showerror(
                self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "fileSaveErrorTitle"),
                self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "fileSaveError").replace("#path#",
                    savename) + "\n" + str(e))

    def __doPaste(self):
        import clipboard

        self.__CodeBox.insert(INSERT, clipboard.paste())

    def __doCopy(self):
        import clipboard

        clipboard.copy(self.__CodeBox.selection_get())


    def __addToRecent(self, text):
        """Saves the recent opened file list, also updates the listbox.
        If maximum number of recent is exceeded, it will delete the last element before update."""

        file = open("default/Recent.txt", "w")
        if text in self.__recentFiles:
            self.__recentFiles.remove(text)
            self.__recentList.delete(self.__recentList.get(0, END).index(text.split("/")[-1]))

        if len(self.__recentFiles) == int(self.__Config.get_Element("MaxRecent")) and self.__Config.get_Element("MaxRecent") != "0":
            self.__recentFiles.pop()
            self.__recentList.delete(END)

        self.__recentFiles.insert(0, text)
        for num in range(0, len(self.__recentFiles)):
            file.write(self.__recentFiles[num].split("/")[-1] + "=" + self.__recentFiles[num] + "\n")

        file.close()
        self.__recentList.insert(0, text.split("/")[-1])

    def __getButtonPoz(self, num):
        """Returns X position for the menu button"""
        return (4 + (self.__buttonSize) * num)

    def CheckIfValid(self):
        """Disables test in browser buttons if browser path is not enabled."""
        if self.__Config.get_Element("Chrome") == "":
            self.__Chrome_B.config(state=DISABLED)
        else:
            self.__Chrome_B.config(state=NORMAL)

        if self.__Config.get_Element("FireFox") == "":
            self.__FFox_B.config(state=DISABLED)
        else:
            self.__FFox_B.config(state=NORMAL)
        if self.__Config.get_Element("Edge") == "":
            self.__Edge_B.config(state=DISABLED)
        else:
            self.__Edge_B.config(state=NORMAL)
        if self.__Config.get_Element("Opera") == "":
            self.__Opera_B.config(state=DISABLED)
        else:
            self.__Opera_B.config(state=NORMAL)

    def __create_Main_Window_by_size(self, __size, s, __windowW, __windowH, boxW):
        """Contains calls for creating the main window size, the container for the textbox and the listboxes."""
        self.__setMainGeo(__windowW, __windowH, __size)
        self.__createCodeBox(self.__hammerFont, boxW, __windowH - ((self.__fontSize) * 5) - 55)
        self.__create_Listboxes(__windowW, __windowH, s, boxW)

    def __setMainGeo(self, w, h, size):
        """Sets the size of the main window."""
        self.__main.geometry("%dx%d+%d+%d" % (w, h, (size[0] / 2) - (w / 2), (size[1] / 2) - (h / 2) - 25))


    def __createCodeBox(self, baseFont, w, h):
        import tkinter.scrolledtext as tkscrolled

        """Creates the elements for the main input field."""
        self.__Frame_for_CodeBox = Frame(self.__main, width=w, height=h)
        self.__Frame_for_CodeBox.place(x=2, y=baseFont[1] + 58)
        self.__Frame_for_CodeBox.pack_propagate(False)

        self.__CodeBox = tkscrolled.ScrolledText(self.__Frame_for_CodeBox, width=1, height=1, font=baseFont)
        self.__box_Ctrl_Pressed = False
        self.__CodeBox.bind("<MouseWheel>", self.mouse_Wheel)


        self.__loadQuickSave()
        self.updateCodeBox()

    def code_Key_Pressed(self, event):
        """Neded for the usual ctrl + mousewheel combnation for resizing textbox font."""
        self.__modified = True
        if (event.keysym == "Control_L" or event.keysym == "Control_R"):
            self.__box_Ctrl_Pressed = True


    def code_Key_Released(self, event):
        """Neded for the usual ctrl + mousewheel combnation for resizing textbox font."""
        self.__highLighter()

        if (event.keysym == "Control_L" or event.keysym == "Control_R"):
            self.__box_Ctrl_Pressed = False

    def mouse_Wheel(self, event):
        """If ctrl is pressed and the user roll the mouse's wheel, the font size will be changed.
        Need to call updateCodeBox for the actual change."""
        if self.__box_Ctrl_Pressed:
            if (event.delta > 0 and int(self.__Config.get_Element("BoxFontSize")) < 48):
                self.__Config.set_Element("BoxFontSize", str(int(self.__Config.get_Element("BoxFontSize")) + 1))
                self.updateCodeBox()

            if (event.delta < 0 and int(self.__Config.get_Element("BoxFontSize")) > 12):
                self.__Config.set_Element("BoxFontSize", str(int(self.__Config.get_Element("BoxFontSize")) - 1))
                self.updateCodeBox()

    def __getHammerFont(self):
        """Sets font for the code box section"""

        from tkinter.font import Font, families

        hammerFont = Font(font='HammerFat_Hun')
        if int(self.__Config.get_Element("BoxFontSize")) == 0:
            hammerFont.config(size=self.__fontSize+4)
        else:
            hammerFont.config(size=int(self.__Config.get_Element("BoxFontSize")))


        return (hammerFont)

    @abstractmethod
    def updateCodeBox(self):
        """Changes the light/dark them for the box, also changes the font size.
        If the listbox are existing, updates their colors too."""

        if int(self.__Config.get_Element("BoxFontSize")) > 48:
            self.__Config.set_Element("BoxFontSize", "48")
        if int(self.__Config.get_Element("BoxFontSize")) < 12:
            self.__Config.set_Element("BoxFontSize", "12")

        if (self.__Config.get_Element("DarkBox") == "False"):
            self.__color = "white"
            self.__color2 = "black"
        else:
            self.__color = "black"
            self.__color2 = "lightgray"
        hammerFont = self.__getHammerFont()


        self.__CodeBox.config(bg=self.__color, fg=self.__color2,
                              width=68,
                              height=50,
                              wrap=CHAR)

        self.__CodeBox.config(font=hammerFont)
        try:
            self.__recentList.config(bg=self.__color, fg=self.__color2)
            self.__syntaxList.config(bg=self.__color)

            if (self.__Config.get_Element("DarkBox") == "False"):

                self.__syntaxList.config(fg="blue")
                for num in range(0, self.__syntaxList.size()-1):
                    if self.__SYN[num] in self.__Syntax.getKeys():
                        self.__syntaxList.itemconfig(num, {"fg": "green"})


            else:
                self.__syntaxList.config(fg="light sky blue")

                for num in range(0, self.__syntaxList.size()-1):
                    if self.__SYN[num] in self.__Syntax.getKeys():
                        self.__syntaxList.itemconfig(num, {"fg": "lime"})

            self.__highLighter()
        except Exception as e:
            pass

        self.__CodeBox.pack()

    def __on_leave(self, event):
        self.__Hint.set("")

    def __setHintTextLocation(self, num):
        """Places the tint text of file men to the right place"""
        self.__HintText.place(x=4 + (self.__buttonSize) * num, y=self.__buttonSize)

    """Hints X locations are set manually because of tkinter's strict event handling."""

    def __on_enterNewB(self, event):
        self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "new"))
        self.__setHintTextLocation(0)

    def __on_enterOpenB(self, event):
        self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "open"))
        self.__setHintTextLocation(0)

    def __on_enterSaveB(self, event):
        self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "save"))
        self.__setHintTextLocation(0)

    def __on_enterSaveAsB(self, event):
        self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "save_as"))
        self.__setHintTextLocation(0)

    def __on_enterCopy(self, event):
        self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "copy"))
        self.__setHintTextLocation(4.25)

    def __on_enterPaste(self, event):
        self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "paste"))
        self.__setHintTextLocation(4.25)

    def __on_enterHTML(self, event):
        self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "HTMLCode"))
        self.__setHintTextLocation(6.5)

    def __on_enterFastTest(self, event):
        self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "fastTest"))
        self.__setHintTextLocation(6.5)

    def __on_enterFFox(self, event):
        if self.__Config.get_Element("FireFox") == "":
            self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "browserNotSet").replace("#browser#", "Firefox"))
        else:
            self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "FFoxTest"))
        self.__setHintTextLocation(6.5)

    def __on_enterChrome(self, event):
        if self.__Config.get_Element("Chrome") == "":
            self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "browserNotSet").replace("#browser#", "Chrome"))
        else:
            self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "ChromeTest"))
        self.__setHintTextLocation(6.5)

    def __on_enterEdge(self, event):
        if self.__Config.get_Element("Edge") == "":
            self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "browserNotSet").replace("#browser#", "Edge"))
        else:
            self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "EdgeTest"))
        self.__setHintTextLocation(6.5)

    def __on_enterOpera(self, event):
        if self.__Config.get_Element("Opera") == "":
            self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "browserNotSet").replace("#browser#", "Opera"))
        else:
            self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "OperaTest"))
        self.__setHintTextLocation(6.5)

    def __on_enterSettings(self, event):
        self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "settings"))
        self.__setHintTextLocation(12.75)

    def __on_enterHelp(self, event):
        self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "help"))
        self.__setHintTextLocation(12.75)

    def __on_enterAbout(self, event):
        self.__Hint.set(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "about"))
        self.__setHintTextLocation(12.75)

    @abstractmethod
    def create_StatLabel(self, text):
        "Because other objects can display message on the main window, the method has an abstract call."
        try:
            self.__destroy_StatLabel()
        except:
            pass
        self.__StatLabel = Label(self.__main, text=text, font=self.__hammerFont)
        self.__StatLabel.place(x=3, y=self.__main.winfo_height() - self.__fontSize * 2.25)
        self.__StatLabel.after(len(text) * 50 + 1000, self.__destroy_StatLabel)

    def __destroy_StatLabel(self):
        self.__StatLabel.destroy()

    def __create_Listboxes(self, __windowW, __windowH, __size, __boxW):
        """Creates the recent files listbox, also the one containing the syntax used for coding.
        Elements based on characters while calculating width and height are strictly placed into
        frames those are calculated in pixels."""
        self.__setFont(__size)

        if __size > 1:
            __relativeX = 640
            __relativeY = -2
        else:
            __relativeX = 490
            __relativeY = 52 + self.__hammerFont[1]

        __recentLabel = Label(self.__main,
                              text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "recent"))
        __recentLabel.config(font=self.__hammerFont)
        __recentLabel.place(x=__relativeX, y=__relativeY)

        __firstListHeight = round(__windowH / 3 - __relativeY - self.__hammerFont[1] * 2)
        self.__recentList_Frame = Frame(self.__main, width=__windowW - __relativeX - 3 - 17, height=__firstListHeight)
        self.__recentList_Frame.place(x=__relativeX, y=(__relativeY + self.__hammerFont[1] * 2))
        self.__recentList_Frame.pack_propagate(False)

        self.__recentListScroller_Frame = Frame(self.__main, width=15, height=__firstListHeight)
        self.__recentListScroller_Frame.place(x=__windowW - 19, y=(__relativeY + self.__hammerFont[1] * 2))
        self.__recentListScroller_Frame.pack_propagate(False)
        self.__recentListScroller = Scrollbar(self.__recentListScroller_Frame)

        self.__recentList = Listbox(self.__recentList_Frame, width=1000, height=1000,
                                    yscrollcommand=self.__recentListScroller.set, selectmode=BROWSE,
                                    bg=self.__color, fg=self.__color2)

        self.__recentList.bind("<<ListboxSelect>>", self.__printPath)
        self.__recentList.config(font=self.__hammerFont)
        self.__recentList.pack()

        self.__recentListScroller.pack(side=RIGHT, fill=Y)
        self.__recentListScroller.config(command=self.__recentList.yview)

        self.__recentButton_Frame = Frame(self.__main, width=__windowW - __relativeX - 4, height=25)
        self.__recentButton_Frame.place(x=__relativeX + 1,
                                        y=(__relativeY + self.__hammerFont[1] * 2) + __firstListHeight + 5)
        self.__recentButton_Frame.pack_propagate(False)

        self.__loadFromRecentButton = Button(self.__recentButton_Frame, width=1000,
                                             text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                               "open"),font=self.__hammerFont, command=self.__openRecentFile)
        self.__loadFromRecentButton.pack()
        self.loadRecent()

        __secondListY = (__relativeY + self.__hammerFont[1] * 2) + __firstListHeight + 51 + self.__hammerFont[1] * 2

        __loadImageFrame = Frame(self.__main, width=__windowW - __relativeX - 5, height=40)
        __loadImageFrame.place(x=__relativeX, y=__secondListY-40)
        __loadImageFrame.pack_propagate(False)
        __loadImageFrame.bind("<Enter>", self.__imgPrintOutLabel)

        from PIL import ImageTk, Image
        self.__imgImg = ImageTk.PhotoImage(Image.open("icons/Image.png"))
        self.__imgLabel = Label(__loadImageFrame, image=self.__imgImg)
        self.__imgLabel.pack(side=LEFT)

        self.__imgButton = Button(__loadImageFrame, width=1000, command=self.__loadImagePath,
                                             text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                               "imgImport"),font=self.__hammerFont)
        self.__imgButton.pack(side=RIGHT)


        __syntaxLabel = Label(self.__main,
                              text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "syntax"))
        __syntaxLabel.config(font=self.__hammerFont)
        __syntaxLabel.place(x=__relativeX, y=(__relativeY + self.__hammerFont[1] * 2) + __firstListHeight + 75)

        __secondListHeight = round(__windowH / 3 * 1.4 - __relativeY - self.__hammerFont[1] * 2)
        self.__syntaxList_Frame = Frame(self.__main, width=__windowW - __relativeX - 3 - 17, height=__secondListHeight)

        self.__syntaxList_Frame.place(x=__relativeX, y=__secondListY+25)
        self.__syntaxList_Frame.pack_propagate(False)

        self.__syntaxListScroller_Frame = Frame(self.__main, width=15, height=__secondListHeight)
        self.__syntaxListScroller_Frame.place(x=__windowW - 19, y=__secondListY+20)
        self.__syntaxListScroller_Frame.pack_propagate(False)
        self.__syntaxListScroller = Scrollbar(self.__syntaxListScroller_Frame)

        self.__syntaxList = Listbox(self.__syntaxList_Frame, width=1000, height=1000,
                                    yscrollcommand=self.__syntaxListScroller.set, selectmode=BROWSE,
                                    bg=self.__color, fg=self.__color2)
        self.__syntaxList.config(font=self.__hammerFont)
        self.__syntaxList.pack()

        self.__syntaxListScroller.pack(side=RIGHT, fill=Y)
        self.__syntaxListScroller.config(command=self.__syntaxList.yview)

        self.__syntaxButton_Frame = Frame(self.__main, width=__windowW - __relativeX - 4, height=25)
        self.__syntaxButton_Frame.place(x=__relativeX + 1, y=__secondListY + 35 + __secondListHeight)
        self.__syntaxButton_Frame.pack_propagate(False)

        self.__loadFromsyntaxButton = Button(self.__syntaxButton_Frame, width=1000,
                                             text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                               "paste"), font=self.__hammerFont,
                                                                                command=self.__insertSyntax)
        self.__loadFromsyntaxButton.pack()
        self.__fillSyntaxList()

    def __loadImagePath(self):
        path = askopenfilename(initialdir="*", title=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),"openImage"),
                               filetypes=[
                                   (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),"imgFiles"), "*.png"),
                                   (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),"imgFiles"), "*.jpg"),
                                   (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),"imgFiles"), "*.gif"),
                                   (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),"imgFiles"), "*.jpeg"),
                                   (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),"imgFiles"), "*.bmp"),
                                   (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "imgFiles"),
                                    "*.tiff"),
                                   (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "imgFiles"),
                                    "*.apng"),
                                   (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "imgFiles"),
                                    "*.svg"),
                                   (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "imgFiles"),
                                    "*.avif"),
                                   (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "imgFiles"),
                                    "*.webp"),
                                   (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "imgFiles"),
                                    "*.ico"),
                                   (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),"fileAll"), "*.*"),
                               ])
        if path!="":
            self.__CodeBox.insert(INSERT, path)


    def loadRecent(self):
        """List of recently saved and opened files.
        If max number of recent files is exceeded, it won't load more."""
        if os.path.exists("default/Recent.txt"):
            file = open("default/Recent.txt", "r")
            self.__recentFiles = []
            self.__recentList.delete(0, END)
            for item in file.readlines():
                try:
                    if len(self.__recentFiles) < int(self.__Config.get_Element("MaxRecent")) or int(
                            self.__Config.get_Element("MaxRecent")) == 0:
                        self.__recentList.insert(END, item.replace("\n", "").replace("\r", "").split("=")[0])
                        self.__recentFiles.append(item.replace("\n", "").replace("\r", "").split("=")[1])

                except:
                    pass
        else:
            file = open("default/Recent.txt", "w")
        file.close()

    def __printPath(self, event):
        """Uses the hint label to print out selected file's path"""
        try:
            self.create_StatLabel(self.__recentFiles[self.__recentList.curselection()[0]])
        except:
            self.create_StatLabel(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "recentList"))

    def __OptionsMenu(self):
        import OptionsM

        OptionsM=OptionsM.OptionsMenu(self.__dicts, self.__Config, self.__hammerFont,
                             self.__imgChrome, self.__imgFFox, self.__imgEdge, self.__imgOpera, self, self.__main, self.__fontSize, self.__monitor)

    def __AboutMenu(self):
        """Opens the men abouth the program and the author."""
        import About

        AboutM=About.AboutMenu(self.__dicts, self.__Config, self.__hammerFont, self, self.__main, self.__fontSize, self.__monitor)


    def __getCodeOnly(self):
        import GetCodeOnly

        GetCodeOnly = GetCodeOnly.GetCodeOnly(self.__dicts, self.__Config, self.__hammerFont, self, self.__main, self.__fontSize, self.__monitor, self.__getCodeFromBox(), self.__Syntax)

    def __getCodeFromBox(self):
        return(self.__CodeBox.get(0.0, END))

    def __deleteQuick(self):
        if os.path.exists("QuickSave.txt"):
            os.remove("QuickSave.txt")

    def __loadQuickSave(self):
        """Loads quicksave file if present."""
        if os.path.exists("QuickSave.txt"):
            file=open("QuickSave.txt", "r")
            self.__insertBox(file.read())
            file.close()

    @abstractmethod
    def saveQuickSave(self):
        file = open("QuickSave.txt", "w", encoding='utf8')
        file.write(self.__getCodeFromBox())
        file.close()


    def __imgPrintOutLabel(self, event):
        self.create_StatLabel(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "imgLabel"))

    def __openRecentFile(self):
        try:
            self.__openFile(self.__recentFiles[self.__recentList.curselection()[0]], False)
        except:
            pass

    def __insertSyntax(self):
        try:
            self.__CodeBox.insert(INSERT, self.__SYN[self.__syntaxList.curselection()[0]])
        except:
            pass


    def __fillSyntaxList(self):
        the_list = []
        for item in self.__Syntax.getKeys():
            the_list.append(item)
            templist = self.__Syntax.getValueOfKey(item)
            for subItem in templist:
                the_list.append(subItem)
        the_list = list(set(the_list))
        the_list.sort()
        self.__SYN = []
        for i in range(1, len(the_list)):
            self.__SYN.append(the_list[i])
            self.__syntaxList.insert(END, the_list[i])

    def __highLighter(self):
        for tag in self.__CodeBox.tag_names():
            self.__CodeBox.tag_delete(tag)

        self.__standard_tinting("subArg", self.__SYN)

        if (self.__Config.get_Element("DarkBox") == "False"):
            self.__CodeBox.tag_config("Arg", foreground="green", font=("HammerFat_Hun", self.__Config.get_Element("BoxFontSize"), "bold", "underline"))
            self.__CodeBox.tag_config("subArg", foreground="blue", font=("HammerFat_Hun", self.__Config.get_Element("BoxFontSize"), "bold"))
            self.__CodeBox.tag_config("string", foreground="red", background="yellow", font=("HammerFat_Hun", self.__Config.get_Element("BoxFontSize")))
            self.__CodeBox.tag_config("comment", background="white", foreground="plum4", font=("HammerFat_Hun", self.__Config.get_Element("BoxFontSize"), "italic",))
            self.__CodeBox.config(insertbackground="black")

        else:
            self.__CodeBox.tag_config("Arg", foreground="lime", font=("HammerFat_Hun", self.__Config.get_Element("BoxFontSize"), "bold", "underline"))
            self.__CodeBox.tag_config("subArg", foreground="light sky blue", font=("HammerFat_Hun", self.__Config.get_Element("BoxFontSize"), "bold"))
            self.__CodeBox.tag_config("string", foreground="yellow", background="red", font=("HammerFat_Hun", self.__Config.get_Element("BoxFontSize")))
            self.__CodeBox.tag_config("comment", background="black", foreground="plum1", font=("HammerFat_Hun", self.__Config.get_Element("BoxFontSize"), "italic",))
            self.__CodeBox.config(insertbackground="lightgray")

        self.__standard_tinting("Arg", self.__Syntax.getKeys())
        self.__between_tinting("string", "'")
        self.__between_tinting("string", '"')
        self.__comment_tinting()


    def __standard_tinting(self, tag, refList):
        lines=self.__CodeBox.get("1.0", END).splitlines()
        for linenum in range(0, len(lines)):
            x = 0
            temp=""
            for charnum in range(0, len(lines[linenum])):
                if lines[linenum][charnum].isalpha()==False and lines[linenum][charnum]!="-":
                    if temp in refList:
                        self.__CodeBox.tag_add(tag, str(linenum+1) + "." + str(x), str(linenum+1)+"."+str(charnum))
                    x=charnum+1
                    temp=""
                else:
                    temp+=lines[linenum][charnum]
            if temp in refList:
                self.__CodeBox.tag_add(tag, str(linenum + 1) + "." + str(x), str(linenum + 1) + "." + str(len(lines[linenum])))

    def __between_tinting(self, tag, char):
        lines=self.__CodeBox.get("1.0", END).splitlines()
        for linenum in range(0, len(lines)):
            x = 0
            on = False
            for charnum in range(0, len(lines[linenum])):
                if lines[linenum][charnum] == char:
                    if on == False:
                        on = True
                        x = charnum
                    else:
                        on = False
                        self.__CodeBox.tag_add(tag, str(linenum + 1) + "." + str(x+1),
                                               str(linenum + 1) + "." + str(charnum))

    def __comment_tinting(self):
        lines=self.__CodeBox.get("1.0", END).splitlines()
        if len(lines)>1:
            for linenum in range(0, len(lines)):
                for charnum in range(0, len(lines[linenum])-1):
                    if lines[linenum][charnum] == "%" and lines[linenum][charnum+1] == "%":

                        self.__CodeBox.tag_add("comment", str(linenum + 1) + "." + str(charnum),
                                                   str(linenum + 1) + "." + str(len(lines[linenum])))
                        break

    def __lightDark(self):
        if self.__Config.get_Element("DarkBox") == "True":
            self.__Config.set_Element("DarkBox", "False")
        else:
            self.__Config.set_Element("DarkBox", "True")
        self.updateCodeBox()

    def __F1(self, event):
        self.__doNew()

    def __F2(self, event):
        self.__doOpen()

    def __F3(self, event):
        self.__doSave()

    def __F4(self, event):
        self.__getCodeOnly()

    def __F5(self, event):
        self.__loadImagePath()

    def __F6(self, event):
        self.__OptionsMenu()

    def __F7(self, event):
        self.__lightDark()

class MainWindow(MainWindow_Real):
    def __init__(self):
        super().__init__()

    def create_StatLabel(master, text):
        super().create_StatLabel(text)

    def updateCodeBox(master):
        super().updateCodeBox()

    def saveQuickSave(master):
        super().saveQuickSave()


if __name__ == "__main__":
    MainWindow()
    if os.path.exists("Quicksave.txt"):
        os.remove("Quicksave.txt")

