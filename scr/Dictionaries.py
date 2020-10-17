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
        f = open(path, "r")
        lines = f.readlines()
        f.close()
        self.__D[name]={}

        for line in lines:
            self.__D[name][line.split("=")[0]] = line.split("=")[1].replace("\n","")

    @abstractmethod
    def getWordFromDict(self, lang, word):
        return(self.__D[lang][word])

class Dictionaries(Dictionaries_REAL):
    def __init__(self):
        super().__init__()

    def getWordFromDict(self, lang, word):
        return(super().getWordFromDict(lang,word))