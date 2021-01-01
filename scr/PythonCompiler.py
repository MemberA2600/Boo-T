from abc import *
import re
import os


class Compiler_REAL(ABC):

    @abstractmethod
    def __init__(self, code, config, dicts):

        import ColorPalettes
        self.__Colors = ColorPalettes.ColorPalettes()
        self.__Config=config
        self.__dicts=dicts


        """Basic Variables"""
        self.__author=""
        self.__title=""
        self.__lang=""
        self.__description=""
        self.__charset=""
        self.__keywords=""
        self.__palette=""
        self.__background = ""
        self.__bannerText = ""
        self.__bannerCSS = ""

        """Formatting the code, getting the full, perfect lines before reading it"""
        code = self.__removeComments(code)
        code = self.__removeNewLines(code)
        code=code.split("%%")
        try:
            code.remove("")
        except:
            #If there are no blank lines...
            pass

        """Load_Templates"""
        self.__mainTemplate=open("templates/MainTemplate.txt", "r").read()
        self.__mainTemplateChanged = False
        self.__bannerTemplate=open("templates/BannerTemplate.txt", "r").read()
        self.__bannerTemplateChanged = False
        self.__navBarTemplate=open("templates/NavBarTemplate.txt", "r").read()
        self.__navBarTemplateChanged = False
        self.__footerTemplate=open("templates/FooterTemplate.txt", "r").read()
        self.__footerTemplateChanged = False
        self.__containerTemplate=open("templates/ContainerTemplate.txt", "r").read()
        self.__containerTemplateChanged = False
        self.__cssTemplate=open("templates/CSSTemplate.txt", "r").read()
        self.__cssTemplateChanged = False


        """Compile Line-By-Line, if there is a compile error, puts message at end and sets string"""
        self.compiled = ""
        self.__error=False

        self.__number = 0
        for line in code:
            self.__number+=1
            """Don't compile empty lines."""
            if re.findall(r"[a-zA-Z]", line)!=[]:
                self.__compile(line)
            if self.__error!=False:
                break

        self.__createCompiled()
        if self.__error==False:
            self.__replaceCompiled()
            self.__addColors()

    def __replaceCompiled(self):
        self.compiled = self.compiled.replace("#background#", self.__background)
        self.compiled = self.compiled.replace("#bannerCSS#", self.__bannerCSS)
        self.compiled = self.compiled.replace("#bannertext#", self.__bannerText)


    def __createCompiled(self):
        if self.__error!=False:
            self.compiled = self.__dicts.getWordFromDict(
                self.__Config.get_Element("Language"), "errorBasic").replace("#error#", self.__error).replace("#number#", str(self.__number))
        else:
            self.compiled = self.__mainTemplate

            self.compiled = self.compiled.replace("#author#", self.__author)
            self.compiled = self.compiled.replace("#title#", self.__title)
            self.compiled = self.compiled.replace("#lang#", self.__lang)
            self.compiled = self.compiled.replace("#description#", self.__description)
            self.compiled = self.compiled.replace("#charset#", self.__charset)
            self.compiled = self.compiled.replace("#keywords#", self.__keywords)


            if self.__bannerTemplateChanged==True:
                self.compiled = self.compiled.replace("#Banner#", self.__bannerTemplate)
            else:
                self.compiled = self.compiled.replace("#Banner#", "")

            if self.__navBarTemplateChanged==True:
                self.compiled = self.compiled.replace("#NavBar#", self.__navBarTemplate)
            else:
                self.compiled = self.compiled.replace("#NavBar#", "")


            if self.__containerTemplateChanged==True:
                self.compiled = self.compiled.replace("#Container#", self.__containerTemplate)
            else:
                self.compiled = self.compiled.replace("#Container#", "")

            if self.__footerTemplateChanged==True:
                self.compiled = self.compiled.replace("#Footer#", self.__footerTemplate)
            else:
                self.compiled = self.compiled.replace("#Footer#", "")

            if self.__cssTemplateChanged==True:
                self.compiled = self.compiled.replace("#style#", self.__cssTemplate)
            else:
                self.compiled = self.compiled.replace("#style#", "")

    def __removeComments(self, code):
        return(re.sub(r"%%.*\n", "%%", code))

    def __removeNewLines(self, code):
        return(code.replace("\n", ""))

    def __joinLines(self, code):
        return("\n".join(code))

    def __compile(self, line):
        """
        mainCommands={
            "basics": ["author", "language", "charset", "palette"] ,
            "keywords": [],
            "description": [],
            "title": []
        } """
        import SyntaxList

        self.__mainCommands = SyntaxList.SyntaxList()


        line=line.strip()
        line=self.__Command_and_Argument(line)

        if line[0] not in self.__mainCommands.getKeys():
            self.__error = self.__dicts.getWordFromDict(
                           self.__Config.get_Element("Language"), "errorInvalidCommand").replace("#line#", line[0])


        else:
            args=line[1][1:-1]
            if line[0] == "keywords":
                self.__keywords = args
            elif line[0] == "description":
                self.__description = args
            elif line[0] == "title":
                self.__title = args
            elif line[0] == "basics":
                args = self.__splitComma(args)
                for arg in args:
                    Key = arg.split("=",1)[0].strip()
                    Value = arg.split("=",1)[1].strip()
                    self.__checkInvalidKey(Key, line[0])
                    if Key == "author":
                        self.__author = Value
                    elif Key == "language":
                        self.__lang = Value
                    elif Key == "charset":
                        self.__charset = Value
                    elif Key == "palette":
                        if Value not in self.__Colors.getColors():
                            try:
                                num=int(Value)
                                Value=list(self.__Colors.getColors())[num]
                            except:
                                self.__error = self.__dicts.getWordFromDict(
                                               self.__Config.get_Element("Language"), "errorColorPalette").replace("#Value#", Value)
                        if self.__error==False:
                            self.__cssTemplateChanged=True
                        self.__palette = Value
            elif line[0] == "background":


                if args.startswith("color"):
                    self.__background = "background-color: #Color1#"

                elif args.startswith("gradient"):
                    self.__background = "background-image: linear-gradient(#Data#)"
                    try:
                        args = args.split("=", 1)[1]
                        if args == "HOR":
                            data = "to right, "
                        elif args == "VER":
                            data = ""
                        elif args == "DIG":
                            data = "to bottom right, "
                        else:
                            self.__argumentError(args, "background")

                        data = data + "#Color1#, #Color2#, #Color1#"

                        self.__background = self.__background.replace("#Data#", data)

                    except:
                        self.__argumentError(args, "background")

                elif args.startswith("image"):
                    args=self.__splitComma(args.split("=",1)[1])
                    if len(args) == 1:
                        args.append("cover")

                    self.__background = "background-image: url('"+ args[0] +"');"+os.linesep
                    self.__background = self.__background + "\tbackground-repeat: no-repeat;" + os.linesep \
                                        + "\tbackground-attachment: fixed;" + os.linesep \
                                        + "\tbackground-size: " + args[1]


                else:
                    self.__argumentError(args, "background")

            elif line[0] == "banner":
                self.__bannerTemplateChanged = True

                self.__splitComma(args)
                args = self.__splitComma(args)
                self.__bannerSize="cover"
                self.__bannerTextSize="3em"
                self.__bannerTextAlign="center"
                self.__bannerData=""
                self.__bannerAnimation=""
                self.__bannerHeight = 200
                self.__bannerCSS = open("templates/BannerCSSTemplate.txt").read()

                for subArg in args:
                    subArg=subArg.strip()
                    subArgs = subArg.split("=", 1)
                    if subArg.startswith("image"):
                        self.__bannerData += "\tbackground-image: url('"+ subArgs[1] +"');"+os.linesep
                        self.__bannerData += "\tbackground-repeat: no-repeat;" + os.linesep \
                                            + "\tbackground-attachment: fixed;" + os.linesep
                    elif subArg.startswith("size"):
                        self.__bannerSize=subArgs[1]

                    elif subArg.startswith("text"):
                        textstuff = self.__splitComma(self.__Command_and_Argument(args[1])[1][1:-1])
                        self.__bannerText=textstuff[0][1:-1]
                        self.__bannerTextSize=textstuff[1]
                        self.__bannerTextAlign = textstuff[2]

                    elif subArg.startswith("animation"):
                        self.__bannerAnimation = open("templates/bannerAnimationTemplate.txt").read()
                        animpart = "\t\t#number#%{	background-image: url('#img#');	}" + os.linesep

                        __replacer = ""

                        stuff = self.__Command_and_Argument(subArg)[1][1:-1]
                        stuff = self.__splitComma(stuff)
                        self.__time=stuff[0]
                        move = (100//(len(stuff)-1))//10
                        still = 100//(len(stuff)-1) - move
                        number = 0

                        for imageNum in range(1, len(stuff)):
                            __replacer+=animpart.replace("#number#", str(number)).replace("#img#", stuff[imageNum])
                            number+=still
                            __replacer+=animpart.replace("#number#", str(number)).replace("#img#", stuff[imageNum])
                            number+=move

                        __replacer+=animpart.replace("#number#", "100").replace("#img#", stuff[1])

                        self.__bannerAnimation = self.__bannerAnimation.replace("#animationThings#", __replacer)

                    elif subArg.startswith("height"):
                        self.__bannerHeight=subArgs[1]

                    else:
                        self.__argumentError(subArg, "banner")

                self.__bannerData += "\tdisplay: flex;" + os.linesep
                self.__bannerData += "\talign-items: flex-end;" + os.linesep

                self.__bannerData += "\tbackground-size: "+self.__bannerSize+";" + os.linesep
                self.__bannerData += "\tfont-size: " + self.__bannerTextSize +";" +os.linesep
                self.__bannerData += "\tjustify-content: "+self.__bannerTextAlign.replace("left", "flex-start").replace("right", "flex-end") +";" +os.linesep
                self.__bannerData += "\theight: "+self.__bannerHeight +"px;" +os.linesep
                self.__bannerData += "\tvertical-align: bottom;"+os.linesep
                self.__bannerData += "\tbackground-position-x: center;"+os.linesep
                self.__bannerData += "\tmargin-left: auto;"+os.linesep
                self.__bannerData += "\tmargin-right: auto;"+os.linesep
                self.__bannerData += "\tborder-radius: 15px 15px 0px 0px;"+os.linesep
                self.__bannerData += "\ttext-shadow: #Color1# 10px 10px 10px;"+os.linesep



                if self.__bannerAnimation!="":
                    self.__bannerData += "\tanimation-name: bannerAnimation;"+os.linesep
                    self.__bannerData += "\tanimation-duration: " + self.__time + ";"+os.linesep
                    self.__bannerData += "\tanimation-timing-function: ease-in-out;"+os.linesep
                    self.__bannerData += "\tanimation-iteration-count: infinite;"+os.linesep



                self.__bannerCSS = self.__bannerCSS.replace("#bannerData#", self.__bannerData)
                self.__bannerCSS = self.__bannerCSS.replace("#BannerAnimation#", self.__bannerAnimation)


    def __argumentError(self, Key, All):
        self.__error = self.__dicts.getWordFromDict(
            self.__Config.get_Element("Language"), "errorInvalidArgument").replace("#Key#",
                                                                                   Key).replace(
            "#All#", All)

    def __Command_and_Argument(self, line):
        return(line.split("(",1)[0], line.replace(line.split("(",1)[0], ""))

    def __splitComma(self, line):
        listOfArgs=[]
        lines2 = []
        lines = line.split(",")
        tempstring=""
        merge = False
        for item in lines:
            item=item.strip()
            tempstring +=item

            for char in item:
                if char == '"':
                    merge = not merge
            if merge == False:
                lines2.append(tempstring)
                tempstring=""
            else:
                tempstring+=","

        tempstring=""

        for item in lines2:
            item=item.strip()
            tempstring +=item
            for char in item:
                if char == '(':
                    merge=True
                elif char == ')':
                    merge =False


            if merge == False:
                listOfArgs.append(tempstring)
                tempstring = ""
            else:
                tempstring += ","

        return(listOfArgs)

    def __checkInvalidKey(self, Key, All):
        if Key not in self.__mainCommands.getValueOfKey(All):
            self.__argumentError(Key, All)

    def __addColors(self):
        for number in range(0,4):
            if self.__palette!="":
                self.compiled = self.compiled.replace("#Color"+str(number+1)+"#", self.__Colors.getPalette(self.__palette)[number])


class Compiler(Compiler_REAL):

    def __init__(self, code, config, dicts):
        return(super().__init__(code, config, dicts))