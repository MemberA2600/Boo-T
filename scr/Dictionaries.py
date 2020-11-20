from tkinter import *
from abc import *
import os
import sys
import re
from tkinter.filedialog import *
from tkinter import messagebox

class Dictionaries_REAL(ABC):
    """Cointains text the application will display, loaded from '/dicts'."""
    @abstractmethod
    def __init__(self):
        self.__D = {}
        for root, dirs, files in os.walk("dicts/"):
            for file in files:
                self.__LoadDict(root+file, file.replace(".txt",""))

    def __LoadDict(self, path, name):
        try:
            f = open(path, "r")
            lines = f.readlines()
            f.close()
        except:
            """Added another method because in Linux, it throws UnicodeDecodeError."""
            f = open(path, "r", encoding="latin1")
            lines = f.readlines()
            for num in range(0, len(lines)-1):
                lines[num]=lines[num].replace("\n", "")
            f.close()

        self.__D[name]={}

        for line in lines:
            self.__D[name][line.replace("\r","").replace("\n","").split("=")[0]] = line.replace("\r","").replace("\n","").split("=")[1].replace("\n","")

    @abstractmethod
    def getWordFromDict(self, lang, word):
        return(self.__D[lang][word])

class Dictionaries(Dictionaries_REAL):
    def __init__(self):
        super().__init__()

    def getWordFromDict(self, lang, word):
        return(super().getWordFromDict(lang,word))