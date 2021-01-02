from tkinter import *
from abc import *
from tkinter.filedialog import *

class GetCodeOnly_REAL(ABC):

    @abstractmethod
    def __init__(self, dicts, config, hammer, master, main, fontSize, monitor, code):
        import tkinter.scrolledtext as tkscrolled

        self.__dicts = dicts
        self.__Config = config
        self.__hammerFont = hammer
        self.master = master
        self.__main = main
        self.__code = code

        __monitor = monitor
        size = __monitor.get_screensize()

        self.__TheBox = Toplevel()
        self.__TheBox.title(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "generateCode"))
        self.__TheBox.resizable(False, False)
        self.__TheBox.geometry("%dx%d+%d+%d" % (500, 450, size[0] / 2 - 250, size[1] / 2 - 400))

        self.__TheBox.pack_propagate(False)

        self.__codeBoxFrame = Frame(self.__TheBox, width=500, height=400)
        self.__codeBoxFrame.place(x=0, y=0)
        self.__codeBoxFrame.pack_propagate(False)

        if (self.__Config.get_Element("DarkBox") == "False"):
            self.__color = "white"
            self.__color2 = "black"
        else:
            self.__color = "black"
            self.__color2 = "lightgray"

        self.__codebox = tkscrolled.ScrolledText(self.__codeBoxFrame, width=999, height=999, font=self.__hammerFont)
        self.__codebox.pack()

        self.__codebox.config(bg=self.__color, fg=self.__color2, wrap=WORD)

        self.__buttonsFrame1 = self.__createButtonFrame(0)
        self.__buttonsFrame2 = self.__createButtonFrame(166)
        self.__buttonsFrame3 = self.__createButtonFrame(332)


        self.__copyButton = self.__createButton(self.__buttonsFrame1, self.__dicts.getWordFromDict(
            self.__Config.get_Element("Language"),
            "copyToClipBoard"),
            self.__doCopy
        )

        self.__saveButton = self.__createButton(self.__buttonsFrame2, self.__dicts.getWordFromDict(
            self.__Config.get_Element("Language"),
            "save"),
            self.__doSaveAs
        )

        self.__cancelButton = self.__createButton(self.__buttonsFrame3, self.__dicts.getWordFromDict(
            self.__Config.get_Element("Language"),
            "Cancel"),
            self.__destroyWindow
        )

        self.__getCode(code)
        self.__TheBox.focus()
        self.__TheBox.wait_window()

    def __getCode(self, code):
        self.__codebox.delete(0.0, END)

        if self.__Config.get_Element("FortranCompiler")=="False":
            import PythonCompiler
            Compiler = PythonCompiler.Compiler(code, self.__Config, self.__dicts)
            code = Compiler.compiled

        else:
            import subprocess
            subprocess.call("TODO", creationflags=0x08000000)

        self.__codebox.insert(0.0, code)


    def __createButtonFrame(self, x):
        frame = Frame(self.__TheBox, width=166, height=50)
        frame.place(x=x, y=410)
        frame.pack_propagate(False)
        return(frame)


    def __createButton(self, frame, text, command):
        button = Button(frame, text=text, command=command, width=len(text)+2)
        button.config(font=self.__hammerFont)
        button.pack(side = TOP)
        return(button)

    def __doCopy(self):
        import clipboard
        clipboard.copy(self.__codebox.get(0.0, END))

    def __destroyWindow(self):
        self.__TheBox.destroy()

    def __doSaveAs(self):
        savename = asksaveasfilename(initialdir="*",
                                     title=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "save"),
                                     filetypes=((self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                              "fileHTML"), "*.html"),
                                                (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                              "fileTxT"), "*.txt")))

        try:
            if savename.endswith(".html") == False or savename.endswith(".txt"):
                savename += ".html"
            opened = open(savename, "w")
            opened.write(self.__codebox.get(0.0, END))
            opened.close()

        except Exception as e:
            messagebox.showerror(
                self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "fileSaveErrorTitle"),
                self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "fileSaveError").replace("#path#",
                    savename) + "\n" + str(e))
        self.__destroyWindow()

class GetCodeOnly(GetCodeOnly_REAL):

    def __init__(self, dicts, config, hammer, master, main, fontSize, monitor, code):
        super().__init__(dicts, config, hammer, master, main, fontSize, monitor, code)