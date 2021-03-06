from tkinter.filedialog import *

class SaveHTML():

    def __init__(self, code, config, dicts, savename, path):
        self.__dicts=dicts
        self.__Config = config
        self.__path = path
        if savename == "":
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
                filepath = os.sep.join(savename.split(os.sep)[0:-1]) + os.sep
                sep = os.sep

            if savename == "temp/temp.html":
                filepath=os.getcwd()+sep+"temp"+sep

            if os.path.exists(filepath+"img")==False:
                pass
            else:
                import shutil
                shutil.rmtree(filepath+"img")
            os.mkdir(filepath+"img")

            if os.path.exists(filepath+"bootstrap")==False:
                os.mkdir(filepath+"bootstrap")


            if savename.endswith(".html") == False or savename.endswith(".txt"):
                savename += ".html"
            code = self.__searchForImagesPaths(code, sep, filepath)
            opened = open(savename, "w", encoding='utf8')
            opened.write(code)
            opened.close()

            for img in ["email.png","phone.png","skype.png","facebook.png", "youtube.png", "instagram.png", "vkontakte.png", "googleplus.png", "linkedin.png", "twitter.png", "github.png"]:
                self.__copyFile(str(filepath+"img"+ sep), img, sep, str(os.path.abspath(os.getcwd())+sep+"icons"), img)

            for root, dirs, files in os.walk("bootstrap/"):
                for file in files:
                    self.__copyFile(str(filepath+"bootstrap"+ sep), file, sep, str(os.path.abspath(os.getcwd())+sep+"bootstrap"), file)

        except Exception as e:
            from tkinter import messagebox

            messagebox.showerror(
                self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "fileSaveErrorTitle"),
                self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "fileSaveError").replace("#path#",
                    savename) + "\n" + str(e))


    def __copyFile(self, dir, file,sep,sourcedir, destfile):
        from shutil import copyfile
        src = sourcedir+sep+file
        dest = str(dir + destfile).replace(os.sep, sep)
        copyfile(src, dest)

    def __searchForImagesPaths(self, code, sep, filepath, ):
        import re
        regex=re.findall(r"src=\'[\-:a-zA-Z0-9\.\/\\]+\'", code)
        regex2=re.findall(r"url\(\'[\-:a-zA-Z0-9\.\/\\]+\'\)", code)
        already = []
        source_paths = []
        saved = []
        for item in regex:
            temp = item.replace("src=","").replace("'","")
            img_types = ["jpg", "bmp", "gif", "png", "tiff", "webp", "avif",  "ico", "apng", "svg", "jpeg"]

            if (temp.split(".")[-1] in img_types) and temp.startswith("http") == False:
                if (temp.startswith("/") or temp[1:3] == ":/"):
                    filename=temp.split(sep)[-1]
                    if filename in ["email.png","phone.png","skype.png","facebook.png", "youtube.png", "instagram.png", "vkontakte.png", "googleplus.png", "linkedin.png", "twitter.png", "github.png"]:
                        continue
                    savename = self.__getSaveName(filename, sep, filepath, already)

                    if (temp in source_paths) and (savename in saved):
                        pass
                    else:
                        source_paths.append(temp)
                        saved.append(savename)
                        self.__copyFile(str(filepath+"img"+sep), filename, sep, sep.join(temp.split(sep)[0:-1]), savename)
                    code=code.replace(item, "src='img/" + savename + "'" )
                    code=code.replace(item.replace("src", "href", 1), "href='img/" + savename + "'" )
                else:
                    filename=temp.split(sep)[-1]
                    if filename in ["email.png","phone.png","skype.png","facebook.png", "youtube.png", "instagram.png", "vkontakte.png", "googleplus.png", "linkedin.png", "twitter.png", "github.png"]:
                        continue
                    savename = self.__getSaveName(filename, sep, filepath, already)

                    if (temp in source_paths) and (savename in saved):
                        pass
                    else:
                        source_paths.append(temp)
                        saved.append(savename)
                        sourcedir = sep.join(self.__path.split(sep)[:-1]) + sep + sep.join(temp.split(sep)[0:-1])
                        self.__copyFile(str(filepath+"img"+sep), filename, sep, sourcedir, savename)
                    code=code.replace(item, "src='img/" + savename + "'" )
                    code=code.replace(item.replace("src", "href", 1), "href='img/" + savename + "'" )


        for item in regex2:
            temp = item.replace("url(","").replace("'","").replace(")","")
            img_types = ["jpg", "bmp", "gif", "png", "tiff", "webp", "avif",  "ico", "apng", "svg", "jpeg"]


            if (temp.split(".")[-1] in img_types) and temp.startswith("http") == False:
                if (temp.startswith("/") or temp[1:3] == ":/"):
                    filename=temp.split(sep)[-1]
                    if filename in ["email.png","phone.png","skype.png","facebook.png", "youtube.png", "instagram.png", "vkontakte.png", "googleplus.png", "linkedin.png", "twitter.png", "github.png"]:
                        continue
                    savename = self.__getSaveName(filename, sep, filepath, already)
                    if (temp in source_paths) and (savename in saved):
                        pass
                    else:
                        source_paths.append(temp)
                        saved.append(savename)
                        self.__copyFile(str(filepath+"img"+sep), filename, sep, sep.join(temp.split(sep)[0:-1]), savename)
                    code =code.replace(item, "url('img/" + savename + "')" )
                else:
                    filename=temp.split(sep)[-1]
                    if filename in ["email.png","phone.png","skype.png","facebook.png", "youtube.png", "instagram.png", "vkontakte.png", "googleplus.png", "linkedin.png", "twitter.png", "github.png"]:
                        continue
                    savename = self.__getSaveName(filename, sep, filepath, already)
                    if (temp in source_paths) and (savename in saved):
                        pass
                    else:
                        source_paths.append(temp)
                        saved.append(savename)
                        sourcedir = sep.join(self.__path.split(sep)[:-1]) + sep + sep.join(temp.split(sep)[0:-1])
                        self.__copyFile(str(filepath+"img"+sep), filename, sep, sourcedir, savename)
                    code =code.replace(item, "url('img/" + savename + "')" )

        return(code)

    def __getSaveName(self, filename, sep, filepath, already):
        if filename in already:
            savename = self.__changeName(str(filepath + "img" + sep), filename, sep)
        else:
            savename = filename
            already.append(filename)
        return(savename)

    def __changeName(self, path, file, sep):
        num = 1
        """If path exists, add underline and a 3 digit number with leading zeros to name."""
        file2=file
        if (os.path.exists(path+file)):
            file2 = ".".join(file.split(".")[:-1])+"_000."+file.split(".")[-1]
        while (os.path.exists(path+file2)):
            file2 = ".".join(file.split(".")[:-1])+"_"+str(f'{num:03d}')+"."+file.split(".")[-1]
            num=num+1

        return (file2)