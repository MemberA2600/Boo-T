from tkinter import *
from abc import *
import os
import sys
import re
from tkinter.filedialog import *
from tkinter import messagebox

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
        super().set_Element(key, value)

    def get_Element(self, key):
        return(super().get_Element(key))