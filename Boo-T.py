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
        self.__CheckBrowsers(self.__Config["Chrome"],
                             self.__Config["FireFox"],
                             self.__Config["Edge"],
                             self.__Config["Opera"],
                             self.__Config["Safari"])

    @abstractmethod
    def Set_Element(self, key, value):
        self.__Config[key]=value

    @abstractmethod
    def Get_Element(self, key):
        return(self.__Config[key])

    def __Load_Config_File(self):
        __temp={}
        config_file=open("Config.txt", "r")
        text=config_file.readlines()
        config_file.close()
        for line in text:
            __temp[line.split("=")[0]]=line.split("=")[1].replace("\n","")
        return(__temp)

    def __CheckBrowsers(self, Chrome, FireFox, Edge, Opera, Safari):
        if Chrome=="":
            self.__Config["Chrome"]=self.__GetLocation("Chrome")

    def __GetLocation(self, browser):
        import winapps
        result=""
        for app in winapps.search_installed(browser):
            if app!="":
                self.__Regex_Get_Install_Location(app)
        if result=="":
            return(result)
        else:
            pass

    def __Regex_Get_Install_Location(self, app):
        FindRegex = re.findall(r"install_location=WindowsPath\(\'[a-zA-Z0-9:\/\s]+\'\)", str(app))
        if len(FindRegex) > 0:
            result = FindRegex[0].replace("install_location=WindowsPath('", "").replace("')", "")
        return(result)

class Config(Config_Real):
    """This is the class that can be accessed directly for the
    configuration."""

    def __init__(self):
        super().__init__()

    def Set_Element(self, key, value):
        super().Set_Element(key, value)

    def Get_Element(self, key):
        return(super().Get_Element(key))


if __name__=="__main__":
    Config=Config()