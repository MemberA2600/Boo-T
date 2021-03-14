from tkinter import *

class UndoBuffer():

    def __init__(self, button):
        self.__buffer = [""]
        self.__maxSize=25
        self.__button = button

    def saveBox(self, code):
        if len(self.__buffer)>=self.__maxSize:
            self.__buffer.pop(0)
        self.__buffer.append(code)
        self.__button.config(state=NORMAL)

    def undo(self):
        try:
            temp=self.__buffer[-1]
            self.__buffer.pop()
            if len(self.__buffer)==0:
                self.__button.config(state=DISABLED)
            return(temp)
        except:
            return(False)