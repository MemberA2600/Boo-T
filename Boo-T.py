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

        self.__dicts = Dictionaries.Dictionaries()
        self.__Config = Config.Config(self.__dicts)

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

        "Makes the main window visible again."
        self.__main.deiconify()
        self.create_StatLabel("Welcome!")
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
            self.__create_Main_Window_by_size(size, s, 800, 688, 632)
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
        self.__HTML_B = self.__createButton(self.__imgHTML, None, self.__on_enterHTML, 6.5)

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

        if os.path.exists("default/new_file.txt") and self.__Config.get_Element("loadTemplate")=="True":
            self.__openFile("default/new_file.txt", False)


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
        opened = open(openname, "r")
        self.__insertBox(opened.read())
        opened.close()
        if addRecent==True:
            self.__addToRecent(openname)
        self.__opened = True
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
            if savename.endswith(".boo") == False or savename.endswith(".txt"):
                savename += ".boo"
            opened = open(savename, "w")
            opened.write(self.__getCodeFromBox())
            opened.close()
            self.saveQuickSave()
            self.__addToRecent(savename)
            self.__opened = True
            self.__path = savename

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

        if len(self.__recentFiles) == int(self.__Config.get_Element("MaxRecent")) and int(
                self.__Config.get_Element("MaxRecent")) != 0:
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
        self.Frame_for_CodeBox = Frame(self.__main, width=w, height=h)
        self.Frame_for_CodeBox.place(x=2, y=baseFont[1] + 58)
        self.Frame_for_CodeBox.pack_propagate(False)

        self.__CodeBox = tkscrolled.ScrolledText(self.Frame_for_CodeBox, width=1, height=1, font=baseFont)
        self.__box_Ctrl_Pressed = False
        self.__CodeBox.bind("<Key>", self.code_Key_Pressed)
        self.__CodeBox.bind("<KeyRelease>", self.code_Key_Released)
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
                              wrap=WORD)

        self.__CodeBox.config(font=hammerFont)
        try:
            self.__recentList.config(bg=self.__color, fg=self.__color2)
            self.__syntaxList.config(bg=self.__color, fg=self.__color2)
        except:
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
                                                                               "open"),font=self.__hammerFont)
        self.__loadFromRecentButton.pack()
        self.loadRecent()

        __syntaxLabel = Label(self.__main,
                              text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "syntax"))
        __syntaxLabel.config(font=self.__hammerFont)
        __syntaxLabel.place(x=__relativeX, y=(__relativeY + self.__hammerFont[1] * 2) + __firstListHeight + 31)

        __secondListHeight = round(__windowH / 3 * 1.6 - __relativeY - self.__hammerFont[1] * 2)
        self.__syntaxList_Frame = Frame(self.__main, width=__windowW - __relativeX - 3 - 17, height=__secondListHeight)

        __secondListY = (__relativeY + self.__hammerFont[1] * 2) + __firstListHeight + 31 + self.__hammerFont[1] * 2
        self.__syntaxList_Frame.place(x=__relativeX, y=__secondListY)
        self.__syntaxList_Frame.pack_propagate(False)

        self.__syntaxListScroller_Frame = Frame(self.__main, width=15, height=__secondListHeight)
        self.__syntaxListScroller_Frame.place(x=__windowW - 19, y=__secondListY)
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
        self.__syntaxButton_Frame.place(x=__relativeX + 1, y=__secondListY + 5 + __secondListHeight)
        self.__syntaxButton_Frame.pack_propagate(False)

        self.__loadFromsyntaxButton = Button(self.__syntaxButton_Frame, width=1000,
                                             text=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                               "paste"), font=self.__hammerFont)
        self.__loadFromsyntaxButton.pack()


    def loadRecent(self):
        """List of recently saved and opened files.
        If max number of recent files is exceeded, it won't load more."""
        if os.path.exists("default/Recent.txt"):
            file = open("default/Recent.txt", "r")
            self.__recentFiles = []
            self.__recentList.delete(0, END)
            for item in file.readlines():
                try:
                    if len(self.__recentFiles) < int(self.__Config.get_Element("MaxRecent")) and int(
                            self.__Config.get_Element("MaxRecent")) != 0:
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

    def __getCodeFromBox(self):
        return(self.__CodeBox.get(0.0, END))

    def __loadQuickSave(self):
        """Loads quicksave file if present."""
        if os.path.exists("QuickSave.txt"):
            file=open("QuickSave.txt", "r")
            self.__insertBox(file.read())
            file.close()
            os.remove("QuickSave.txt")

    @abstractmethod
    def saveQuickSave(self):
        file = open("QuickSave.txt", "w")
        file.write(self.__getCodeFromBox())
        file.close()

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
