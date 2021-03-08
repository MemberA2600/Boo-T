class ColorPalettes():

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

    def getPalette(self, color):
        return(self.__colors[color])


    def getColors(self):
        return(self.__colors.keys())


    def getRGBA(self, color):
        return(self.__rgbaCodes[color])