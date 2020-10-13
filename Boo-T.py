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
        __config = Config(self.__dicts)
        self.__size_Num=self.__Create_Main_Window_By_Screen_Size(__monitor.get_Screensize() ,__config.get_Element("Language"))

    def __Create_Main_Window_By_Screen_Size(self, size, lang):
        if size[0]>1600:
            s=4
            self.__create_Main_Window_size4(size)
        elif size[0]>1280:
            s=3
            self.__create_Main_Window_size3(size)
        elif size[0]>800:
            s=2
            self.__create_Main_Window_size2(size)
        else:
            s=1
            self.__create_Main_Window_size1(size)

        self.__create_Menu(lang, s)
        return(s)

    def __create_Menu(self, lang, size):
        from PIL import ImageTk, Image

        __new = self.__dicts.getWordFromDict(lang, "new")
        __open = self.__dicts.getWordFromDict(lang, "open")
        __file = self.__dicts.getWordFromDict(lang, "file")

        self.__main.title("Boo-T")
        self.__main.overrideredirect(False)
        self.__main.iconbitmap("icons/Boots.ico")
        self.__menuBar = Menu(self.__main)
        self.__main.config(menu=self.__menuBar)

        self.__fontSize=9+size

        self.__fileMenu=Menu(self.__menuBar, tearoff=0, font=self.__fontSize)
        self.__menuBar.add_cascade(label=__file, menu=self.__fileMenu)
        self.__fileMenu.add_command(label=__new, font=self.__fontSize)
        self.__fileMenu.add_command(label=__open)
        self.__imgNew = ImageTk.PhotoImage(Image.open("icons/new.png"))
        self.__imgOpen = ImageTk.PhotoImage(Image.open("icons/open.png"))

        self.__new_B=Button(self.__main, image=self.__imgNew, width=32, height=32).place(x=4, y=5)
        self.__new_B=Button(self.__main, image=self.__imgOpen, width=32, height=32).place(x=44, y=5)

    def __create_Main_Window_size1(self, size):
        self.__create_Main_Window_size3(size) # Temporal set only!

    def __create_Main_Window_size2(self, size):
        self.__create_Main_Window_size3(size) # Temporal set only!

    def __create_Main_Window_size3(self, size):
        self.__main.geometry("%dx%d+%d+%d" % (1400, 1000, (size[0]/2)-700, (size[1]/2)-550))

    def __create_Main_Window_size4(self, size):
        self.__create_Main_Window_size3(size) # Temporal set only!

class Create_MainWindow(Create_MainWindow_Real):

    def __init__(self, main):
        super().__init__(main)

if __name__=="__main__":


    Main_Window = Tk()
    Creator = Create_MainWindow(Main_Window)
    Main_Window.mainloop()

