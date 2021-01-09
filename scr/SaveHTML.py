from abc import *
from tkinter.filedialog import *

class SaveHTML_Real(ABC):

    def __init__(self, code, config, dicts):
        self.__dicts=dicts
        self.__Config = config
        savename = asksaveasfilename(initialdir="*",
                                     title=self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "save"),
                                     filetypes=((self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                              "fileHTML"), "*.html"),
                                                (self.__dicts.getWordFromDict(self.__Config.get_Element("Language"),
                                                                              "fileTxT"), "*.txt")))

        try:
            if self.__Config.get_OS_Name() == "Windows":
                filepath = "/".join(savename.split("/")[0:-1]) + "/"
                sep="/"
            else:
                filepath = "\\"[0].join(savename.split("\\"[0])[0:-1]) + "\\"[0]
                sep = "\\"[0]

            if os.path.exists(filepath+"img")==False:
                os.mkdir(filepath+"img")
            if os.path.exists(filepath+"bootstrap")==False:
                os.mkdir(filepath+"bootstrap")

            if savename.endswith(".html") == False or savename.endswith(".txt"):
                savename += ".html"

            code = code
            code = self.__searchForImagesPaths(code, sep, filepath)

            opened = open(savename, "w")
            opened.write(code)
            opened.close()

            for img in ["facebook.png", "youtube.png", "instagram.png", "vkontakte.png", "googleplus.png", "linkedin.png", "twitter.png", "github.png"]:
                self.__copyFile(str(filepath+"img"+ sep), img, sep, str(os.path.abspath(os.getcwd())+sep+"icons"))

            for root, dirs, files in os.walk("bootstrap/"):
                for file in files:
                    self.__copyFile(str(filepath+"bootstrap"+ sep), file, sep, str(os.path.abspath(os.getcwd())+sep+"bootstrap"))

        except Exception as e:
            from tkinter import messagebox

            messagebox.showerror(
                self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "fileSaveErrorTitle"),
                self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "fileSaveError").replace("#path#",
                    savename) + "\n" + str(e))


    def __copyFile(self, dir, file,sep,sourcedir):
        from shutil import copyfile
        src = sourcedir+sep+file
        dest = str(dir + file).replace("\\"[0], sep)

        if os.path.exists(dest) == False:
            copyfile(src, dest)

    def __searchForImagesPaths(self, code, sep, filepath):
        import re
        regex=re.findall(r"src=\'[\-:a-zA-Z0-9\.\/\\]+\'", code)
        regex2=re.findall(r"url\(\'[\-:a-zA-Z0-9\.\/\\]+\'\)", code)

        for item in regex:
            temp = item.replace("src=","").replace("'","")
            img_types = ["jpg", "bmp", "gif", "png", "tiff", "webp", "avif",  "ico", "apng", "svg", "jpeg"]

            if (temp.split(".")[-1] in img_types) and temp.startswith("http") == False and (temp.startswith("/") or temp[1:3] == ":/"):
                filename=temp.split(sep)[-1]
                self.__copyFile(str(filepath+"img"+sep), filename, sep, sep.join(temp.split(sep)[0:-1]))
                code=code.replace(item, "src='img/" + filename + "'" )
                code=code.replace(item.replace("src", "href"), "href='img/" + filename + "'" )


        for item in regex2:
            temp = item.replace("url(","").replace("'","").replace(")","")
            img_types = ["jpg", "bmp", "gif", "png", "tiff", "webp", "avif",  "ico", "apng", "svg"]

            if (temp.split(".")[-1] in img_types) and temp.startswith("http") == False and (temp.startswith("/") or temp[1:3] == ":/"):
                filename=temp.split(sep)[-1]
                num = 1
                """If path exists, add underline and a 3 digit number with leading zeros to name."""

                fullpath=str(filepath + filename).replace("\\"[0], sep)
                if (os.path.exists(fullpath)):
                    fullpath += "_000"
                while (os.path.exists(fullpath)):
                    fullpath[:-3] + str(f'{num:03d}')

                self.__copyFile(str(filepath+"img"+sep), filename, sep, sep.join(temp.split(sep)[0:-1]))
                code =code.replace(item, "url('img/" + filename + "')" )

        return(code)

class SaveHTML(SaveHTML_Real):

    def __init__(self, code, config, dicts):
        super().__init__(code, config, dicts)