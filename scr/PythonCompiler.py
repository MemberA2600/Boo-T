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
        self.__fontfamily='"Arial"'

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
        self.__navBarCSS = ""
        self.__footerCSS = ""
        self.__navbarOpacity = 1.0
        self.__tableOpacity = 1.0
        self.__rowOpacity = 1.0
        self.__footerOpacity = 1.0


        self.__mainBody=""
        self.__tableCSS = ""
        self.__rowCSS = ""


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
        self.compiled = self.compiled.replace("#navBarCSS#", self.__navBarCSS)
        self.compiled = self.compiled.replace("#bannertext#", self.__bannerText)
        self.compiled = self.compiled.replace("#font#", self.__fontfamily)
        self.compiled = self.compiled.replace("#tableCSS#", self.__tableCSS)
        self.compiled = self.compiled.replace("#rowCSS#", self.__rowCSS)
        self.compiled = self.compiled.replace("#body#", self.__mainBody)
        self.compiled = self.compiled.replace("#footerCSS#", self.__footerCSS)


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

            self.compiled = self.compiled.replace("#font#", self.__fontfamily)


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
            elif line[0] == "font-family":
                self.__fontfamily = args
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
                                if Value == "random":
                                    import random
                                    import datetime
                                    random.seed(int(str(datetime.datetime.now()).split(".")[1]))

                                    num = random.randint(0,27)
                                else:
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

                args = self.__splitComma(args)
                self.__bannerSize="cover"
                self.__bannerTextSize="3em"
                self.__bannerTextAlign="center"
                self.__bannerData=""
                self.__bannerTextData=""
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
                        #animpart = "\t\t#number#%{	background-image: url('#img#');	}" + os.linesep

                        __replacer = ""

                        stuff = self.__Command_and_Argument(subArg)[1][1:-1]
                        stuff = self.__splitComma(stuff)
                        self.__time=stuff[0]
                        move = (100//(len(stuff)-1))//10
                        still = 100//(len(stuff)-1) - move
                        number = 0

                        """
                        for imageNum in range(1, len(stuff)):
                            __replacer+=animpart.replace("#number#", str(number)).replace("#img#", stuff[imageNum])
                            number+=still
                            __replacer+=animpart.replace("#number#", str(number)).replace("#img#", stuff[imageNum])
                            number+=move

                        __replacer+=animpart.replace("#number#", "100").replace("#img#", stuff[1])
                        """
                        animpart = "\t\t#number#%{	background-image: url('#img#');	filter: saturate(#sat#) blur(#blur#px) ;}" + os.linesep


                        for imageNum in range(1, len(stuff)):
                            __replacer+=animpart.replace("#number#", str(number)).replace("#img#", stuff[imageNum]).replace("#blur#", "3").replace("#sat#", "0.25")
                            __replacer+=animpart.replace("#number#", str(number+move)).replace("#img#", stuff[imageNum]).replace("#blur#", "0").replace("#sat#", "1")

                            number+=still

                            __replacer+=animpart.replace("#number#", str(number-move)).replace("#img#", stuff[imageNum]).replace("#blur#", "0").replace("#sat#", "1")
                            __replacer+=animpart.replace("#number#", str(number)).replace("#img#", stuff[imageNum]).replace("#blur#", "3").replace("#sat#", "0.25")
                            number+=move

                        __replacer+=animpart.replace("#number#", "100").replace("#img#", stuff[1]).replace("#blur#", "3").replace("#sat#", "0.25")



                        self.__bannerAnimation = self.__bannerAnimation.replace("#animationThings#", __replacer)

                    elif subArg.startswith("height"):
                        self.__bannerHeight=subArgs[1]

                    else:
                        self.__argumentError(subArg, "banner")

                self.__bannerData += "\tdisplay: flex;" + os.linesep
                self.__bannerData += "\talign-items: flex-end;" + os.linesep

                self.__bannerTextData += "\tdisplay: flex;" + os.linesep
                self.__bannerTextData += "\talign-items: flex-end;" + os.linesep

                self.__bannerData += "\tbackground-size: "+self.__bannerSize+";" + os.linesep
                self.__bannerTextData += "\tfont-size: " + self.__bannerTextSize +";" +os.linesep
                self.__bannerTextData += "\tjustify-content: "+self.__bannerTextAlign.replace("left", "flex-start").replace("right", "flex-end") +";" +os.linesep
                self.__bannerData += "\theight: "+self.__bannerHeight +"px;" +os.linesep
                self.__bannerTextData += "\theight: 0px;" +os.linesep

                self.__bannerData += "\tvertical-align: bottom;"+os.linesep
                self.__bannerTextData += "\tvertical-align: bottom;"+os.linesep

                self.__bannerData += "\tbackground-position-x: center;"+os.linesep
                self.__bannerData += "\tbackground-position-y: center;"+os.linesep

                self.__bannerData += "\tmargin-left: auto;"+os.linesep
                self.__bannerData += "\tmargin-right: auto;"+os.linesep
                self.__bannerData += "\tborder-radius: 15px 15px 0px 0px;"+os.linesep
                self.__bannerTextData += "\ttext-shadow: #Color1# 5px 5px 5px;"+os.linesep
                self.__bannerTextData += "\tpadding-bottom: "+self.__bannerHeight +"px;" +os.linesep
                self.__bannerTextData += "\tmargin-bottom: -"+self.__bannerHeight +"px;" +os.linesep


                if self.__bannerAnimation!="":
                    self.__bannerData += "\tanimation-name: bannerAnimation;"+os.linesep
                    self.__bannerData += "\tanimation-duration: " + self.__time + ";"+os.linesep
                    self.__bannerData += "\tanimation-timing-function: ease-in-out;"+os.linesep
                    self.__bannerData += "\tanimation-iteration-count: infinite;"+os.linesep



                self.__bannerCSS = self.__bannerCSS.replace("#bannerData#", self.__bannerData).replace("#bannerTextData#", self.__bannerTextData)
                self.__bannerCSS = self.__bannerCSS.replace("#BannerAnimation#", self.__bannerAnimation)

            elif line[0] == "navbar":
                self.__navBarTemplateChanged = True
                __brandName = "Brand"
                __items = []
                __sticky = ""

                args = self.__splitComma(args)
                self.__navBarCSS = open("templates/NavBarCSSTemplate.txt").read()
                self.__navItemTemplate = open("templates/NavItemTemplate.txt").read()
                for item in args:
                    if item.startswith("brand"):
                        inside=self.__Command_and_Argument(item)[1][1:-1]
                        if inside.startswith('"'):
                            __brandName = inside[1:-1]
                        else:
                            url=inside.split("=")[1]
                            __brandName = "<img class='img-fluid' target='_blank' src='" + url +  "'>"
                    elif item.startswith("opacity"):
                        self.__navbarOpacity=float(item.split("=")[1])

                    elif item.startswith("item"):
                        subargs = self.__splitComma(self.__Command_and_Argument(item)[1][1:-1])
                        temp = self.__navItemTemplate
                        temp=temp.replace("#text#", subargs[0][1:-1]).replace("#link#", str("#"+subargs[1]))
                        __items.append(temp)

                    elif item=="sticky":
                        __sticky="sticky-top"

                    else:
                        self.__argumentError(item, "navbar")

                if self.__navbarOpacity!=1:
                    self.__navBarTemplate = self.__navBarTemplate.replace("#Color2#", "#NavbarOpacityColor2#")

                self.__navBarTemplate=self.__navBarTemplate.replace("#brand#", __brandName).replace("#navItems#", os.linesep.join(__items)).replace("#sticky#", __sticky)

            elif line[0] == "table":
                self.__containerTemplateChanged = True
                __tableTemplate = open("templates/TableTemplate.txt").read()
                __headTemplate = "\t\t\t\t<th scope='col'>#column#</th>"
                self.__tableCSS = open("templates/TableCSSTemplate.txt").read()
                tempcolumns = []
                temprows = []
                __dark=""
                __id=""

                args = self.__splitComma(args)
                for item in args:
                    if item.startswith("opacity"):
                        self.__tableOpacity = float(item.split("=")[1])
                    elif item=="inverted":
                        __dark = "table-dark"
                    elif item.startswith("id"):
                        __id = item.split("=")[1]
                    elif item.startswith("columns"):
                        columns = self.__Command_and_Argument(item)[1][1:-1]
                        for column in self.__splitComma(columns):
                            tempcolumns.append(__headTemplate.replace("#column#", column[1:-1]))
                    elif item.startswith("row"):
                        row = self.__Command_and_Argument(item)[1][1:-1]
                        temprow = []
                        temprow_string="\t\t\t<tr>" + os.linesep
                        for r in self.__splitComma(row):
                            temprow.append(r[1:-1])

                        for num in range(0, len(temprow)):
                            if num == 0:
                                temprow_string+=str("\t\t\t\t<th scope='row'>#value#</th>" + os.linesep).replace("#value#", temprow[0])
                            else:
                                temprow_string+=str("\t\t\t\t<td>#value#</td>" + os.linesep).replace("#value#", temprow[num])
                        temprow_string+="\t\t\t</tr>" + os.linesep
                        temprows.append(temprow_string)

                    else:
                        self.__argumentError(item, "table")

                __tableTemplate=__tableTemplate.replace("#headItems#", os.linesep.join(tempcolumns)).replace("#rowItems#", os.linesep.join(temprows)).replace("#dark#", __dark).replace("#id#", str("id='"+__id+"'"))

                self.__mainBody+=__tableTemplate

                if self.__tableOpacity!=1.0:
                    self.__tableCSS =self.__tableCSS.replace("Color2", "TableOpacityColor2")
            elif line[0] == "row":
                self.__containerTemplateChanged = True
                __rowTemplate = open("templates/RowTemplate.txt").read()
                __rowItemTemplate = open("templates/RowItemTemplate.txt").read()
                __articleTemplate = open("templates/ArticleTemplate.txt").read()
                self.__rowCSS = open("templates/RowCSSTemplate.txt").read()
                __id=""
                __rates= []
                __rowItems=[]
                __titleAlign="center"
                __imgfilter=""

                args = self.__splitComma(args)
                for item in args:
                    if item.startswith("opacity"):
                        self.__rowOpacity = float(item.split("=")[1])
                    elif item.startswith("id"):
                        __id = item.split("=")[1]
                    elif item.startswith("rate"):
                        __rates = self.__splitComma(self.__Command_and_Argument(item)[1][1:-1])
                        sum=0
                        for number in __rates:
                            sum+=int(number)
                        if sum!=12:
                            self.__error = self.__dicts.getWordFromDict(
                                self.__Config.get_Element("Language"), "errorNot12")

                    elif item.startswith("image"):
                        __image = str("\t\t\t\t<a href='"+item.split("=")[1]+"'><img class='img-fluid #filter#' src='"+item.split("=")[1] + "'></a>")
                        __rowItems.append(__rowItemTemplate.replace("#number#", __rates[len(__rowItems)]).replace("#data#", __image))

                    elif item.strip()=="imgfilter":
                        __imgfilter="img-animate"

                    elif item.startswith("article"):
                        __article=__articleTemplate
                        __title=""
                        __text=""
                        for ehhh in self.__splitComma(self.__Command_and_Argument(item)[1][1:-1]):
                            if ehhh.startswith("title-align"):
                                __titleAlign = ehhh.split("=")[1]

                            elif ehhh.startswith("title"):
                                __title = ehhh.split("=")[1][1:-1]

                            elif ehhh.startswith("rawtext"):
                                __text = ehhh.split("=")[1][1:-1]

                            else:
                                self.__argumentError(item, "artitle")

                        __article = __article.replace("#title#", __title).replace("#text#", __text).replace("#align#", __titleAlign)
                        __rowItems.append(__rowItemTemplate.replace("#number#", __rates[len(__rowItems)]).replace("#data#", __article))
                    else:
                        self.__argumentError(item, "row")

                if len(__rowItems)!=len(__rates):
                    self.__error = self.__dicts.getWordFromDict(
                        self.__Config.get_Element("Language"), "errorNoMatch")

                __rowTemplate = __rowTemplate.replace("#rowitems#", os.linesep.join(__rowItems)).replace("#id#", str("id='"+__id+"'"))
                __rowTemplate = __rowTemplate.replace("#filter#", __imgfilter)
                self.__mainBody+=__rowTemplate

                if self.__tableOpacity!=1.0:
                    self.__rowCSS =self.__rowCSS.replace("Color2", "RowOpacityColor2")
            elif line[0]=="footer":
                self.__footerTemplateChanged = True
                self.__footerCSS = open("templates/FooterCSSTemplate.txt").read()
                __footerData = ""
                __buttonText = "Go to Top"
                __socials = {}
                __icons = []

                __id=""
                args = self.__splitComma(args)
                for item in args:
                    if item.startswith("opacity"):
                        self.__footerOpacity = float(item.split("=")[1])
                    elif item.startswith("id"):
                        __id = item.split("=")[1]
                    elif item.startswith("button"):
                        __buttonText = item.split("=")[1][1:-1].strip()
                    elif item.startswith("facebook"):
                        __socials["facebook"] = item.split("=")[1].strip()
                    elif item.startswith("youtube"):
                        __socials["youtube"] = item.split("=")[1].strip()
                    elif item.startswith("twitter"):
                        __socials["twitter"] = item.split("=")[1].strip()
                    elif item.startswith("vkontakte"):
                        __socials["vkontakte"] = item.split("=")[1].strip()
                    elif item.startswith("instagram"):
                        __socials["instagram"] = item.split("=")[1].strip()
                    elif item.startswith("googleplus"):
                        __socials["googleplus"] = item.split("=")[1].strip()
                    elif item.startswith("linkedin"):
                        __socials["linkedin"] = item.split("=")[1].strip()
                    elif item.startswith("github"):
                        __socials["github"] = item.split("=")[1].strip()
                    else:
                        self.__argumentError(item, "footer")

                if "facebook" in __socials.keys():
                    __icons.append(str("\t\t\t<div class='col-3 col-md'>"+os.linesep+"\t\t\t\t<a  href='" + __socials["facebook"] + "' target='_blank'><img src='img/facebook.png' class='img-fluid'></a>"+os.linesep+"</div>" ))
                if "youtube" in __socials.keys():
                    __icons.append(str("\t\t\t<div class='col-3 col-md'>"+os.linesep+"\t\t\t\t<a  href='" + __socials["youtube"] + "' target='_blank'><img src='img/youtube.png' class='img-fluid'></a>"+os.linesep+"</div>" ))
                if "twitter" in __socials.keys():
                    __icons.append(str("\t\t\t<div class='col-3 col-md'>"+os.linesep+"\t\t\t\t<a  href='" + __socials["twitter"] + "' target='_blank'><img src='img/twitter.png' class='img-fluid'></a>"+os.linesep+"</div>" ))
                if "vkontakte" in __socials.keys():
                    __icons.append(str("\t\t\t<div class='col-3 col-md'>"+os.linesep+"\t\t\t\t<a  href='" + __socials["vkontakte"] + "' target='_blank'><img src='img/vk.png' class='img-fluid'></a>"+os.linesep+"</div>" ))
                if "instagram" in __socials.keys():
                    __icons.append(str("\t\t\t<div class='col-3 col-md'>"+os.linesep+"\t\t\t\t<a  href='" + __socials["instagram"] + "' target='_blank'><img src='img/instagram.png' class='img-fluid'></a>"+os.linesep+"</div>" ))
                if "googleplus" in __socials.keys():
                    __icons.append(str("\t\t\t<div class='col-3 col-md'>"+os.linesep+"\t\t\t\t<a  href='" + __socials["googleplus"] + "' target='_blank'><img src='img/google-plus.png' class='img-fluid'></a>"+os.linesep+"</div>" ))
                if "linkedin" in __socials.keys():
                    __icons.append(str("\t\t\t<div class='col-3 col-md'>"+os.linesep+"\t\t\t\t<a  href='" + __socials["linkedin"] + "' target='_blank'><img src='img/linkedin.png' class='img-fluid'></a>"+os.linesep+"</div>" ))
                if "github" in __socials.keys():
                    __icons.append(str("\t\t\t<div class='col-3 col-md'>"+os.linesep+"\t\t\t\t<a  href='" + __socials["github"] + "' target='_blank'><img src='img/github.png' class='img-fluid'></a>"+os.linesep+"</div>" ))

                import datetime
                self.__footerTemplate = self.__footerTemplate.replace("#ButtonText#", __buttonText).replace("#id#", str("id='"+__id+"'")).replace("#year#", str(datetime.datetime.now()).split("-")[0]).replace("#icons#", os.linesep.join(__icons))

                if self.__footerOpacity!=1.0:
                    self.__footerCSS =self.__footerCSS.replace("Color2", "FooterOpacityColor2")

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
                self.compiled = self.compiled.replace("#NavbarOpacityColor"+str(number+1)+"#", str("rgba(" + self.__Colors.getRGBA(self.__Colors.getPalette(self.__palette)[number]) + "," + str(self.__navbarOpacity) + ")"))
                self.compiled = self.compiled.replace("#TableOpacityColor"+str(number+1)+"#", str("rgba(" + self.__Colors.getRGBA(self.__Colors.getPalette(self.__palette)[number]) + "," + str(self.__tableOpacity) + ")"))
                self.compiled = self.compiled.replace("#RowOpacityColor"+str(number+1)+"#", str("rgba(" + self.__Colors.getRGBA(self.__Colors.getPalette(self.__palette)[number]) + "," + str(self.__tableOpacity) + ")"))
                self.compiled = self.compiled.replace("#FooterOpacityColor"+str(number+1)+"#", str("rgba(" + self.__Colors.getRGBA(self.__Colors.getPalette(self.__palette)[number]) + "," + str(self.__footerOpacity) + ")"))


class Compiler(Compiler_REAL):

    def __init__(self, code, config, dicts):
        return(super().__init__(code, config, dicts))