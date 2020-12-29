from abc import *
import re

class Compiler_REAL(ABC):

    @abstractmethod
    def __init__(self, code):

        """Basic Variables"""
        self.__author=""
        self.__title=""
        self.__lang=""
        self.__description=""
        self.__charset=""
        self.__keywords=""
        self.__palette=""

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
        self.__mainTemplate=open("default/MainTemplate.txt", "r").read()
        self.__mainTemplateChanged = False
        self.__bannerTemplate=open("default/BannerTemplate.txt", "r").read()
        self.__bannerTemplateChanged = False
        self.__navBarTemplate=open("default/NavBarTemplate.txt", "r").read()
        self.__navBarTemplateChanged = False
        self.__footerTemplate=open("default/FooterTemplate.txt", "r").read()
        self.__footerTemplateChanged = False
        self.__containerTemplate=open("default/ContainerTemplate.txt", "r").read()
        self.__containerTemplateChanged = False
        self.__cssTemplate=open("default/CSSTemplate.txt", "r").read()
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

    def __createCompiled(self):
        if self.__error!=False:
            self.compiled = self.__error + " at valid line " + str(self.__number) + "!"
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
                self.compiled = self.compiled.replace("#style#", open("default/DefaultCSS.txt", "r").read())

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
            self.__error = "Invalid Command ("+line[0]+")"
        else:
            args=line[1][1:-1]
            if line[0] == "keywords":
                self.__keywords = args
            elif line[0] == "description":
                self.__description = args
            elif line[0] == "title":
                self.__title = args
            elif line[0] == "basics":
                args = args.split(",")
                for arg in args:
                    Key = arg.split("=")[0].strip()
                    Value = arg.split("=")[1].strip()
                    self.__checkInvalidKey(Key, line[0])
                    if Key == "author":
                        self.__author = Value
                    elif Key == "language":
                        self.__lang = Value
                    elif Key == "charset":
                        self.__charset = Value
                    elif Key == "palette":
                        self.__palette = Value


    def __Command_and_Argument(self, line):
        return(line.split("(")[0], line.replace(line.split("(")[0], ""))

    def __checkInvalidKey(self, Key, All):
        if Key not in self.__mainCommands.getValueOfKey(All):
            self.__error = "Invalid Argument (" + Key + ") for '" + All +"'"

class Compiler(Compiler_REAL):

    def __init__(self, code):
        return(super().__init__(code))