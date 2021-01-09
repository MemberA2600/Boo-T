from abc import *

class SyntaxList_Real(ABC):

    @abstractmethod
    def __init__(self):
        self.__syntax = {}
        self.__openSyntax()

    def __openSyntax(self):
        lines = open("default/Syntax.txt", "r").readlines()
        for line in lines:
            self.__syntax[line.split("=",1)[0]] = []
            list_of_things = line.split("=",1)[1].split(",")
            for thing in list_of_things:
                self.__syntax[line.split("=")[0]].append(thing.strip())

    @abstractmethod
    def getKeys(self):
        return(self.__syntax.keys())

    @abstractmethod
    def getValueOfKey(self, key):
        return(self.__syntax[key])

class SyntaxList(SyntaxList_Real):

    def __init__(self):
        super().__init__()

    def getKeys(self):
        return(super().getKeys())

    def getValueOfKey(self, key):
        return(super().getValueOfKey(key))
