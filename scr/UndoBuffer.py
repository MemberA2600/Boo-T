from tkinter import *
from abc import *
import os

class UndoBuffer_REAL(ABC):

    @abstractmethod
    def __init__(self, button):
        self.__buffer = [""]
        self.__maxSize=25
        self.__button = button

    @abstractmethod
    def saveBox(self, code):
        if len(self.__buffer)>=self.__maxSize:
            self.__buffer.pop(0)
        self.__buffer.append(code)
        self.__button.config(state=NORMAL)

    @abstractmethod
    def undo(self):
        try:
            temp=self.__buffer[-1]
            self.__buffer.pop()
            if len(self.__buffer)==0:
                self.__button.config(state=DISABLED)
            return(temp)
        except:
            return(False)


class UndoBuffer(UndoBuffer_REAL):

    def __init__(self, button):
        super().__init__(button)

    def saveBox(self, code):
        super().saveBox(code)

    def undo(self):
        return(super().undo())
