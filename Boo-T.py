from tkinter import *
from abc import *
import os
import re
from tkinter.filedialog import *
from tkinter import messagebox
import tkinter.scrolledtext as tkscrolled
from tkinterhtml import HtmlFrame
import multiprocessing


class Dictionaries_REAL(ABC):
    """Cointains text the application will display, loaded from '/dicts'."""
    @abstractmethod
    def __init__(self):
        self.__D = {}
        for root, dirs, files in os.walk("dicts/"):
            for file in files:
                self.__LoadDict(root+file, file.replace(".txt",""))

    def __LoadDict(self, path, name):
        f = open(path, "r")
        lines = f.readlines()
        f.close()
        self.__D[name]={}

        for line in lines:
            self.__D[name][line.split("=")[0]] = line.split("=")[1]

    @abstractmethod
    def getWordFromDict(self, lang, word):
        return(self.__D[lang][word])

class Dictionaries(Dictionaries_REAL):
    def __init__(self):
        super().__init__()

    def getWordFromDict(self, lang, word):
        return(super().getWordFromDict(lang,word))

class Config_Real(ABC):
    """This is the real class, hidden from direct accessing.
    The configuration file and the dictionary containing the
    settings can be accessed with it."""

    @abstractmethod
    def __init__(self, dicts):
        self.__dicts=dicts
        self.__Config=self.__Load_Config_File()
        if self.__Config["AutoCheckForInstalledBrowsers"]=="True":
            self.__CheckBrowsers(self.__Config["Chrome"],
                                 self.__Config["FireFox"],
                                 self.__Config["Edge"],
                                 self.__Config["Opera"])

    @abstractmethod
    def set_Element(self, key, value):
        self.__Config[key]=value

    @abstractmethod
    def get_Element(self, key):
        return(self.__Config[key])

    def __Load_Config_File(self):
        """Will load the config file located in the root folder."""
        __temp={}
        config_file=open("Config.txt", "r")
        text=config_file.readlines()
        config_file.close()
        for line in text:
            __temp[line.split("=")[0]]=line.split("=")[1].replace("\n","")
        return(__temp)

    def __CheckBrowsers(self, Chrome, FireFox, Edge, Opera):
        """If a browser had no gien path, it will try to find the installed path of application.
        Only Windows and these four browsers are supported at the moment."""

        self.__CheckChrome(Chrome)
        self.__CheckFireFox(FireFox)
        self.__CheckEdge(Edge)
        self.__CheckOpera(Opera)

    def __pathExists(self, path):
        if os.path.exists(path):
            return(path)
        return("")

    def __CheckEdge(self, Edge):
        if Edge=="":
            self.__Config["Edge"]=self.__GetLocation("Edge")
            if self.__Config["Edge"] == "":
                self.__Config["Edge"] = self.__pathExists("C:\Program Files\Microsoft\Edge\Application\msedge.exe")
            if self.__Config["Edge"] == "":
                self.__Config["Edge"] = self.__pathExists("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
            if self.__Config["Edge"] == "":
                self.__Config["Edge"] = self.__Browser_Search_Window("Edge")


    def __CheckOpera(self, Opera):
        if Opera=="":
            self.__Config["Opera"]=self.__GetLocation("Opera")
            if self.__Config["Opera"] == "":
                self.__Config["Opera"] = self.__pathExists("C:\\Users\\"+os.getlogin()+"\AppData\Local\Programs\Opera\launcher.exe")

            if self.__Config["Opera"] == "":
                self.__Config["Opera"] = self.__Browser_Search_Window("Opera")


    def __CheckFireFox(self, FireFox):
        if FireFox=="":
            self.__Config["FireFox"]=self.__GetLocation("FireFox")
            if self.__Config["FireFox"]=="":
                self.__Config["FireFox"] = self.__pathExists("C:\Program Files\Mozilla Firefox\firefox.exe")
            if self.__Config["FireFox"]=="":
                self.__Config["FireFox"] = self.__pathExists("C:\Program Files (x86)\Mozilla Firefox\firefox.exe")
            if self.__Config["FireFox"]=="":
                self.__Config["FireFox"] = self.__Browser_Search_Window("FireFox")

    def __CheckChrome(self, Chrome):
        if Chrome=="":
            self.__Config["Chrome"]=self.__GetLocation("Chrome")
            if self.__Config["Chrome"]=="":
                self.__Config["Crome"] = self.__pathExists("C:\Program Files\Google\Chrome\Application\chrome.exe")
            if self.__Config["Chrome"]=="":
                self.__Config["Crome"] = self.__pathExists("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
            if self.__Config["Chrome"] == "":
                self.__Config["Chrome"] = self.__Browser_Search_Window("Chrome")


    def __Browser_Search_Window(self, browser):

        title = self.__dicts.getWordFromDict(self.__Config["Language"], "browserNotFoundTitle").replace("#browser#", browser)
        message = self.__dicts.getWordFromDict(self.__Config["Language"], "browserNotFoundMessage").replace("#browser#", browser)
        asktitle=self.__dicts.getWordFromDict(self.__Config["Language"], "browserNotFoundAskTitle").replace("#browser#", browser)

        QuestionBox=messagebox.askyesno(title=title, message=message, default="yes")
        if QuestionBox==False:
            return("")
        else:
            return(askopenfilename(initialdir = "*",title = asktitle, filetypes = ((".exe","*.exe"),)))

    def __GetLocation(self, browser):
        import winapps
        for app in winapps.search_installed(browser):
            if app!="":
                result=self.__Get_App_Path(self.__Regex_Get_Install_Location(app), browser)
                if result!="":
                    return(result)
        return("")

    def __Regex_Get_Install_Location(self, app):
        FindRegex = re.findall(r"install_location=WindowsPath\(\'[a-zA-Z0-9:\/\s\(\)]+\'\)", str(app))
        if len(FindRegex) > 0:
            return(FindRegex[0].replace("install_location=WindowsPath('", "").replace("')", ""))
        return("")

    def __Get_App_Path(self, result, browser):
        for root, dirs, files in os.walk(result):
            for file in files:
                if file.upper()==browser.upper()+".EXE" or str(browser.upper()+".EXE") in file.upper():
                    return(str(root + "/" + file).replace("\\", "/"))
        return("")

class Config(Config_Real):
    """This is the class that can be accessed directly for the
    configuration."""

    def __init__(self, dicts):
        super().__init__(dicts)

    def set_Element(self, key, value):
        super().Set_Element(key, value)

    def get_Element(self, key):
        return(super().get_Element(key))

class Monitor_Real(ABC):
    """This the real class that is supposed to get the current
    resolution of the primary monitor."""

    @abstractmethod
    def __init__(self):
        import ctypes as ctypes

        user32 = ctypes.windll.user32
        self.__screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    @abstractmethod
    def get_Screensize(self):
        return(self.__screensize)

class Monitor(Monitor_Real):
    """This is the class the user can primary access to get the resolution of the screen."""

    def __init__(self):
        super().__init__()

    def get_Screensize(self):
        return(super().get_Screensize())

class DisplayLoading_Real(ABC):
    """This class only opens a loading screen image and swaits for 3 seccnds,
    then destroys the window and then goes back to the main window."""

    @abstractmethod
    def __init__(self, size):
        from PIL import ImageTk, Image

        if size[0]>1600:
            self.__w_Size=800
        elif size[0]>1280:
            self.__w_Size=650
        elif size[0]>800:
            self.__w_Size=550
        else:
            self.__w_Size=400

        self.__h_Size=round((self.__w_Size/800)*300)
        self.__Loading_Window=Toplevel()
        self.__Loading_Window.geometry("%dx%d+%d+%d" % (self.__w_Size, self.__h_Size,
                                                        (size[0]/2)-self.__w_Size/2,
                                                        (size[1]/2)-self.__h_Size/2-50))
        self.__Loading_Window.overrideredirect(True)
        self.__Loading_Window.resizable(False, False)
        self.__img = ImageTk.PhotoImage(Image.open("loading.png").resize((self.__w_Size,self.__h_Size)))

        self.__imgLabel = Label(self.__Loading_Window, image=self.__img)
        self.__imgLabel.pack()

        self.__Loading_Window.after(3500, self.destroy_Loader)
        self.__Loading_Window.wait_window()


    def destroy_Loader(self):
        self.__Loading_Window.destroy()


class DisplayLoading(DisplayLoading_Real):
    """Access to the implemented class creating the Lading screen."""

    def __init__(self, size):
        super().__init__(size)


class Create_MainWindow_Real(ABC):
    """Creating the Main Window, loads data for application."""
    def __init__(self, main):

        self.__main=main
        self.__main.geometry("%dx%d+%d+%d" % (1, 1, 1, 1))
        self.__main.overrideredirect(True)
        self.__main.resizable(False, False)

        self.__dicts = Dictionaries()
        __monitor = Monitor()
        __loading_Screen = DisplayLoading(__monitor.get_Screensize())
        self.__config = Config(self.__dicts)
        if self.__config.get_Element("StaticSize")=="0":
            s=self.__GetWindowSize(__monitor.get_Screensize())
        else:
            s=int(self.__config.get_Element("StaticSize"))

        self.__size_Num=self.__Create_Main_Window_By_Screen_Size(s, __monitor.get_Screensize(), self.__config.get_Element("Language"))

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
            self.__create_Main_Window_size4(size)
        elif S==3:
            self.__create_Main_Window_size3(size)
        elif s==2:
            self.__create_Main_Window_size2(size)
        else:
            self.__create_Main_Window_size1(size)

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
        import pyglet

        pyglet.font.add_file('HAMMRF.ttf')
        self.defineWords(lang)

        self.__hammerFont=("Hammerfat", 7+(size*2))
        self.__buttonSize=40

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

        self.Hint=StringVar()
        self.HintText = Label(self.__main, textvariable=self.Hint, font=self.__hammerFont)

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

    def __create_Main_Window_size1(self, size):
        self.__create_Main_Window_size3(size) # Temporal set only!

    def __create_Main_Window_size2(self, size):
        self.__create_Main_Window_size3(size) # Temporal set only!

    def __create_Main_Window_size3(self, size):
        self.__setMainGeo(1400, 1000, size)

    def __create_Main_Window_size4(self, size):
        self.__create_Main_Window_size3(size) # Temporal set only!

    def __setMainGeo(self, w, h, size):
        self.__main.geometry("%dx%d+%d+%d" % (w, h, (size[0]/2)-(w/2), (size[1]/2)-(h/2)-25))

    def on_Leave(self, event):
        self.Hint.set("")

    def __setHintTextLocation(self, num):
        self.HintText.place(x=4+(self.__buttonSize)*num, y=self.__buttonSize)


    def on_enterNewB(self, event):
        self.Hint.set(self.__new)
        self.__setHintTextLocation(0)


    def on_enterOpenB(self, event):
        self.Hint.set(self.__open)
        print(event)
        self.__setHintTextLocation(0)


    def on_enterSaveB(self, event):
        self.Hint.set(self.__save)
        self.__setHintTextLocation(0)


    def on_enterSaveAsB(self, event):
        self.Hint.set(self.__save_as)
        self.__setHintTextLocation(0)


    def on_enterCopy(self, event):
        self.Hint.set(self.__copy)
        self.__setHintTextLocation(4.25)


    def on_enterPaste(self, event):
        self.Hint.set(self.__paste)
        self.__setHintTextLocation(4.25)

    def on_enterHTML(self, event):
        self.Hint.set(self.__HTML)
        self.__setHintTextLocation(6.5)

    def on_enterFastTest(self, event):
        self.Hint.set(self.__FastTest)
        self.__setHintTextLocation(6.5)

    def on_enterFFox(self, event):
        if self.__config.get_Element("FireFox")=="":
            self.Hint.set(self.__browserNotSet.replace("#browser#", "Firefox"))
        else:
            self.Hint.set(self.__FFoxTest)
        self.__setHintTextLocation(6.5)

    def on_enterChrome(self, event):
        if self.__config.get_Element("Chrome")=="":
            self.Hint.set(self.__browserNotSet.replace("#browser#", "Chrome"))
        else:
            self.Hint.set(self.__ChromeTest)
        self.__setHintTextLocation(6.5)

    def on_enterEdge(self, event):
        if self.__config.get_Element("FireFox")=="":
            self.Hint.set(self.__browserNotSet.replace("#browser#", "Edge"))
        else:
            self.Hint.set(self.__EdgeTest)
        self.__setHintTextLocation(6.5)

    def on_enterOpera(self, event):
        if self.__config.get_Element("Opera")=="":
            self.Hint.set(self.__browserNotSet.replace("#browser#", "Opera"))
        else:
            self.Hint.set(self.__OperaTest)
        self.__setHintTextLocation(6.5)

    def on_enterSettings(self, event):
        self.Hint.set(self.__settings)
        self.__setHintTextLocation(12.75)

    def on_enterHelp(self, event):
        self.Hint.set(self.__help)
        self.__setHintTextLocation(12.75)

    def on_enterAbout(self, event):
        self.Hint.set(self.__about)
        self.__setHintTextLocation(12.75)

class Create_MainWindow(Create_MainWindow_Real):

    def __init__(self, main):
        super().__init__(main)

if __name__=="__main__":


    Main_Window = Tk()
    Creator = Create_MainWindow(Main_Window)
    Main_Window.mainloop()

