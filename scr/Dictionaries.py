import os

class Dictionaries():
    """Cointains text the application will display, loaded from '/dicts'."""

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
            """Loads the line, splits it at the eq mark, then both parts get any unneccessery elements removed.
            The first part will became the key, the second the value in the dictionary. """
            self.__D[name][line.replace("\r","").replace("\n","").split("=")[0]] = line.replace("\r","").replace("\n","").split("=")[1].replace("\n","")


    def getWordFromDict(self, lang, word):
        return(self.__D[lang][word])
