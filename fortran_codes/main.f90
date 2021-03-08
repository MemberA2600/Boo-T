    include "fortran_modules/list.f90"
    include "fortran_modules/string_func.f90"
    include "fortran_modules/file_func.f90"
    include "fortran_modules/dict.f90"
    include "fortran_modules/os_func.f90"
    include "fortran_modules/randomInteger.f90"


module Syntax
    use string_func
    use list
    use file_func
    use dict

    implicit none
    contains

    function create_Dict(path) result(TempDict)
        type(Dictionary) :: TempDict
        character(len=100), dimension(:), allocatable :: temp, line_array
        character(len=:), allocatable :: path, line, command, arguments
        integer :: num

        temp = loadLines(path)
        call TempDict%create()

        do num = 1, size(temp), 1
            line = trim(temp(num))
            line_array = split(line, "=", 2)
            command = trim(line_array(1))
            arguments = trim(line_array(2))
            call TempDict%add(command, arguments)
        end do

    end function

end module

module Languages
    use dict
    use string_func
    use OS_func
    use file_func

    implicit none

    type wordDict
        character(:), allocatable :: language
        type(Dictionary) :: words

    end type

    contains

    function createDicts(os, dir) result(dicts)
        type(wordDict), dimension(:), allocatable :: dicts
        character(:), allocatable :: os, dir, filename, temp, pattern, word, message, deliminator
        integer :: alloc, num , num2
        character(100), dimension(:), allocatable :: listOfFiles, parts
        character(10000), dimension(:), allocatable :: lines


        listOfFiles = getFilesFromSubFolder(os, dir)
        allocate(dicts(size(listOfFiles)), stat=alloc)

        do num = 1, size(listOfFiles), 1
            temp = trim(listOfFiles(num))
            pattern = ".txt"
            if (endswith(trim(temp), pattern))  then
                filename = getFileNameFromPath(temp, os, .FALSE.)
                dicts(num)%language = filename
                lines = loadLines(temp)
                call dicts(num)%words%create()
                do num2=1, size(lines), 1
                    deliminator="="
                    parts = split(lines(num2), deliminator, 2)
                    word = trim(parts(1))
                    message = trim(parts(2))
                    call dicts(num)%words%add(word, message)
                end do
            end if
        end do

    end function

    function getWordFromDict(dicts, lang, word) result(message)
        character(:), allocatable :: lang, word, message
        type(wordDict), dimension(:), allocatable :: dicts
        integer :: num

        message = "Not found!"

        do num = 1, size(dicts), 1
            if (dicts(num)%language == lang) message = trim(dicts(num)%words%get(word))
        end do

    end function

    function getDeliminator(line) result(deliminator)
        character(:), allocatable :: deliminator, line, temp
        character(10000), dimension(:), allocatable :: lineSplitted

        lineSplitted = splitBySpaces(line, 9999)
        temp = trim(lineSplitted(1))
        call removeBullShitFromBeginning(temp)
        if (temp == "deliminator") then
            deliminator = trim(lineSplitted(2))
        else
            deliminator = "%%"
        end if
    end function

    subroutine removeComments(codeLines, deliminator)
        character(10000), dimension(:), allocatable, intent(inout) :: codeLines
        character(:), allocatable :: deliminator, temp
        integer :: linenum, x1, x2

        do linenum = 1, size(codeLines), 1
            do x1 = 1, len(codeLines(linenum))-1, 1
                x2 = x1 + len(deliminator)-1
                temp = codeLines(linenum)
                if (temp(x1:x2)==deliminator) then
                    temp = temp(1:x2)
                    codeLines(linenum) = temp
                end if
            end do
        end do

    end subroutine

    subroutine removeNewLineChar(codeLines)
        character(10000), dimension(:), allocatable, intent(inout) :: codeLines
        integer :: num,x
        character(:), allocatable :: temp, temp2

        do num = 1, size(codeLines), 1
            temp = codeLines(num)
            temp2 = ""
            do x = 1, len(temp), 1
                if (temp(x:x) /= achar(10) .AND. temp(x:x) /= achar(15)) then
                    temp2 = temp2 // temp(x:x)
                end if
            end do
            codeLines(num) = temp2
        end do
    end subroutine
    subroutine removeLeadingSpacesFromEveryLine(array)
        character(10000), dimension(:), allocatable, intent(inout) :: array
        character(:), allocatable :: temp
        integer :: num, x, charI

        do num = 1, size(array), 1
            do x = 1, len(array(num)), 1
                temp = array(num)
                charI = ichar(temp(x:x))
                if (charI>32) then
                    array(num) = temp(x:len(temp))
                    exit
                end if
            end do
        end do
    end subroutine

    subroutine templateLoader(string, name)
        character(:), allocatable, intent(inout) :: string
        character(:), allocatable :: name, path

        path = "templates/"//name//".txt"
        string = loadText(path)
        string = trim(string)

    end subroutine

    subroutine removeBullShitFromBeginning(command)
        character(:), allocatable, intent(inout) :: command
        integer :: num, start
        character(1) :: c

        start = 1
        do num=1, len(command), 1
            c = lower(command(num:num))

            if (ichar(c)<97 .OR. ichar(c)>122) then
                start = start + 1
            else
                exit
            end if
        end do

        command = command(start:len(command))

    end subroutine

end module

module compiler
    use dict
    use Languages
    use randomInteger
    use string_func
    use OS_func
    use list

    implicit none


    contains

    subroutine compileLine(lineNum, errorText, temp, author, title, description, keywords, background, bannerText,&
                & bannerCSS, navBarCSS, footerCSS, tableCSS, rowCSS, deliminator,&
                & mainTemplate, bannerTemplate, navbarTemplate, footerTemplate, containerTemplate ,&
                & cssTemplate, name, SyntaxList, ColorsList, RGBAList, Config, dicts,&
                & navbarOpacity, tableOpacity, rowOpacity, footerOpacity, fontFamily, lang, charset, palette, os,&
                & mainTemplateChanged, bannerTemplateChanged, navbarTemplateChanged, footerTemplateChanged&
                &, containerTemplateChanged, cssTemplateChanged)
        character(:), allocatable :: line, command, args, errorCommand, k, v, temp, allofthem, key, os
        character(:), allocatable, intent(inout) :: errorText
        character(:), allocatable, intent(inout) :: author, title, description, keywords, background, bannerText,&
                & deliminator, name, fontFamily, lang, charset, palette
        character(:), allocatable :: bannerCSS, navBarCSS, footerCSS, tableCSS, rowCSS,&
                & mainTemplate, bannerTemplate, navbarTemplate, footerTemplate, containerTemplate,&
                & cssTemplate
        real :: navbarOpacity, tableOpacity, rowOpacity, footerOpacity
        character(10000), dimension(2) :: comAndArg
        type(Dictionary) :: SyntaxList, ColorsList, RGBAList, Config
        type(wordDict), dimension(:), allocatable :: dicts
        character(10000), dimension(:), allocatable :: argList, tempList, tempList2, tempList3
        character(len=:), allocatable :: path, temp2, replacer
        integer :: lineNum, num, num2, io, num3, alloc, theSum
        logical :: mainTemplateChanged, bannerTemplateChanged, navbarTemplateChanged, footerTemplateChanged&
                    &, containerTemplateChanged, cssTemplateChanged, contain

        character(:), allocatable :: bannerSize, bannerTextSize, bannerTextAlign, bannerData, bannerTextData,&
                                    &bannerAnimation, time, animPart, bannerHeight, brandName, sticky, expand,&
                                    &temp3, navItemTemplate, tableTemplate, headTemplate, dark, theID,&
                                    &tempRowString, rowTemplate, articleTemplate, rowItemTemplate, rates,&
                                    &titleAlign, imgFilter, img, article, text, title2, footerData,&
                                    &buttonText

        integer :: move, still, xs
        type(charList) :: items, tempColumns, tempRows, tempRow, rowItems, icons
        character(3), dimension(5) :: sizes
        character(2), dimension(:), allocatable :: numbers
        character(10), dimension(:), allocatable :: social_icons
        type(Dictionary) :: socials
        character(8) date

        line=trim(adjustl(temp))

        comAndArg = commandAndArgument(line);
        command = trim(adjustl(comAndArg(1)))
        call removeBullShitFromBeginning(command)
        if (trim(command) == "") then
            ! do nothing
        else if (SyntaxList%containsKey(Command) .EQV. .FALSE.) then
            if (startswith(command, "deliminator") .EQV. .FALSE.) then
                errorCommand = "errorInvalidCommand"
                errorText = wordFromDict(errorCommand,Config, dicts)
                errorText = string_replace_all(errorText, "#line#", command)
            end if
        else
            args = trim(adjustl(comAndArg(2)))
            if (command == "deliminator") then
                if (lineNum>1) then
                    errorCommand = "deliminatorNoFirstLineError"
                    errorText = wordFromDict(errorCommand,Config, dicts)
                end if
            else if (command == "keywords") then
                keywords = args

            else if (command == "opacity") then
                argList = splitByCommmas(args, .FALSE.)
                do num = 1, size(argList), 1
                    temp = argList(num)
                    k = trim(adjustl(getFirstPartBeforeEQ(temp)))
                    v = trim(adjustl(getSecondPartAfterEQ(temp)))

                    if (k == "container") then
                        rowOpacity = charToReal(v)
                    else if (k == "navbar") then
                        navbarOpacity = charToReal(v)
                    else if (k == "table") then
                        tableOpacity = charToReal(v)
                    else if (k == "footer") then
                        footerOpacity = charToReal(v)
                    else
                        key = args
                        allofthem = "opacity"
                        errorText = argumentError(key, allofthem, Config, dicts)
                    end if

                end do
            else if (command == "description") then
                description = args
            else if (command == "font-family") then
                fontFamily = args
            else if (command == "title") then
                title = args
            else if (command == "basics") then
                argList = splitByCommmas(args, .FALSE.)

                do num = 1, size(argList), 1
                    temp = argList(num)
                    k = trim(adjustl(getFirstPartBeforeEQ(temp)))
                    v = trim(adjustl(getSecondPartAfterEQ(temp)))

                    if (k == "author") then
                        author = v
                    else if (k == "language") then
                        lang = v
                    else if (k == "charset") then
                        charset = v
                    else if (k == "palette") then
                        if (ColorsList%containsKey(v) .EQV. .FALSE.) then
                            if (v == "random") then
                                num2 = randInt(1,28)
                            else
                                num2 = charToInt(v)
                                num2 = num2+1
                            end if
                            if (num2<=ColorsList%getSize() .AND. num2>-1) then
                                tempList = ColorsList%getKeys()
                                v = tempList(num2)
                            else
                                errorCommand = "errorColorPalette"
                                errorText = wordFromDict(errorCommand,Config, dicts)
                                errorText = string_replace_all(errorText, "#Value#", v)
                            end if
                        end if
                        if (errorText == "No Error") palette = trim(v)
                    else
                        key = args
                        allofthem = "basics"
                        errorText = argumentError(key, allofthem, Config, dicts)
                    end if
                end do

            else if (command == "background") then
                if (startswith(args, "color")) then
                    background = "background-color: #Color1#"
                else if (startswith(args, "gradient")) then
                    background = "background-image: linear-gradient(#Data#)"

                    if (getSecondPartAfterEQ(args) == "HOR") then
                        temp = "to right, "
                    else if (getSecondPartAfterEQ(args) == "VER") then
                        temp = ""
                    else if (getSecondPartAfterEQ(args) == "DIG") then
                        temp = "to bottom right, "
                    else
                        key = args
                        allofthem = "background"
                        errorText = argumentError(key, allofthem, Config, dicts)
                    end if

                    temp = temp//"#Color1#, #Color2#, #Color1#"
                    background = string_replace_all(background, "#Data#", temp)

                else if (startswith(args, "image")) then
                    tempList=splitByCommmas(getSecondPartAfterEQ(args), .FALSE.)

                    if (size(tempList) == 1) then
                        background = setBackGroundData(tempList, 1, os)//achar(9)//"background-size: cover;"
                    else
                        background = setBackGroundData(tempList, 1, os)//achar(9)//"background-size: "//trim(tempList(2))//";"
                    end if

                end if
                name = "background.txt"
                call saveFile(name, background)

                !path="test.txt"
                !open(UNIT=11, file=path, status="replace", iostat=io, action="write", encoding='UTF-8')
                !write(11,*) background
                !close(11)
            else if (command == "banner") then
                if (bannerTemplateChanged .EQV. .TRUE.) then
                    errorText = canBeOnlySetOnceError(command, Config, dicts)
                else
                    bannerTemplateChanged = .TRUE.
                    tempList = splitByCommmas(args, .TRUE.)

                    bannerSize = "cover"
                    bannerTextSize = "3em"
                    bannerTextAlign = "center"
                    bannerData = ""
                    bannerTextData = ""
                    bannerAnimation = ""
                    bannerHeight = "200"

                    name = "BannerCSSTemplate"
                    call templateLoader(bannerCSS, name)

                    do num = 1, size(tempList), 1
                        temp = trim(adjustl(tempList(num)))
                        call removeBullShitFromBeginning(temp)

                        if (startswith(temp, "image") .EQV. .TRUE.) then
                            temp2 = getSecondPartAfterEQ(temp)
                            tempList2(2) = temp2
                            bannerData = bannerData//setBackGroundData(tempList2, 2, os)
                        else if (startswith(temp, "size") .EQV. .TRUE.) then
                            bannerSize = getSecondPartAfterEQ(temp)
                        else if (startswith(temp, "text") .EQV. .TRUE.) then
                            tempList2 = commandAndArgument(temp)
                            temp2 = tempList2(2)
                            tempList3 = splitByCommmas(temp2, .TRUE.)
                            bannerText = tempList3(1)(2:len_trim(tempList3(1))-1)
                            bannerTextSize = trim(tempList3(2))
                            bannerTextAlign = trim(tempList3(3))
                        else if (startswith(temp, "animation") .EQV. .TRUE.) then
                            temp2="bannerAnimationTemplate"
                            call templateLoader(bannerAnimation, temp2)

                            replacer = ""
                            tempList2 = commandAndArgument(temp)
                            temp2=tempList2(2)
                            tempList3 = splitByCommmas(temp2, .FALSE.)
                            time = tempList3(1)

                            move = (100/(size(tempList3)-1))/10
                            still = 100/(size(tempList3)-1) - move

                            animPart = achar(9)//achar(9)//"#number#%{	background-image: url('#img#');&
                            &	filter: saturate(#sat#) blur(#blur#px) ;}"//getLineSep(os)
                            num2=0

                            name = "animator.txt"
                            do num3 = 2, size(tempList3), 1
                                temp3 = animPartMaker(animPart, intToChar(num2), tempList3(num3), "3   ", "0.25")
                                temp3 = trim(temp3)
                                call appendFile(temp3, name)

                                temp3 = animPartMaker(animPart, intToChar(num2+move), tempList3(num3), "0  ", "1   ")
                                temp3 = trim(temp3)
                                call appendFile(temp3, name)

                                num2 = num2+still

                                temp3 = animPartMaker(animPart, intToChar(num2-move), tempList3(num3), "0   ", "1   ")
                                temp3 = trim(temp3)
                                call appendFile(temp3, name)

                                temp3 = animPartMaker(animPart, intToChar(num2), tempList3(num3), "3   ", "0.25")
                                temp3 = trim(temp3)
                                call appendFile(temp3, name)

                                num2 = num2+move

                            end do
                            temp3 = replacer//animPartMaker(animPart, intToChar(100), tempList3(2), "3   ", "0.25")
                            call appendFile(temp3, name)

                            replacer = loadText(name)
                            call deleteF(name)

                            bannerAnimation = string_replace_all(bannerAnimation, "#animationThings#", replacer)

                        else if (startswith(temp, "height") .EQV. .TRUE.) then
                            bannerHeight = getSecondPartAfterEQ(temp)
                        else
                            key = args
                            allofthem = "banner"
                            errorText = argumentError(key, allofthem, Config, dicts)

                        end if
                    end do
                    bannerData = bannerData//basicCSS(bannerHeight, os)//&
                                &achar(9)//"background-size: "//trim(bannerSize)//";"//getLineSep(os)//&
                                &achar(9)//"background-position-x: center;"//getLineSep(os)//&
                                &achar(9)//"background-position-y: center;"//getLineSep(os)//&
                                &achar(9)//"margin-left: auto;"//getLineSep(os)//&
                                &achar(9)//"margin-right: auto;"//getLineSep(os)//&
                                &achar(9)//"border-radius: 15px 15px 0px 0px;"//getLineSep(os)

                    if (bannerAnimation/="") then
                        bannerData = bannerData//achar(9)//"animation-name: bannerAnimation;"//getLineSep(os)//&
                                    &achar(9)//"animation-duration: "//trim(time)//";"//getLineSep(os)//&
                                    &achar(9)//"animation-timing-function: ease-in-out;"//getLineSep(os)//&
                                    &achar(9)//"animation-iteration-count: infinite;"//getLineSep(os)

                    temp2 = "0"
                    bannerTextData = bannerTextData//basicCSS(temp2, os)//&
                                    &achar(9)//"font-size: "//trim(bannerTextSize)//";"//getLineSep(os)//&
                                    &achar(9)//"justify-content: "//trim(bannerTextAlign)//";"//getLineSep(os)//&
                                    &achar(9)//"text-shadow: #Color1# 5px 5px 5px;"//getLineSep(os)//&
                                    &achar(9)//"padding-bottom: "//trim(bannerHeight)//"px;"//getLineSep(os)//&
                                    &achar(9)//"margin-bottom: -"//trim(bannerHeight)//"px;"//getLineSep(os)

                    bannerTextData = string_replace_all(bannerTextData, "left", "flex-start")
                    bannerTextData = string_replace_all(bannerTextData, "right", "flex-right")
                    bannerCSS = string_replace_all(bannerCSS, "#bannerData#", bannerData)
                    bannerCSS = string_replace_all(bannerCSS, "#bannerTextData#", bannerTextData)
                    bannerCSS = string_replace_all(bannerCSS, "#BannerAnimation#", bannerAnimation)
                    name = "bannerCSS.txt"
                    call saveFile(name, bannerCSS)
                    bannerTemplate = string_replace_all(bannerTemplate, "#bannertext#", bannerText)
                    name = "banner.txt"
                    call saveFile(name, bannerTemplate)

                    end if

                end if
            else if (command == "navbar") then

                if (navbarTemplateChanged .EQV. .TRUE.) then
                        errorText = canBeOnlySetOnceError(command, Config, dicts)
                else
                        navbarTemplateChanged = .TRUE.
                brandName = "Brand"
                call items%create()
                sticky = ""
                expand = "-lg"
                tempList = splitByCommmas(args, .TRUE.)
                name = "NavBarCSSTemplate"
                call templateLoader(bannerCSS, name)
                do num = 1, size(tempList), 1
                    temp = trim(adjustl(tempList(num)))
                    call removeBullShitFromBeginning(temp)

                    if (startswith(temp, "brand") .EQV. .TRUE.) then
                        tempList2 = commandAndArgument(temp)
                        temp2 = tempList2(2)
                        if (temp2(1:1)==achar(34)) then
                            brandName = temp2(2:len(temp2)-1)
                        else
                            brandName = "<img class='img-fluid' target='_blank' style='max-width: 300px; &
                            &max-height: 200px' src='"//trim(getSecondPartAfterEQ(temp2))//"'>"
                        end if
                    else if (startswith(temp, "item"))then
                        tempList2 = commandAndArgument(temp)
                        temp2 = tempList2(2)
                        tempList3 = splitByCommmas(temp2, .TRUE.)
                        temp2 = trim(tempList3(1))
                        name = "NavItemTemplate"
                        call templateLoader(navItemTemplate, name)
                        temp3 = string_replace_all(navItemTemplate, "#text#", temp2(2:len(temp2)-1))
                        temp2 = trim(tempList3(2))
                        temp3 = string_replace_all(temp3, "#link#", "#"//temp2)
                        call items%add(temp3)

                    else if (startswith(temp, "sticky")) then
                        sticky = "sticky-top"

                    else if (startswith(temp, "expand")) then
                        sizes=(/"   ", "-sm", "-md", "-lg", "-xl"/)
                        temp2 = getSecondPartAfterEQ(temp)
                        contain = .FALSE.
                        do num2  = 1, size(sizes), 1
                            if (trim(adjustl(temp2))==sizes(num2)) contain = .TRUE.
                        end do
                        if (contain .EQV. .TRUE.) then
                            expand = trim(adjustl(temp2))
                        else
                            expand = "-"//trim(adjustl(temp2))
                        end if

                    else
                        key = args
                        allofthem = "navbar"
                        errorText = argumentError(key, allofthem, Config, dicts)
                    end if
                end do

                temp3=""
                do num3 = 1, items%getSize(), 1
                    temp3=temp3//trim(items%get(num3))//getLineSep(os)
                end do
                navbarTemplate = string_replace_all(navbarTemplate, "#Color2#", "#NavbarOpacityColor2#")
                navbarTemplate = string_replace_all(navbarTemplate, "#brand#", brandName)
                navbarTemplate = string_replace_all(navbarTemplate, "#navItems#", temp3)
                navbarTemplate = string_replace_all(navbarTemplate, "#sticky#", sticky)
                navbarTemplate = string_replace_all(navbarTemplate, "#expand#", expand)


                name = "navBar.txt"
                call saveFile(name, navbarTemplate)
                end if


            else if (command == "table") then
                containerTemplateChanged = .TRUE.
                name = "TableCSSTemplate"
                call templateLoader(tableCSS, name);
                name = "TableTemplate"
                call templateLoader(tableTemplate, name);
                headTemplate = achar(9)//achar(9)//achar(9)//achar(9)//"<th scope='col'>#column#</th>"
                call tempRows%create()
                call tempColumns%create()
                dark = ""
                theId= ""
                tempList = splitByCommmas(args, .TRUE.)
                do num2 = 1, size(tempList), 1
                    temp = tempList(num2)
                    call removeBullShitFromBeginning(temp)
                    if (startswith(temp, "inverted") .EQV. .TRUE.) then
                        dark = "table-dark"
                    else if (startswith(temp, "id") .EQV. .TRUE.) then
                        theID = trim(getSecondPartAfterEQ(temp))
                    else if (startswith(temp, "columns") .EQV. .TRUE.) then
                        tempList2 = commandAndArgument(temp)
                        temp2 = tempList2(2)
                        tempList3 = splitByCommmas(temp2, .TRUE.)
                        do num3=1, size(tempList3), 1
                            temp3 = trim(adjustl(tempList3(num3)))
                            temp3 = temp3(2:len(temp3)-1)
                            temp3 = string_replace_all(headTemplate, "#column#", temp3)
                            temp3=trim(temp3)
                            call tempColumns%add(temp3)
                        end do
                    else if (startswith(temp, "row") .EQV. .TRUE.) then
                        tempList2 = commandAndArgument(temp)
                        temp2 = tempList2(2)
                        call tempRow%create()
                        tempRowString=achar(9)//achar(9)//achar(9)//"<tr>"//getLineSep(os)
                        tempList3 = splitByCommmas(temp2, .TRUE.)
                        do num3 = 1, size(tempList3), 1
                            temp3 = trim(adjustl(tempList3(num3)))
                            temp3 = temp3(2:len(temp3)-1)
                            temp3=trim(temp3)
                            call tempRow%add(temp3)
                        end do

                        do num3 = 1, tempRow%getSize(), 1
                            tempRowString = tempRowString//achar(9)//achar(9)//achar(9)//achar(9)
                            if (num3 == 1) then
                                tempRowString = tempRowString//"<th scope='row'>#value#</th>"
                            else
                                tempRowString = tempRowString//"<td>#value#</td>"
                            end if
                            tempRowString = tempRowString//getLineSep(os)
                            tempRowString = string_replace_all(tempRowString, "#value#", tempRow%get(num3))

                        end do
                        tempRowString = tempRowString//achar(9)//achar(9)//achar(9)//"</tr>"//getLineSep(os)
                        call tempRows%add(tempRowString)
                    else
                        key = args
                        allofthem = "table"
                        errorText = argumentError(key, allofthem, Config, dicts)

                    end if
                end do

                temp3 = ""
                do num3 = 1, tempColumns%getSize(), 1
                    temp3 = temp3//tempColumns%get(num3)//getLineSep(os)

                end do
                tableTemplate = string_replace_all(tableTemplate, "#headItems#", temp3)
                temp3 = ""
                do num3 = 1, tempRows%getSize(), 1
                    temp3 = temp3//tempRows%get(num3)//getLineSep(os)

                end do
                tableTemplate = string_replace_all(tableTemplate, "#rowItems#", temp3)
                tableTemplate = string_replace_all(tableTemplate, "#dark#", dark)
                temp3 = "id='"//theId//"'"
                tableTemplate = string_replace_all(tableTemplate, "#id#", temp3)

                temp3 = "mainBody.txt"
                call appendFile(tableTemplate, temp3)

                tableCSS = string_replace_all(tableCSS, "#Color2#", "#TableOpacityColor2#")
                name="tableCSS.txt"
                call saveFile(name, tableCSS)
            else if (command == "bootrow") then

                containerTemplateChanged = .TRUE.
                name = "RowTemplate"
                call templateLoader(rowTemplate, name)
                name = "RowItemTemplate"
                call templateLoader(rowItemTemplate, name)
                name = "ArticleTemplate"
                call templateLoader(articleTemplate, name)
                name = "RowCSSTemplate"
                call templateLoader(rowCSS, name)
                theID = ""
                rates = "auto"
                call rowItems%create()
                titleAlign = "center"
                imgFilter = ""
                tempList = splitByCommmas(args, .TRUE.)
                temp = ""

                do num2 =1, size(tempList), 1
                    temp = trim(adjustl(tempList(num2)))
                    call removeBullShitFromBeginning(temp)
                    if (startswith(temp, "id") .EQV. .TRUE.) then
                        theID = trim(getSecondPartAfterEQ(temp))
                    else if (startswith(temp, "rate") .EQV. .TRUE.) then
                        tempList3 = commandAndArgument(temp)
                        if (trim(adjustl(tempList3(2))) == "auto") then
                            rates = "auto"
                        else
                            rates = "numbers"
                            tempList2 = commandAndArgument(temp)
                            temp2 = trim(adjustl(tempList2(2)))
                            tempList2 = splitByCommmas(temp2, .FALSE.)
                            allocate(numbers(size(tempList2)), stat=alloc)
                            theSum = 0
                            do num3 = 1, size(tempList2), 1
                                temp2 = tempList2(num3)
                                numbers(num3) = temp2
                                theSum = theSum + charToInt(temp2)
                            end do
                            if (theSum /=12) then
                                errorCommand = "errorNot12"
                                errorText = wordFromDict(errorCommand,Config, dicts)

                            end if

                        end if
                    else if (startswith(temp, "image") .EQV. .TRUE.) then
                        img = achar(9)//achar(9)//achar(9)//achar(9)//"<a href='"//&
                              &trim(adjustl(getSecondPartAfterEQ(temp)))//"'><img class='img-fluid #filter#' src='"//&
                              &trim(adjustl(getSecondPartAfterEQ(temp)))//"'></a>"
                        if (rates /= "auto") then
                            temp2 = string_replace_all(rowItemTemplate, "#number#", "-"//numbers(rowItems%getSize()+1))
                        else
                            temp2 = string_replace_all(rowItemTemplate, "#number#", "")
                        end if

                    temp2 = string_replace_all(temp2, "#data#", img)
                    call rowItems%add(temp2)

                    else if (startswith(temp, "imgfilter") .EQV. .TRUE.) then
                        imgFilter = "img-animate"
                    else if (startswith(temp, "article") .EQV. .TRUE.) then
                        article = articleTemplate
                        title2 = ""
                        text = ""
                        tempList2 = commandAndArgument(temp)
                        temp2 = tempList2(2)
                        tempList2 = splitByCommmas(temp2, .TRUE.)
                        do num3 = 1, size(tempList2), 1
                            temp3 = trim(tempList2(num3))
                            if (startswith(temp3, "title-align")) then
                                titleAlign = trim(adjustl(getSecondPartAfterEQ(temp3)))
                            else if (startswith(temp3, "title")) then
                                title2 = trim(adjustl(getSecondPartAfterEQ(temp3)))
                            else if (startswith(temp3, "rawtext")) then
                                text = trim(adjustl(getSecondPartAfterEQ(temp3)))
                            else
                                key = args
                                allofthem = "title"
                                errorText = argumentError(key, allofthem, Config, dicts)
                            end if
                        end do
                        article = string_replace_all(article, "#title#", title2)
                        article = string_replace_all(article, "#title-align#", titleAlign)
                        article = string_replace_all(article, "#text#", text)


                        if (rates /= "auto") then
                            temp2 = string_replace_all(rowItemTemplate, "#number#", "-"//numbers(rowItems%getSize()+1))
                        else
                            temp2 = string_replace_all(rowItemTemplate, "#number#", "")
                        end if
                        temp2 = string_replace_all(temp2, "#data#", article)
                        call rowItems%add(temp2)
                    else
                        key = args
                        allofthem = "row"
                        errorText = argumentError(key, allofthem, Config, dicts)
                    end if
                end do
                if (rates/="auto" .AND. rowItems%getSize()/=size(numbers)) then
                    errorCommand = "errorNoMatch"
                    errorText = wordFromDict(errorCommand,Config, dicts)
                end if
                temp2 = ""
                do num2=1, rowItems%getSize(), 1
                    temp2=temp2//rowItems%get(num2)//getLineSep(os)
                end do
                rowTemplate = string_replace_all(rowTemplate, "#rowitems#", temp2)
                rowTemplate = string_replace_all(rowTemplate, "#id#", "id='"//theID//"'")
                rowTemplate = string_replace_all(rowTemplate, "#filter#", imgFilter)

                temp3 = "mainBody.txt"
                call appendFile(rowTemplate, temp3)

                rowCSS = string_replace_all(rowCSS, "#Color2#", "#RowOpacityColor2#")
                name="rowCSS.txt"
                call saveFile(name, rowCSS)
            else if (command == "footer") then

                if (footerTemplateChanged .EQV. .TRUE.) then
                        errorText = canBeOnlySetOnceError(command, Config, dicts)
                else
                        footerTemplateChanged = .TRUE.
                end if
                footerData = ""
                buttonText = "Go to Top"
                call socials%create()
                call icons%create()
                theID = ""
                tempList = splitByCommmas(args, .TRUE.)

                social_icons = (/"facebook  ","youtube   ","twitter   ","vkontakte ","instagram ",&
                &"googleplus","linkedin  ","github    ","skype     ","email     ", "phone     " /)

                do num=1, size(tempList), 1
                    contain = .FALSE.
                    temp = tempList(num)
                    call removeBullShitFromBeginning(temp)

                    do num2 = 1, size(social_icons), 1
                        if (getFirstPartBeforeEQ(temp) == trim(social_icons(num2))) contain = .TRUE.
                    end do

                    if (startswith(temp, "id")) then
                        theID = getSecondPartAfterEQ(temp)
                    else if (startswith(temp, "button")) then
                        buttonText = getSecondPartAfterEQ(temp)
                    else if (contain .EQV. .TRUE.) then
                        call socials%add(getFirstPartBeforeEQ(temp), getSecondPartAfterEQ(temp))
                    else
                        key = args
                        allofthem = "footer"
                        errorText = argumentError(key, allofthem, Config, dicts)
                    end if
                    end do
                    if (socials%getSize() == 0) then
                        xs = 12
                    else if (socials%getSize() < 5) then
                        xs = 12/socials%getSize()
                    else if (socials%getSize() < 7) then
                        xs = 4
                    else
                        xs = 3
                    end if

                    tempList2 = socials%getKeys()
                    do num2 = 1,  size(social_icons), 1
                        do num3 = 1, socials%getSize(), 1
                            if (trim(social_icons(num2)) == trim(tempList2(num3))) then
                                name = trim(tempList2(num3))
                                temp3 = achar(9)//achar(9)//achar(9)//"<div class='col-"//intToChar(xs)//&
                                        &" col-md text-center'>"//getLineSep(os)//&
                                        &achar(9)//achar(9)//achar(9)//achar(9)//"<a  href='"//&
                                        &socials%get(name)//&
                                        &"' target='_blank'><img src='img/"//name//&
                                        &".png' class='img-fluid'></a>"//getLineSep(os)//"</div>"
                                call icons%add(temp3)
                            end if
                        end do
                    end do

                    call date_and_time(DATE=date)
                    date = date(1:4)
                    footerTemplate = string_replace_all(footerTemplate, "#ButtonText#", buttonText(2:len_trim(buttonText)-1))
                    footerTemplate = string_replace_all(footerTemplate, "#id#", "id='"//theID//"'")
                    footerTemplate = string_replace_all(footerTemplate, "#year#", date(1:4))

                    if (socials%getSize()>0) then
                       temp3 = ""
                       !tempList2 = socials%getKeys()
                       !tempList3 = socials%getValues()
                       do num3 = 1, icons%getSize(),1
                       !     write(*,*) trim(tempList2(num3))
                       !     write(*,*) trim(tempList3(num3))


                            temp3 = temp3//icons%get(num3)//getLineSep(os)
                       end do

                       footerTemplate = string_replace_all(footerTemplate, "#icons#", temp3)
                    else
                       footerTemplate = string_replace_all(footerTemplate, "#icons#", "")
                    end if


                    name = "FooterCSSTemplate"
                    call templateLoader(footerCSS, name)
                    footerCSS = string_replace_all(footerCSS, "#Color2#", "FooterOpacityColor2")

                    name = "footer.txt"
                    call saveFile(name, footerTemplate)

                    name = "footerCSS.txt"
                    call saveFile(name, footerCSS)
            end if

        end if
    end subroutine



    function getFirstPartBeforeEQ(string) result (part)
        character(:), allocatable :: string, part
        integer :: x1, num

        part=""
        x1=0
        do num=1, len(string), 1
            if (x1==0 .AND. string(num:num) == "=") then
                x1=num-1
                exit
            end if
        end do

        part = string(1:x1)


    end function

    function getSecondPartAfterEQ(string) result (part)
        character(:), allocatable :: string, part
        integer :: x1, num

        part=""
        x1=0
        do num=1, len(string), 1
            if (x1==0 .AND. string(num:num) == "=") then
                x1=num+1
                exit
            end if
        end do

        if ((string(x1:x1)==achar(34) .AND. string(len(string):len(string))==achar(34)) .OR.&
        & (string(x1:x1)==achar(39) .AND. string(len(string):len(string))==achar(39)) .OR.&
        (string(x1:x1)==achar(96) .AND. string(len(string):len(string))==achar(96))) then
            part = string(x1+1:len(string)-1)
        else
            part = string(x1:len(string))

        end if
    end function

    function basicCSS(num, os) result(string)
        character(:), allocatable :: num, string, os

        string = achar(9) // "display: flex;" // getLineSep(os) //&
                &achar(9) // "height: " // trim(num) // "px;" // getLineSep(os) //&
                &achar(9) // "align-items: flex-end;" // getLineSep(os) //&
                &achar(9) // "vertical-align: bottom;" // getLineSep(os)



    end function

    function animPartMaker(animpart, numb, img, blur, sat) result(string)
        character(:), allocatable :: animpart, string, numb, temp
        character(4) :: sat
        character(1) :: blur
        character(10000) :: img

        temp=trim(adjustl(img))
        call removeBullShitFromBeginning(temp)
        img=temp

        string = string_replace_all(animpart, "#number#", numb)
        string = string_replace_all(string, "#img#", trim(adjustl(img)))
        string = string_replace_all(string, "#sat#", trim(adjustl(sat)))
        string = string_replace_all(string, "#blur#", trim(adjustl(blur)))
    end function


    function canBeOnlySetOnceError(command, Config, dicts) result(errorText)
        character(:), allocatable :: command, errorText, errorCommand
        type(Dictionary) :: Config
        type(wordDict), dimension(:), allocatable :: dicts

        errorCommand = "canBeOnlySetOnceError"
        errorText = wordFromDict(errorCommand,Config, dicts)
        errorText = string_replace_all(errorText, "#item#", command)

    end function

    function setBackGroundData(tempList, num, os) result(text)
        character(10000), dimension(:), allocatable :: tempList
        integer :: num
        character(:), allocatable :: text, os

        text = "background-image: url('"//trim(tempList(num))//"');"//getLineSep(os)//&
        &achar(9)//"background-repeat: no-repeat;"//getLineSep(os)//&
        &achar(9)//"background-attachment: fixed;"//getLineSep(os)

    end function


    function argumentError(key, allofthem, Config, dicts) result(errorText)
        character(:), allocatable :: key, allofthem, errorText, errorCommand
        type(Dictionary) :: Config
        type(wordDict), dimension(:), allocatable :: dicts

        errorCommand = "errorInvalidArgument"
        errorText = wordFromDict(errorCommand,Config, dicts)
        errorText = string_replace_all(errorText, "#Key#", key)
        errorText = string_replace_all(errorText, "#All#", allofthem)


    end function

    function splitByCommmas(string, merger) result(array)
        character(:), allocatable :: string
        character(10000), dimension(:), allocatable :: array
        logical :: merger

        array = split(string, ",", 9999)
        if (merger .EQV. .TRUE.) array = subMerge(array)

    end function

    !function splitByEQ(string) result(array)
    !    character(:), allocatable :: string
    !    character(10000), dimension(:), allocatable :: array
    !
    !    array = split(string, "=", 2)
    !
    !end function

    function subMerge(array) result (mergedArray)
        character(10000), dimension(:), allocatable :: array, mergedArray
        logical :: merger
        integer :: num, subNum, x, alloc, num2
        character(:), allocatable :: temp, tempString, stringSign
        type(CharList) :: tempList, tempList2

        call tempList%create
        call tempList2%create

        merger = .FALSE.
        stringSign = ""

        tempString = ""
        do num=1, size(array), 1
            temp = trim(adjustl(array(num)))
            tempString = tempString//temp
            do num2=1, len(temp), 1
                if (stringSign == "") then
                    if (temp(num2:num2) == achar(34) .OR. temp(num2:num2) == achar(39)&
                    & .OR. temp(num2:num2) == achar(96)) stringSign = temp(num2:num2)
                end if
                if (temp(num2:num2) == stringSign) then
                    if (merger .EQV. .FALSE. ) then
                        merger = .TRUE.
                    else
                        merger = .FALSE.
                    end if
                end if
            end do

            if (merger .EQV. .FALSE.) then
                call tempList%add(tempString)
                tempString=""
            else
                tempString=tempString//", "
            end if
        end do

        merger = .FALSE.
        tempString = ""
        mergedArray = tempList%getAll()

        do num=1, size(mergedArray), 1
            temp = trim(adjustl(mergedArray(num)))
            tempString = tempString//temp
            do num2=1, len(temp), 1
                if (temp(num2:num2) == achar(40)) then
                    merger = .TRUE.
                else if (temp(num2:num2) == achar(41)) then
                    merger = .FALSE.
                end if
            end do

            if (merger .EQV. .FALSE.) then
                call tempList2%add(tempString)
                tempString=""
            else
                tempString=tempString//","
            end if

        end do

        mergedArray = tempList2%getAll()

    end function


    function commandAndArgument(line) result(array)
        character(:), allocatable :: line
        character(10000), dimension(2) :: array
        integer :: num, num2, num3
        num2=0
        do num = 1, len_trim(line), 1
            if (line(num:num)==achar(40) .AND. num2 == 0) then
                num2 = num
            end if
            if (line(num:num)==achar(41)) then
                num3 = num
            end if
        end do
        if (num2 == 0) then
            array(1) = trim(adjustl(line))
            array(2) = ""
        else
            array(1) = trim(adjustl(line(1:num2-1)))
            array(2) = adjustl(line(num2+1:num3-1))
        end if

    end function

    function wordFromDict(word, Config, dicts) result(res)
        type(Dictionary) :: Config
        type(wordDict), dimension(:), allocatable :: dicts
        character(:), allocatable :: word, key, res
        integer :: num

        do num=1, size(dicts),1
            key = "Language"
            if (dicts(num)%language == Config%get(key)) then
                res = dicts(num)%words%get(word)
            end if

        end do
    end function

    subroutine templateChanger(compiled, var, string, changeTo)
        character(:), allocatable, intent(inout) :: compiled
        character(:), allocatable :: string, changeTo
        logical :: var
        if (var .EQV. .TRUE.) then
            compiled = string_replace_all(compiled, string, changeTo)
        else
            compiled = string_replace_all(compiled, string, "")
        end if


    end subroutine


    subroutine saveFile(name, string)
        character(:), allocatable :: name, string
        integer :: io

        open(unit=11, file=name, status="REPLACE", action="WRITE", iostat=io, encoding="utf-8")
        write(11,*) string
        close(11)

    end subroutine

    subroutine appendFile(string, name)
        character(:), allocatable :: name, string, temp
        integer :: io

        open(unit=11, file=name, status="unknown", position="append", action="write")
        write(11,*) string
        close(11)

    end subroutine

    subroutine deleteF(path)
        character(:), allocatable :: path
        integer :: io

        open(unit=1234, iostat=io, file=path, status='old')
        if (io == 0) close(1234, status='delete')

    end subroutine


end module

module fresh
    use string_func
    use list
    use file_func
    use Syntax
    use dict
    use OS_func
    use compiler

    implicit none

    contains

    subroutine hopeThereWontBeAnyMemoryAllocationErrors(palette, author, title, charset, keywords,&
        &description, fontfamily, lang, mainTemplateChanged, bannerTemplateChanged,&
        &navbarTemplateChanged, footerTemplateChanged, containerTemplateChanged,&
        &cssTemplateChanged, navbarOpacity, tableOpacity, rowOpacity, footerOpacity&
        ,ColorsList, RGBAList)
        character(:), allocatable :: name,  background, compiled, palette, temp, author, title, charset,&
                                    &keywords, description, fontfamily, lang

        logical :: mainTemplateChanged, bannerTemplateChanged, navbarTemplateChanged, footerTemplateChanged&
                &, containerTemplateChanged, cssTemplateChanged

        real :: navbarOpacity, tableOpacity, rowOpacity, footerOpacity
        type(Dictionary) :: ColorsList, RGBAList
        integer :: num, io
        character(10000), dimension(:), allocatable :: tempList

        compiled = ""
        name = "MainTemplate"
        call templateLoader(compiled, name)
        compiled = trim(compiled)

        temp = ""
        name = "CSSTemplate"
        call templateLoader(temp, name)
        name = "#style#"
        temp = temp(1:getTheLastChar(temp))
        call templateChanger(compiled, .TRUE.,name, temp)

        temp = ""
        name = "background.txt"
        temp=loadText(name)
        call deleteFile(name)
        name="#background#"
        temp = temp(1:getTheLastChar(temp))
        call templateChanger(compiled, .TRUE., name, temp)

        temp = ""
        name = "bannerCSS.txt"
        temp = loadText(name)
        call deleteFile(name)
        name="#bannerCSS#"
        temp = temp(1:getTheLastChar(temp))
        call templateChanger(compiled, bannerTemplateChanged,name, temp)

        temp = ""
        name = "footerCSS.txt"
        temp=loadText(name)
        call deleteFile(name)
        name="#footerCSS#"
        temp = temp(1:getTheLastChar(temp))
        call spaceTags(temp)
        call templateChanger(compiled, footerTemplateChanged,name, temp)

        temp = ""
        name = "tableCSS.txt"
        temp=loadText(name)
        call deleteFile(name)
        name="#tableCSS#"
        temp = temp(1:getTheLastChar(temp))
        call spaceTags(temp)
        call templateChanger(compiled, containerTemplateChanged,name, temp)

        temp = ""
        name = "rowCSS.txt"
        temp=loadText(name)
        call deleteFile(name)
        name="#rowCSS#"
        temp = temp(1:getTheLastChar(temp))
        call spaceTags(temp)
        call templateChanger(compiled, containerTemplateChanged,name, temp)

        temp = ""
        name = "NavBarCSSTemplate"
        call templateLoader(temp, name)
        name ="#navBarCSS#"
        temp = temp(1:getTheLastChar(temp))
        call spaceTags(temp)
        call templateChanger(compiled, navbarTemplateChanged,name, temp)

        temp = ""
        name = "banner.txt"
        temp=loadText(name)
        call deleteFile(name)
        name="#Banner#"
        temp = temp(1:getTheLastChar(temp))
        call spaceTags(temp)
        call templateChanger(compiled, bannerTemplateChanged,name, temp)

        temp = ""
        name = "navBar.txt"
        temp=loadText(name)
        call deleteFile(name)
        name="#NavBar#"
        temp = temp(1:getTheLastChar(temp))
        call spaceTags(temp)
        call templateChanger(compiled, navbarTemplateChanged,name, temp)

        temp = ""
        name = "mainBody.txt"
        temp=loadText(name)
        call deleteFile(name)
        name="#Container#"
        temp = temp(1:getTheLastChar(temp))
        call spaceTags(temp)
        call templateChanger(compiled, containerTemplateChanged,name, temp)

        temp = ""
        name = "footer.txt"
        temp=loadText(name)
        call deleteFile(name)
        name="#Footer#"
        temp = temp(1:getTheLastChar(temp))
        call spaceTags(temp)
        call templateChanger(compiled, footerTemplateChanged,name, temp)

        compiled = string_replace_all(compiled, "#author#", author)
        compiled = string_replace_all(compiled, "#title#", title)
        compiled = string_replace_all(compiled, "#lang#", lang)
        compiled = string_replace_all(compiled, "#keywords#", keywords)
        compiled = string_replace_all(compiled, "#description#", description)
        compiled = string_replace_all(compiled, "#author#", author)
        compiled = string_replace_all(compiled, "#charset#", charset)

        compiled = string_replace_all(compiled, "#font#", fontFamily)


        if (palette /="") then
            do num = 1, 4, 1
                tempList = splitByCommmas(ColorsList%get(palette), .FALSE.)
                temp = trim(adjustl(tempList(num)))
                compiled = string_replace_all(compiled, "#Color"//intToChar(num)//"#", temp)
                compiled = string_replace_all(compiled, "#NavbarOpacityColor"//intToChar(num)//"#",&
                            &"rgba("//RGBAList%get(temp)//","//realToChar(navbarOpacity)//")")
                compiled = string_replace_all(compiled, "#TableOpacityColor"//intToChar(num)//"#",&
                            &"rgba("//RGBAList%get(temp)//","//realToChar(tableOpacity)//")")
                compiled = string_replace_all(compiled, "#RowOpacityColor"//intToChar(num)//"#",&
                            &"rgba("//RGBAList%get(temp)//","//realToChar(rowOpacity)//")")
                compiled = string_replace_all(compiled, "#FooterOpacityColor"//intToChar(num)//"#",&
                            &"rgba("//RGBAList%get(temp)//","//realToChar(footerOpacity)//")")
            end do
        end if
        name="temp.txt"

        open(11, file=name, iostat=io, STATUS="replace", action="write")
        write(11, *) compiled(1:getTheLastChar(compiled))
        close(11)

    end subroutine

    function getTheLastChar(text) result(lastChar)
        integer :: num, lastChar, temp
        character(:), allocatable :: text
        character(1) :: a, b, c

        temp=1
        do num=len_trim(text), 1, -1
            if (ichar(text(num:num))==62 .OR. ichar(text(num:num))==125&
            & .OR. ichar(text(num:num))==35 .OR. ichar(text(num:num))==59&
            & .OR. ichar(text(num:num))==41) then

                lastChar = num
                exit
            end if
        end do

    end function

    subroutine deleteFile(path)
        character(:), allocatable :: path
        integer :: io

        open(unit=1234, iostat=io, file=path, status='old')
        if (io == 0) close(1234, status='delete')

    end subroutine

    subroutine spaceTags(code)
        character(:), allocatable, intent(inout) :: code
        integer :: x1, x2, x3, db, startnum
        character(:), allocatable :: tempstring, changeTo
        logical :: was

        startnum = 1
        x1 = 1
        do while(x1 < len_trim(code)-9)
            was = .FALSE.
            do x1=startnum, len_trim(code)-9, 1
                x2 = x1+6
                if (code(x1:x2) == "<space:") then
                    x3=x2+1
                    do while(code(x3:x3)/=">")
                        x3 = x3 + 1
                    end do
                    tempstring = code(x1:x3)
                    db = charToInt(code(x2+1:x3-1))
                    changeTo = ""
                    do while(db>0)
                        changeTo = changeTo//"&nbsp;"
                        db = db - 1
                    end do

                    code = string_replace_all(code, tempstring, changeTo)
                    was = .TRUE.
                    exit

                end if
            end do
            if (was .EQV. .TRUE.) startnum = x1
        end do

    end subroutine

end module

subroutine FortranCompiler() bind(C, name="compile")

    use string_func
    use list
    use file_func
    use Syntax
    use dict
    use OS_func
    use Languages
    use compiler
    use randomInteger
    use fresh

    implicit none
    type(Dictionary) :: SyntaxList, ColorsList, RGBAList, Config
    integer :: num, alloc, lineNum, io
    character(:), allocatable :: key, value, path, os, dir, ch, language, word, code
    type(wordDict), dimension(:), allocatable :: dicts

    character(:), allocatable :: author, title, description, keywords, background, bannerText,&
                & bannerCSS, navBarCSS, footerCSS, tableCSS, rowCSS, deliminator,&
                & mainTemplate, bannerTemplate, navbarTemplate, footerTemplate, containerTemplate ,&
                & cssTemplate, name, errorText, errorCommand, mainBody

    character(10000), dimension(:), allocatable :: codeLines, tempList
    real :: navbarOpacity, tableOpacity, rowOpacity, footerOpacity
    character(:), allocatable :: fontFamily, lang, charset, palette, temp, compiled, RGBA
    logical :: mainTemplateChanged, bannerTemplateChanged, navbarTemplateChanged, footerTemplateChanged&
                &, containerTemplateChanged, cssTemplateChanged, nonEmpty

    name = "mainBody.txt"
    temp=""
    call saveFile(name, temp)

    os = "Windows"
    dir = "dicts"

    !Load the important data modules

    path = "default/Syntax.txt"
    SyntaxList = create_Dict(path)
    path = "default/Colors.txt"
    ColorsList = create_Dict(path)
    path = "default/RGBA.txt"
    RGBAList = create_Dict(path)
    path = "Config.txt"
    Config= create_Dict(path)

    dicts = createDicts(os, dir)

    !Set basic variables
    author=""
    title=""
    description=""
    keywords=""
    background=""
    bannerText=""
    bannerCSS=""
    navBarCSS=""
    footerCSS=""
    mainBody=""
    tableCSS=""
    rowCSS=""

    navbarOpacity = 1.0
    tableOpacity= 1.0
    rowOpacity= 1.0
    footerOpacity= 1.0

    !Set defaults
    fontFamily = "Arial"
    lang = "en"
    charset = "UTF-8"
    palette = "black"


    !Formatting the code, getting the full, perfect lines before reading it
    path = "temp.boo"
    codeLines = loadLines(path)
    !do num = 1, len(codeLines), 1
    !    write(*,*) codeLines(num)
    !end do

    temp = codeLines(1)
    deliminator = getDeliminator(temp)
    call removeComments(codeLines, deliminator)
    call removeLeadingSpacesFromEveryLine(codeLines)
    code = trim(arrayToTextWithoutNewLines(codeLines))

    codeLines = split(code, deliminator, 9999999)

    !Load templates
    name = "MainTemplate"
    call templateLoader(mainTemplate, name)
    mainTemplateChanged = .FALSE.
    name = "BannerTemplate"
    call templateLoader(bannerTemplate, name)
    bannerTemplateChanged = .FALSE.
    name = "NavBarTemplate"
    call templateLoader(navbarTemplate, name)
    navbarTemplateChanged = .FALSE.
    name = "FooterTemplate"
    call templateLoader(footerTemplate, name)
    footerTemplateChanged = .FALSE.
    name = "ContainerTemplate"
    call templateLoader(containerTemplate, name)
    containerTemplateChanged = .FALSE.


    !Compile Line-By-Line, if there is a compile error, puts message at end and sets string

    compiled = ""
    errorText = "No Error"

    do lineNum = 1, size(codeLines), 1
        nonEmpty = .FALSE.
        do num=1, len(codeLines(lineNum)), 1
            if (ichar(codeLines(lineNum)(num:num))>32) then
                nonEmpty = .TRUE.
                exit
            end if
        end do
        if (nonEmpty .EQV. .TRUE.) then
            temp = codeLines(lineNum)
            CALL compileLine(lineNum, errorText, temp, author, title, description, keywords, background, bannerText,&
                & bannerCSS, navBarCSS, footerCSS, tableCSS, rowCSS, deliminator,&
                & mainTemplate, bannerTemplate, navbarTemplate, footerTemplate, containerTemplate ,&
                & cssTemplate, name, SyntaxList, ColorsList, RGBAList, Config, dicts,&
                & navbarOpacity, tableOpacity, rowOpacity, footerOpacity, fontFamily, lang, charset, palette, os,&
                & mainTemplateChanged, bannerTemplateChanged, navbarTemplateChanged, footerTemplateChanged&
                &, containerTemplateChanged, cssTemplateChanged)

        end if
        if (errorText /= "No Error" ) exit

    end do
    if (errorText/="No Error") then
        errorCommand = "errorBasic"
        compiled = wordFromDict(errorCommand,Config, dicts)
        compiled = string_replace_all(compiled, "#error#", errorText)
        compiled = string_replace_all(compiled, "#number#", intToChar(lineNum))
        name="temp.txt"
        open(11, file=name, iostat=io, STATUS="replace", action="write")
        write(11, *) errorText
        close(11)
    else
        call hopeThereWontBeAnyMemoryAllocationErrors(palette, author, title, charset, keywords,&
        &description, fontfamily, lang, mainTemplateChanged, bannerTemplateChanged,&
        &navbarTemplateChanged, footerTemplateChanged, containerTemplateChanged,&
        &cssTemplateChanged, navbarOpacity, tableOpacity, rowOpacity, footerOpacity&
        ,ColorsList, RGBAList)
    end if


end subroutine
