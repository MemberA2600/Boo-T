import re
import os

class Compiler():

    def __init__(self, code, config, dicts, syntax, master):

        import ColorPalettes
        self.__Colors = ColorPalettes.ColorPalettes()
        self.__Config=config
        self.__dicts=dicts
        self.__Syntax = syntax

        self.__master = master

        """Basic Variables"""
        self.__author=""
        self.__title=""
        self.__description=""
        self.__keywords=""
        self.__background = ""
        self.__bannerText = ""
        self.__bannerCSS = ""
        self.__navBarCSS = ""
        self.__footerCSS = ""
        self.__navbarOpacity = 1.0
        self.__tableOpacity = 1.0
        self.__rowOpacity = 1.0
        self.__footerOpacity = 1.0

        self.__fontfamily='"Arial"'
        self.__lang="en"
        self.__charset="UTF-8"
        self.__palette="black"

        self.__mainBody=""
        self.__tableCSS = ""
        self.__rowCSS = ""

        """Formatting the code, getting the full, perfect lines before reading it"""
        code = self.__removeComments(code)
        code = self.__removeNewLines(code)
        code = self.__spaceTags(code)

        code=code.split(self.__master.getDeliminator())
        try:
            code.remove("")
        except:
            #If there are no blank lines...
            pass

        """Load_Templates"""
        self.__mainTemplate= self.__templateLoader("MainTemplate")
        self.__mainTemplateChanged = False
        self.__bannerTemplate=self.__templateLoader("BannerTemplate")
        self.__bannerTemplateChanged = False
        self.__navBarTemplate=self.__templateLoader("NavBarTemplate")
        self.__navBarTemplateChanged = False
        self.__footerTemplate=self.__templateLoader("FooterTemplate")
        self.__footerTemplateChanged = False
        self.__containerTemplate=self.__templateLoader("ContainerTemplate")
        self.__containerTemplateChanged = False
        self.__cssTemplate=self.__templateLoader("CSSTemplate")
        self.__cssTemplateChanged = False


        """Compile Line-By-Line, if there is a compile error, puts message at end and sets string"""
        self.compiled = ""
        self.__error=False

        self.__number = 0
        for line in code:
            self.__number+=1
            """Don't compile empty lines."""
            if re.findall(r"[a-zA-Z]", line)!=[]:
                try:
                    self.__compile(line)
                except Exception as e:
                    self.__error = self.__dicts.getWordFromDict(
                        self.__Config.get_Element("Language"), "syntaxError").replace("#python#",str(e))

            if self.__error!=False:
                break

        self.__createCompiled()
        if self.__error==False:
            self.__replaceCompiled()
            self.__addColors()


    def __replaceCompiled(self):
        self.__compiledReplacer("#background#", self.__background)
        self.__compiledReplacer("#bannerCSS#", self.__bannerCSS)
        self.__compiledReplacer("#navBarCSS#", self.__navBarCSS)
        self.__compiledReplacer("#bannertext#", self.__bannerText)
        self.__compiledReplacer("#font#", self.__fontfamily)
        self.__compiledReplacer("#tableCSS#", self.__tableCSS)
        self.__compiledReplacer("#rowCSS#", self.__rowCSS)
        self.__compiledReplacer("#body#", self.__mainBody)
        self.__compiledReplacer("#footerCSS#", self.__footerCSS)

    def __compiledReplacer(self, s, var):
        self.compiled=self.compiled.replace(s, var)

    def __createCompiled(self):
        if self.__error!=False:
            self.compiled = self.__dicts.getWordFromDict(
                self.__Config.get_Element("Language"), "errorBasic").replace("#error#", self.__error).replace("#number#", str(self.__number))
        else:
            self.compiled = self.__mainTemplate

            self.__compiledReplacer("#author#", self.__author)
            self.__compiledReplacer("#title#", self.__title)
            self.__compiledReplacer("#lang#", self.__lang)
            self.__compiledReplacer("#description#", self.__description)
            self.__compiledReplacer("#charset#", self.__charset)
            self.__compiledReplacer("#keywords#", self.__keywords)

            self.__templateChanged(self.__bannerTemplateChanged, "#Banner#", self.__bannerTemplate)
            self.__templateChanged(self.__navBarTemplateChanged, "#NavBar#", self.__navBarTemplate)
            self.__templateChanged(self.__containerTemplateChanged, "#Container#", self.__containerTemplate)
            self.__templateChanged(self.__footerTemplateChanged, "#Footer#", self.__footerTemplate)
            self.__templateChanged(self.__cssTemplateChanged, "#style#", self.__cssTemplate)

            self.__compiledReplacer("#font#", self.__fontfamily)

    def __templateChanged(self, var, s, changeTo):
        if var == True:
            self.__compiledReplacer(s, changeTo)
        else:
            self.__compiledReplacer(s, "")

    def __removeComments(self, code):
        return(re.sub(rf"{self.__master.getDeliminator()}.*\n", self.__master.getDeliminator(), code))

    def __removeNewLines(self, code):
        return(code.replace("\n", ""))

    def __joinLines(self, code):
        return("\n".join(code))

    def __compile(self, line):
        line=line.strip()
        line=self.__Command_and_Argument(line)


        if line[0] not in self.__Syntax.getKeys():
            """If the main command is invalid, raise error."""
            self.__error = self.__dicts.getWordFromDict(
                           self.__Config.get_Element("Language"), "errorInvalidCommand").replace("#line#", line[0])

        else:
            """Setting the most basic things in the first 5 cases for HTML header."""
            args=line[1][1:-1]
            if line[0] == "keywords":
                self.__keywords = args
            elif line[0] == "deliminator":
                if self.__number>1:
                    self.__error = self.__dicts.getWordFromDict(
                        self.__Config.get_Element("Language"), "deliminatorNoFirstLineError")

            elif line[0] == "opacity":
                args = self.__splitComma(args)
                for arg in args:
                    Key = self.__splitByEQ(arg, 0)
                    Value = self.__splitByEQ(arg, 1)

                    if Key=="container":
                        self.__rowOpacity=float(Value)
                    elif Key == "navbar":
                        self.__navbarOpacity = float(Value)
                    elif Key == "table":
                        self.__tableOpacity = float(Value)
                    elif Key == "footer":
                        self.__footerOpacity = float(Value)
                    else:
                        self.__argumentError(args, "opacity")


            elif line[0] == "description":
                self.__description = args
            elif line[0] == "font-family":
                self.__fontfamily = args
            elif line[0] == "title":
                self.__title = args
            elif line[0] == "basics":
                """Sets author, language, charset and palette. Palette can be the name of palette or a number between 0-27, 
                or random, which generates a random palette number every time."""

                args = self.__splitComma(args)
                for arg in args:
                    Key = self.__splitByEQ(arg, 0)
                    Value = self.__splitByEQ(arg, 1)
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
                                    try:
                                        random.seed(int(str(datetime.datetime.now()).split(".")[1]))
                                    except:
                                        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
                                        import pygame.mouse as M
                                        random.seed(M.get_pos()[0] + M.get_pos()[1])
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
                    else:
                        self.__argumentError(args, "basics")

            elif line[0] == "background":
                "Settings of global background for the whole site."

                if args.startswith("color"):
                    self.__background = "background-color: #Color1#"

                elif args.startswith("gradient"):
                    self.__background = "background-image: linear-gradient(#Data#)"
                    try:
                        args = self.__splitByEQ(args, 1)
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
                    args=self.__splitComma(self.__splitByEQ(args, 1))
                    if len(args) == 1:
                        args.append("cover")
                    self.__background = self.__setBackGroundData(args, 0) \
                                        + "\tbackground-size: " + args[1]


                else:
                    self.__argumentError(args, "background")

            elif line[0] == "banner":
                "Settings for the banner."
                if self.__bannerTemplateChanged==False:
                    self.__bannerTemplateChanged = True
                else:
                    self.__canBeOnlySetOnceError(line[0])


                args = self.__splitComma(args)
                self.__bannerSize="cover"
                self.__bannerTextSize="3em"
                self.__bannerTextAlign="center"
                self.__bannerData=""
                self.__bannerTextData=""
                self.__bannerAnimation=""
                self.__bannerHeight = 200
                self.__bannerCSS = self.__templateLoader("BannerCSSTemplate")

                for subArg in args:
                    subArg=subArg.strip()
                    if subArg.startswith("image"):
                        subArgs = subArg.split("=", 1)
                        self.__bannerData += self.__setBackGroundData(subArgs, 1)

                    elif subArg.startswith("size"):
                        subArgs = subArg.split("=", 1)
                        self.__bannerSize=subArgs[1]

                    elif subArg.startswith("text"):
                        textstuff = self.__splitComma(self.__Command_and_Argument(subArg)[1][1:-1])

                        self.__bannerText=textstuff[0][1:-1]
                        self.__bannerTextSize=textstuff[1]
                        self.__bannerTextAlign = textstuff[2]

                    elif subArg.startswith("animation"):
                        self.__bannerAnimation = self.__templateLoader("bannerAnimationTemplate")
                        __replacer = ""

                        stuff = self.__Command_and_Argument(subArg)[1][1:-1]
                        stuff = self.__splitComma(stuff)
                        self.__time=stuff[0]
                        move = (100//(len(stuff)-1))//10
                        still = 100//(len(stuff)-1) - move
                        number = 0

                        animpart = "\t\t#number#%{	background-image: url('#img#');	filter: saturate(#sat#) blur(#blur#px) ;}" + os.linesep

                        for imageNum in range(1, len(stuff)):
                            __replacer += self.__animPartMaker(animpart, str(number), stuff[imageNum], "3", "0.25")
                            __replacer += self.__animPartMaker(animpart, str(number+move), stuff[imageNum], "0", "1")

                            number+=still

                            __replacer += self.__animPartMaker(animpart, str(number-move), stuff[imageNum], "0", "1")
                            __replacer += self.__animPartMaker(animpart, str(number), stuff[imageNum], "3", "0.25")

                            number+=move

                        __replacer+=animpart.replace("#number#", "100").replace("#img#", stuff[1]).replace("#blur#", "3").replace("#sat#", "0.25")
                        self.__bannerAnimation = self.__bannerAnimation.replace("#animationThings#", __replacer)

                    elif subArg.startswith("height"):
                        subArgs = subArg.split("=", 1)
                        self.__bannerHeight=subArgs[1]
                    else:
                        self.__argumentError(subArg, "banner")

                self.__bannerData += self.__basicCSS(str(self.__bannerHeight)) \
                                    + "\tbackground-size: "+self.__bannerSize+";" + os.linesep \
                                    + "\tbackground-position-x: center;"+os.linesep \
                                    + "\tbackground-position-y: center;"+os.linesep \
                                    + "\tmargin-left: auto;"+os.linesep \
                                    + "\tmargin-right: auto;"+os.linesep \
                                    + "\tborder-radius: 15px 15px 0px 0px;"+os.linesep

                if self.__bannerAnimation!="":
                    self.__bannerData += "\tanimation-name: bannerAnimation;"+os.linesep \
                                        + "\tanimation-duration: " + self.__time + ";"+os.linesep \
                                        + "\tanimation-timing-function: ease-in-out;"+os.linesep \
                                        + "\tanimation-iteration-count: infinite;"+os.linesep

                self.__bannerTextData += self.__basicCSS("0") \
                                        + "\tfont-size: " + self.__bannerTextSize +";" +os.linesep \
                                        + "\tjustify-content: "+self.__bannerTextAlign.replace("left", "flex-start").replace("right", "flex-end") +";" +os.linesep \
                                        + "\ttext-shadow: #Color1# 5px 5px 5px;"+os.linesep \
                                        + "\tpadding-bottom: "+str(self.__bannerHeight) +"px;" +os.linesep \
                                        + "\tmargin-bottom: -"+str(self.__bannerHeight) +"px;" +os.linesep \

                self.__bannerCSS = self.__bannerCSS.replace("#bannerData#", self.__bannerData).replace("#bannerTextData#", self.__bannerTextData).replace("#BannerAnimation#", self.__bannerAnimation)

            elif line[0] == "navbar":
                "Navbar settings."
                if self.__navBarTemplateChanged == False:
                    self.__navBarTemplateChanged = True
                else:
                    self.__canBeOnlySetOnceError(line[0])
                __brandName = "Brand"
                __items = []
                __sticky = ""
                __expand = "-lg"
                args = self.__splitComma(args)
                self.__navBarCSS = self.__templateLoader("NavBarCSSTemplate")
                self.__navItemTemplate = self.__templateLoader("NavItemTemplate")
                for item in args:
                    if item.startswith("brand"):
                        inside=self.__Command_and_Argument(item)[1][1:-1]
                        if inside.startswith('"'):
                            __brandName = inside[1:-1]
                        else:
                            url=self.__splitByEQ(inside, 1)
                            __brandName = "<img class='img-fluid' target='_blank' style='max-width: 300px; max-height: 200px' src='" + url +  "'>"

                    elif item.startswith("item"):
                        subargs = self.__splitComma(self.__Command_and_Argument(item)[1][1:-1])
                        __items.append(self.__navItemTemplate.replace("#text#", subargs[0][1:-1]).replace("#link#", str("#"+subargs[1])))

                    elif item=="sticky":
                        __sticky="sticky-top"
                    elif item.startswith("expand"):
                        sizes={"0": "", "1": "-sm", "2": "-md", "3": "-lg", "4": "-xl"}
                        size = self.__splitByEQ(item, 1)
                        if size in sizes:
                            __expand=sizes[size]
                        else:
                            __expand = "-"+size



                    else:
                        self.__argumentError(item, "navbar")

                    self.__navBarTemplate = self.__navBarTemplate.replace("#Color2#", "#NavbarOpacityColor2#")

                self.__navBarTemplate=self.__navBarTemplate.replace("#brand#", __brandName).replace("#navItems#", os.linesep.join(__items)).replace("#sticky#", __sticky).replace("#expand#", __expand)

            elif line[0] == "table":
                """Adds a table content to the container body of the site"""

                self.__containerTemplateChanged = True
                self.__tableCSS = self.__templateLoader("TableCSSTemplate")
                __tableTemplate = self.__templateLoader("TableTemplate")
                __headTemplate = "\t\t\t\t<th scope='col'>#column#</th>"
                tempcolumns = []
                temprows = []
                __dark=""
                __id=""

                args = self.__splitComma(args)
                for item in args:
                    if item=="inverted":
                        __dark = "table-dark"
                    elif item.startswith("id"):
                        __id = self.__splitByEQ(item, 1)
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

                self.__tableCSS =self.__tableCSS.replace("Color2", "TableOpacityColor2")
            elif line[0] == "bootrow":
                """Adds a bootstrap row to the container part of the body."""

                self.__containerTemplateChanged = True
                __rowTemplate = self.__templateLoader("RowTemplate")
                __rowItemTemplate = self.__templateLoader("RowItemTemplate")
                __articleTemplate = self.__templateLoader("ArticleTemplate")
                self.__rowCSS = self.__templateLoader("RowCSSTemplate")
                __id=""
                __rates= "auto"
                __rowItems=[]
                __titleAlign="center"
                __imgfilter=""

                args = self.__splitComma(args)
                for item in args:
                    if item.startswith("id"):
                        __id = self.__splitByEQ(item, 1)
                    elif item.startswith("rate"):
                        if "auto" in item:
                            __rates="auto"
                        else:
                            __rates = self.__splitComma(self.__Command_and_Argument(item)[1][1:-1])
                            sum=0
                            for number in __rates:
                                sum+=int(number)
                            if sum!=12:
                                self.__error = self.__dicts.getWordFromDict(
                                    self.__Config.get_Element("Language"), "errorNot12")

                    elif item.startswith("image"):
                        __image = str("\t\t\t\t<a href='"+self.__splitByEQ(item, 1)+"'><img class='img-fluid #filter#' src='"+self.__splitByEQ(item, 1) + "'></a>")
                        if __rates != "auto":
                            __rowItems.append(__rowItemTemplate.replace("#number#", str("-"+__rates[len(__rowItems)])).replace("#data#", __image))
                        else:
                            __rowItems.append(__rowItemTemplate.replace("#number#", "").replace("#data#", __image))


                    elif item.strip()=="imgfilter":
                        __imgfilter="img-animate"

                    elif item.startswith("article"):
                        __article=__articleTemplate
                        __title=""
                        __text=""
                        for ehhh in self.__splitComma(self.__Command_and_Argument(item)[1][1:-1]):
                            if ehhh.startswith("title-align"):
                                __titleAlign = self.__splitByEQ(ehhh, 1)

                            elif ehhh.startswith("title"):
                                __title = self.__splitByEQ(ehhh, 1)[1:-1]

                            elif ehhh.startswith("rawtext"):
                                __text = self.__splitByEQ(ehhh, 1)[1:-1]

                            else:
                                self.__argumentError(item, "title")

                        __article = __article.replace("#title#", __title).replace("#text#", __text).replace("#align#", __titleAlign)
                        if __rates != "auto":
                            __rowItems.append(__rowItemTemplate.replace("#number#", str("-"+__rates[len(__rowItems)])).replace("#data#", __article))
                        else:
                            __rowItems.append(__rowItemTemplate.replace("#number#", "").replace("#data#", __article))

                    else:
                        self.__argumentError(item, "row")

                if __rates!="auto" and len(__rowItems)!=len(__rates):
                    self.__error = self.__dicts.getWordFromDict(
                        self.__Config.get_Element("Language"), "errorNoMatch")

                __rowTemplate = __rowTemplate.replace("#rowitems#", os.linesep.join(__rowItems)).replace("#id#", str("id='"+__id+"'")).replace("#filter#", __imgfilter)
                self.__mainBody+=__rowTemplate

                self.__rowCSS =self.__rowCSS.replace("Color2", "RowOpacityColor2")

            elif line[0]=="footer":
                """Sets the footer for the site."""
                if self.__footerTemplateChanged==False:
                    self.__footerTemplateChanged = True
                else:
                    self.__canBeOnlySetOnceError(line[0])
                self.__footerCSS = self.__templateLoader("FooterCSSTemplate")
                __footerData = ""
                __buttonText = "Go to Top"
                __socials = {}
                __icons = []

                __id=""
                args = self.__splitComma(args)

                social_icons = ["facebook", "youtube", "twitter", "vkontakte", "instagram", "googleplus", "linkedin", "github", "skype", "email", "phone"]

                for item in args:
                    if item.startswith("id"):
                        __id = self.__splitByEQ(item, 1)
                    elif item.startswith("button"):
                        __buttonText = self.__splitByEQ(item, 1)[1:-1]
                    elif self.__splitByEQ(item, 0) in social_icons:
                        __socials[self.__splitByEQ(item, 0)] = self.__splitByEQ(item, 1)
                    else:
                        self.__argumentError(item, "footer")

                if len(__socials) == 0:
                    xs=12
                elif len(__socials) < 5:
                    xs = int(12/len(__socials))
                elif len(__socials) < 7:
                    xs = 4
                elif len(__socials) > 6 :
                    xs = 3
                for media in social_icons:
                    if media in __socials.keys():
                        __icons.append(str("\t\t\t<div class='col-"+str(xs)+" col-md text-center'>" + os.linesep + "\t\t\t\t<a  href='" + __socials[media] + "' target='_blank'><img src='img/"+media+".png' class='img-fluid'></a>" + os.linesep + "</div>"))

                import datetime
                self.__footerTemplate = self.__footerTemplate.replace("#ButtonText#", __buttonText).replace("#id#", str("id='" + __id + "'")).replace("#year#", str(datetime.datetime.now()).split("-")[0])

                if len(__socials)>0:
                    self.__footerTemplate = self.__footerTemplate.replace("#icons#", os.linesep.join(__icons))
                else:
                    self.__footerTemplate = self.__footerTemplate.replace("#icons#", "")

                self.__footerCSS =self.__footerCSS.replace("Color2", "FooterOpacityColor2")

    def __canBeOnlySetOnceError(self, item):
        self.__error = self.__dicts.getWordFromDict(
            self.__Config.get_Element("Language"), "canBeOnlySetOnceError").replace("#item#", item)

    def __argumentError(self, Key, All):
        self.__error = self.__dicts.getWordFromDict(
            self.__Config.get_Element("Language"), "errorInvalidArgument").replace("#Key#",
                                                                                   Key).replace(
            "#All#", All)
    """
    def __formulaError(self, bad, good, command):
        self.__error = self.__dicts.getWordFromDict(
            self.__Config.get_Element("Language"), "formulaError").replace("#bad#", bad).replace("#good#", good).replace("#command#", command)
    """

    def __Command_and_Argument(self, line):
        return(line.split("(",1)[0], line.replace(line.split("(",1)[0], "", 1))

    def __splitComma(self, line):
        listOfArgs=[]
        lines2 = []
        lines = line.split(",")
        tempstring=""
        merge = False
        stringSign = False
        for item in lines:
            item=item.strip()
            tempstring +=item

            for char in item:
                if stringSign == False:
                    if char == '"' or char == "'" or char == '`':
                        stringSign = char
                if char == stringSign:
                    merge = not merge
            if merge == False:
                lines2.append(tempstring)
                tempstring=""
            else:
                tempstring+=", "

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
        if Key not in self.__Syntax.getValueOfKey(All):
            self.__argumentError(Key, All)

    def __addColors(self):
        for number in range(0,4):
            if self.__palette!="":
                self.__compiledReplacer("#Color"+str(number+1)+"#", self.__Colors.getPalette(self.__palette)[number])
                self.__compiledReplacer("#NavbarOpacityColor"+str(number+1)+"#", str("rgba(" + self.__Colors.getRGBA(self.__Colors.getPalette(self.__palette)[number]) + "," + str(self.__navbarOpacity) + ")"))
                self.__compiledReplacer("#TableOpacityColor"+str(number+1)+"#", str("rgba(" + self.__Colors.getRGBA(self.__Colors.getPalette(self.__palette)[number]) + "," + str(self.__tableOpacity) + ")"))
                self.__compiledReplacer("#RowOpacityColor"+str(number+1)+"#", str("rgba(" + self.__Colors.getRGBA(self.__Colors.getPalette(self.__palette)[number]) + "," + str(self.__rowOpacity) + ")"))
                self.__compiledReplacer("#FooterOpacityColor"+str(number+1)+"#", str("rgba(" + self.__Colors.getRGBA(self.__Colors.getPalette(self.__palette)[number]) + "," + str(self.__footerOpacity) + ")"))

    def __splitByEQ(self, item, part):
        return (item.split("=",1)[part].strip())

    def __templateLoader(self, s):
        return (open("templates/" + s + ".txt", "r").read())

    def __setBackGroundData(self, args, num):
        return "background-image: url('" + args[num] + "');" + os.linesep \
                            + "\tbackground-repeat: no-repeat;" + os.linesep \
                            + "\tbackground-attachment: fixed;" + os.linesep

    def __animPartMaker(self, animpart, number, img, blur, sat):
        return animpart.replace("#number#", str(number)).replace("#img#", img).replace("#blur#", blur).replace( "#sat#", sat)

    def __basicCSS(self, num):
        return "\tdisplay: flex;" + os.linesep \
                + "\talign-items: flex-end;" + os.linesep \
                + "\theight: " + num + "px;" + os.linesep \
                + "\tvertical-align: bottom;" + os.linesep

    def __spaceTags(self, code):
        import re
        parts= re.findall(r"<space:\d+>", code)
        for item in parts:
            code=code.replace("<space:"+item[7:-1]+">", "&nbsp;" * int(item[7:-1]))
        return(code)