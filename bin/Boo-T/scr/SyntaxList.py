class SyntaxList():

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

    def getKeys(self):
        return(self.__syntax.keys())

    def getValueOfKey(self, key):
        return(self.__syntax[key])
