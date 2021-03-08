from tkinter import *
from abc import *
import os

class TkinterHTMLviewer_REAL(ABC):

    @abstractmethod
    def __init__(self, dicts, Config, hammerFont, master, main, fontSize, monitor, code):
        self.__dicts=dicts
        self.__Config=Config
        self.__hammerFont=hammerFont
        self.master=master
        self.__main=main
        self.__fontSize=fontSize

        self.__HTMLviewer = Toplevel()
        self.__HTMLviewer.title(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "HTMLviewer"))
        self.__HTMLviewer.resizable(False, False)

        __monitor = monitor
        __s = __monitor.get_screensize()

        if __s[0] < 800:
            __h = 400
        elif __s[0] < 1025:
            __h = 645
        elif __s[0] < 1625:
            __h = 750
        else:
            __h = 1150

        self.__sizes={"xs": 360, "sm": 576, "md": 768, "lg": 992, "xl": 1200}


        __w = self.__getClosest(__s[0])

        self.__setViewerSize(__w, __h, __s)
        self.__createViewer(__w, __h, __s, fontSize, hammerFont, code)

        self.__HTMLviewer.focus()
        self.__HTMLviewer.wait_window()

    def __createViewer(self, __w, __h, __s, fontSize, hammerFont, code):
        """Creates the menu where you can watch the result."""

        from tkinter.font import Font, families

        self.__HTMLviewer.pack_propagate(False)
        hammerFont = Font(font='Hammerfat_Hun')
        hammerFont.config(size=fontSize+2)

        self.__fixheight = __h
        self.__createButtonsFrame(__w, hammerFont)
        self.__createHTMLFrame(__w, __h, code)

    def __createButtonsFrame(self, __w, hammerFont):

        self.__ButtonsFrame = Frame(self.__HTMLviewer, width=__w, height=128)
        self.__ButtonsFrame.pack_propagate(False)
        self.__ButtonsFrame.place(x=0, y=0)

        from PIL import ImageTk, Image

        self.__imgPhone = ImageTk.PhotoImage(Image.open("icons/smartphone.png"))
        self.__sizeXSLabel, self.__sizeXSButtonFrame, self.__sizeXSButton = self.__createSizeButton(self.__imgPhone, None, __w, -3.50, hammerFont, "XS")

        self.__imgTablet = ImageTk.PhotoImage(Image.open("icons/tablet.png"))
        self.__sizeSMLabel, self.__sizeSMButtonFrame, self.__sizeSMButton = self.__createSizeButton(self.__imgTablet, None,
                                                                                                    __w, -2.25, hammerFont,
                                                                                                    "SM")
        self.__imgPCOld = ImageTk.PhotoImage(Image.open("icons/monitor_old.png"))
        self.__sizeSMLabel, self.__sizeSMButtonFrame, self.__sizeSMButton = self.__createSizeButton(self.__imgPCOld, None,
                                                                                                    __w, -1.0, hammerFont,
                                                                                                    "MD")
        self.__imgPCNomal = ImageTk.PhotoImage(Image.open("icons/monitor_normal.png"))
        self.__sizeSMLabel, self.__sizeSMButtonFrame, self.__sizeSMButton = self.__createSizeButton(self.__imgPCNomal, None,
                                                                                                    __w, 0.25, hammerFont,
                                                                                                    "LG")
        self.__imgPCLarge = ImageTk.PhotoImage(Image.open("icons/monitor_large.png"))
        self.__sizeSMLabel, self.__sizeSMButtonFrame, self.__sizeSMButton = self.__createSizeButton(self.__imgPCLarge, None,
                                                                                                    __w, 1.50, hammerFont,
                                                                                                    "XL")
    def __createSizeButton(self, img, command, __w, x, hammerFont, text):
        x=round(__w/2)+(32*x)
        __label = Label(self.__HTMLviewer, image=img, width=32, height=32, command=command)
        __label.place(x=x-2, y=0)
        __buttonFrame=Frame(self.__HTMLviewer, width=32, height=32)
        __buttonFrame.place(x=x, y=40)
        __buttonFrame.pack_propagate(False)
        __button = Button(__buttonFrame, text=text, command=command)
        __button.config(font=hammerFont)
        __button.pack(fill=BOTH)
        return(__label, __buttonFrame, __button)

    def __getClosest(self, w):
        difference=99999
        temp = ""

        for item in self.__sizes:
            if abs(w-self.__sizes[item])<difference and self.__sizes[item]<w:
                difference = abs(w-self.__sizes[item])
                temp = item

        return(self.__sizes[temp])

    def __setViewerSize(self, w, h, size):
        self.__HTMLviewer.geometry("%dx%d+%d+%d" % (w, h, (size[0] / 2) - (w / 2), (size[1] / 2) - (h / 2) - 25))

    def __createHTMLFrame(self, __w, __h, code):
        from tkhtmlview import HTMLLabel

        html = HTMLLabel(self.__HTMLviewer, html=code, width=__w, height=__h-140)
        html.pack(side=BOTTOM)

class TkinterHTMLviewer(TkinterHTMLviewer_REAL):

    def __init__(self, dicts, Config, hammerFont, master, main, fontSize, monitor, code):
        super().__init__(dicts, Config, hammerFont, master, main, fontSize, monitor, code)


