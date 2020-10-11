from abc import*
import os
from tkinter import *
import re
from tkinter.filedialog import *
from tkinter import messagebox
import tkinter.scrolledtext as tkscrolled
from tkinterhtml import HtmlFrame


class Config_Real(ABC):
    """This is the real class, hidden from direct accessing.
    The configuration file and the dictionary containing the
    settings can be accessed with it."""

    @abstractmethod
    def __init__(self):
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
        if Chrome=="":
            self.__Config["Chrome"]=self.__GetLocation("Chrome")
            if self.__Config["Chrome"]=="":
                self.__Config["Chrome"] = self.__Browser_Search_Window("Chrome")
        if FireFox=="":
            self.__Config["FireFox"]=self.__GetLocation("FireFox")
            if self.__Config["FireFox"]=="":
                self.__Config["FireFox"] = self.__Browser_Search_Window("FireFox")
        if Edge=="":
            self.__Config["Edge"]=self.__GetLocation("Edge")
            if self.__Config["Edge"] == "":
                self.__Config["Edge"] = self.__Browser_Search_Window("Edge")
        if Opera=="":
            self.__Config["Opera"]=self.__GetLocation("Opera")
            if self.__Config["Opera"] == "":
                self.__Config["Opera"] = self.__Browser_Search_Window("Opera")

    def __Browser_Search_Window(self, browser):
        if self.__Config["Language"]=="Eng":
            title=browser+" not found!"
            message="Couldn't find path to " + browser +"! Would you like to find it yourself?"
            asktitle="Select the laucher for "+browser+"!"
        else:
            title=browser+" nem található!"
            message="Nem található a(z) " + browser +" böngésző! Kívánja manuálisan beállítani?"
            asktitle="Adja meg a(z) "+browser+" alkalmazás helyét!"

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

    def __init__(self):
        super().__init__()

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
    """This class only opens a loading screen image and shows a status bar.
    It's adopting to the screen size"""

    def __init__(self, size):
        from PIL import ImageTk, Image
        import time

        if size[0]>1600:
            __w_Size=800
        elif size[0]>1280:
            __w_Size=650
        elif size[0]>800:
            __w_Size=550
        else:
            __w_Size=400

        __h_Size=round((__w_Size/800)*300)

        self.__Loading_Window=Toplevel()
        self.__Loading_Window.geometry("%dx%d+%d+%d" % (__w_Size, __h_Size,
                                                        (size[0]/2)-__w_Size/2,
                                                        (size[1]/2)-__h_Size/2-50))
        self.__Loading_Window.overrideredirect(True)
        self.__Loading_Window.resizable(False, False)

        self.__img = ImageTk.PhotoImage(Image.open("loading.png").resize((__w_Size,__h_Size)))

        self.__imgLabel = Label(self.__Loading_Window, image=self.__img)
        self.__imgLabel.pack()


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

        monitor = Monitor()
        loading_Screen = DisplayLoading(monitor.get_Screensize())
        config = Config()

class Create_MainWindow(Create_MainWindow_Real):

    def __init__(self, main):
        super().__init__(main)

if __name__=="__main__":
    Main_Window = Tk()
    Creator = Create_MainWindow(Main_Window)
    Main_Window.mainloop()

