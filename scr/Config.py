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
        self.__os_Name=self.__get_OS()
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


    def __get_OS(self):
        import platform
        return(platform.system())

    @abstractmethod
    def get_OS_Name(self):
        """Many objects work differently with Windows and Linux, so they have to ask for the
        OS really often!"""
        return(self.__os_Name)

    @abstractmethod
    def get_Element(self, key):
        """Gives the objects in the outside, mostly the menüs, the current settings."""
        return(self.__Config[key])

    def __Load_Config_File(self):
        """Will load the config file located in the root folder."""
        if os.path.exists("Config.txt"):
            return(self.__loadDict("Config.txt"))
        else:
            return(self.__loadDict("default/Config.txt"))

    def __loadDict(self, config_file):
        __temp={}
        config_file = open(config_file, "r")
        text=config_file.readlines()
        config_file.close()
        for line in text:
            """Loads the config, then splits it into two at the eq mark. Both parts are removed of some unneccessery possible
            special characters. the first part becomes the key, the other the value."""
            __temp[line.replace("\r","").replace("\n","").split("=")[0]]=line.replace("\r","").replace("\n","").split("=")[1].replace("\n","")
        return(__temp)

    @abstractmethod
    def load_Config_Defaults(self):
        """Loads the Default config file from subfolder."""
        self.__Config=self.__loadDict("default/Config.txt")

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
        """Checks browser location by directly searching in the OS and at the default locations as well."""
        if Edge=="":
            if self.__os_Name=="Windows":
                self.__Config["Edge"]=self.__GetLocation("Edge")
                if self.__Config["Edge"] == "":
                    self.__Config["Edge"] = self.__pathExists("C:\Program Files\Microsoft\Edge\Application\msedge.exe")
                if self.__Config["Edge"] == "":
                    self.__Config["Edge"] = self.__pathExists("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
            else:
                self.__Config["Edge"]=self.__LinuxFindLocation("Edge")
                if self.__Config["Edge"] == "":
                    self.__Config["Edge"] = self.__LinuxFindLocation("microsoft-edge")

            if self.__Config["Edge"] == "":
                self.__Config["Edge"] = self.__Browser_Search_Window("Edge")

    def __LinuxFindLocation(self, app):
        temp = self.__LinuxFindCode(app)
        if temp == "":
            temp = self.__LinuxFindCode(app.lower())

        return(temp)

    def __LinuxFindCode(self, codepart):
        """Uses whereis in Linux to get the location of the app."""
        return((os.popen(str("whereis "+ codepart)).read()).split(":")[1].replace("\n", ""))

    def __CheckOpera(self, Opera):
        """Checks browser location by directly searching in the OS and at the default locations as well."""

        if Opera=="":
            if self.__os_Name=="Windows":
                self.__Config["Opera"]=self.__GetLocation("Opera")
                if self.__Config["Opera"] == "":
                    self.__Config["Opera"] = self.__pathExists("C:\\Users\\"+os.getlogin()+"\AppData\Local\Programs\Opera\launcher.exe")
            else:
                self.__Config["Opera"] = self.__LinuxFindLocation("Opera")

            if self.__Config["Opera"] == "":
                self.__Config["Opera"] = self.__Browser_Search_Window("Opera")


    def __CheckFireFox(self, FireFox):
        """Checks browser location by directly searching in the OS and at the default locations as well."""

        if FireFox=="":
            if self.__os_Name=="Windows":
                self.__Config["FireFox"]=self.__GetLocation("FireFox")
                if self.__Config["FireFox"]=="":
                    self.__Config["FireFox"] = self.__pathExists("C:\Program Files\Mozilla Firefox\firefox.exe")
                if self.__Config["FireFox"]=="":
                    self.__Config["FireFox"] = self.__pathExists("C:\Program Files (x86)\Mozilla Firefox\firefox.exe")
            else:
                self.__Config["FireFox"] = self.__LinuxFindLocation("Firefox")

            if self.__Config["FireFox"]=="":
                self.__Config["FireFox"] = self.__Browser_Search_Window("FireFox")

    def __CheckChrome(self, Chrome):
        """Checks browser location by directly searching in the OS and at the default locations as well."""

        if Chrome=="":
            if self.__get_OS() == "Windows":
                self.__Config["Chrome"]=self.__GetLocation("Chrome")
                if self.__Config["Chrome"]=="":
                    self.__Config["Crome"] = self.__pathExists("C:\Program Files\Google\Chrome\Application\chrome.exe")
                if self.__Config["Chrome"]=="":
                    self.__Config["Crome"] = self.__pathExists("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
            else:
                self.__Config["Chrome"] = self.__LinuxFindLocation("Chrome")
                if self.__Config["Chrome"] == "":
                    self.__Config["Chrome"] = self.__LinuxFindLocation("google-chrome")

            if self.__Config["Chrome"] == "":
                self.__Config["Chrome"] = self.__Browser_Search_Window("Chrome")


    def __Browser_Search_Window(self, browser):
        """Asks if the user want to set the browser location manually."""
        title = self.__dicts.getWordFromDict(self.__Config["Language"], "browserNotFoundTitle").replace("#browser#", browser)
        message = self.__dicts.getWordFromDict(self.__Config["Language"], "browserNotFoundMessage").replace("#browser#", browser)
        asktitle=self.__dicts.getWordFromDict(self.__Config["Language"], "browserNotFoundAskTitle").replace("#browser#", browser)

        QuestionBox=messagebox.askyesno(title=title, message=message, default="yes")
        if QuestionBox==False:
            return("")
        else:
            if self.__os_Name=="Windows":
                return(askopenfilename(initialdir = "C:\\",title = asktitle, filetypes = ((self.__dicts.getWordFromDict(self.__Config["Language"], "executable"), "*.exe"),)))
            else:
                return(askopenfilename(initialdir = "/usr/bin/",title = asktitle, filetypes = ((self.__dicts.getWordFromDict(self.__Config["Language"], "executable"), "*.*"),)))


    def __GetLocation(self, browser):
        """This is the Windows only applicaton """
        import winapps
        for app in winapps.search_installed(browser):
            if app!="":
                result=self.__Get_App_Path(self.__Regex_Get_Install_Location(app), browser)
                if result!="":
                    return(result)
        return("")

    def __Regex_Get_Install_Location(self, app):
        """Searches for the application's path in winapps result list"""
        FindRegex = re.findall(r"install_location=WindowsPath\(\'[a-zA-Z0-9:\/\s\(\)]+\'\)", str(app))
        if len(FindRegex) > 0:
            return(FindRegex[0].replace("install_location=WindowsPath('", "").replace("')", ""))
        return("")

    def __Get_App_Path(self, result, browser):
        """Finds the execute in the path given in winapps."""
        for root, dirs, files in os.walk(result):
            for file in files:
                if file.upper()==browser.upper()+".EXE" or str(browser.upper()+".EXE") in file.upper():
                    return(str(root + "/" + file).replace("\\", "/"))
        return("")

    @abstractmethod
    def saveConfig(self):
        file=open("Config.txt", "w")
        for key in self.__Config:
            file.write(key+"="+self.__Config[key]+"\n")
        file.close()

class Config(Config_Real):
    """This is the class that can be accessed directly for the
    configuration."""

    def __init__(self, dicts):
        super().__init__(dicts)

    def set_Element(self, key, value):
        super().set_Element(key, value)

    def get_Element(self, key):
        return(super().get_Element(key))

    def load_Config_Defaults(self):
        super().load_Config_Defaults()

    def saveConfig(self):
        super().saveConfig()

    def get_OS_Name(self):
        return(super().get_OS_Name())