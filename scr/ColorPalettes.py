from abc import *


class ColorPalettes_REAL(ABC):

    @abstractmethod
    def __init__(self):
        self.__colors = {}
        self.__getColors()
        self.__rgbaCodes={}
        self.__getRGBA()

    def __getColors(self):
        for line in open("default/Colors.txt", "r").readlines():
            xxx = line.split("=")
            self.__colors[xxx[0].strip()] = []
            for color in xxx[1].split(","):
                self.__colors[xxx[0].strip()].append(color.strip())

    def __getRGBA(self):
        for line in open("default/RGBA.txt", "r").readlines():
            xxx = line.split("=")
            self.__rgbaCodes[xxx[0].strip()] = xxx[1].strip()


    @abstractmethod
    def getPalette(self, color):
        return(self.__colors[color])

    @abstractmethod
    def getColors(self):
        return(self.__colors.keys())

    @abstractmethod
    def getRGBA(self, color):
        return(self.__rgbaCodes[color])

class ColorPalettes(ColorPalettes_REAL):

    def __init__(self):
        super().__init__()

    def getPalette(self, color):
        return(super().getPalette(color))

    def getColors(self):
        return(super().getColors())

    def getRGBA(self, color):
        return(super().getRGBA(color))
