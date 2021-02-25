module string_func

    implicit none

    contains

    function string_replace(string, original, new) result(new_string)
        character(LEN=*, kind=1) :: string, original, new
        character(LEN=len(string)+len(new), kind=1) :: new_string
        integer :: x1, x2
        logical :: found_it

        found_it = .FALSE.;

        do x1 = 1, len(string)-len(original), 1
            x2 = x1+len(original)-1
            if (string(x1:x2)==original) then
                    found_it = .TRUE.
                    exit
            end if
        end do

        if (found_it .EQV. .FALSE.) then
            new_string = string
        else
            new_string = string(1:x1-1)//new//string(x2+1:len_trim(string))
        end if
    end function

    function string_replace_all(string, original, new) result(new_string)
        character(LEN=*, kind=1) :: string, original, new
        character(LEN=len(string)+len(new), kind=1) :: new_string
        integer :: x1, x2, dif

        !dif = len(new) - len(original)
        new_string = string
        x1=1
        x2=x1+len(original)-1

        do while(x2<len(new_string))
            x2 = x1+len(original)-1
            if (new_string(x1:x2) == original) then
                new_string = new_string(1:x1-1)//new//new_string(x2+1:len(new_string))
                !x1 = x1 - dif

            end if
            x1 = x1 + 1

        end do
    end function


    function startswith(string, start) result(isIt)
        character(len=*, kind=1) string, start
        logical :: isIt

        isIt = .FALSE.
        if (string(1:len(start)) == start) isIt = .TRUE.

    end function

    function endswith(string, ender) result(isIt)
        character(len=*, kind=1) string, ender
        logical :: isIt

        isIt = .FALSE.
        if (trim(string(len(string)-len(ender)+1:len(string))) == trim(ender)) isIt = .TRUE.

    end function

    function split(string, deliminator, maximum) result(temp_array)
        character(len=*, kind=1) :: string, deliminator
        character(len=len(string), kind=1), dimension(:), allocatable :: temp_array
        integer :: num, x1, x2, alloc_stat, maximum, PrevPoint, delay

        num = 1

        do x1 = 1, len(string), 1
            x2 = x1+len(deliminator)-1
            if (string(x1:x2)==deliminator) then
                num=num+1
            endif
            if (num==maximum) exit
        end do

        !allocate(character(longest)::temp_array%array(num), stat = alloc_stat)
        !write(*,*) size(temp_array%array)
        allocate(temp_array(num), stat=alloc_stat)

        num = 1
        PrevPoint = 1
        delay = 0
        do x1 = 1, len(string), 1
            x2 = x1+len(deliminator)-1
            if (delay>0) then
                delay = delay - 1
                cycle
            end if
            if (string(x1:x2)==deliminator) then
                temp_array(num) = string(PrevPoint:x1-1)

                PrevPoint = x1 + len(deliminator)
                delay = len(deliminator) - 1
                num = num + 1
            end if
        end do

        temp_array(num) = string(PrevPoint:len(string))

    end function

    function splitBySpaces(string, maximum) result(temp_array)
        character(:), allocatable :: string
        integer :: maximum, x1, x2, num, theSize, wordNum, alloc
        character(10000), dimension(:), allocatable :: temp_array
        logical :: newWord

        newWord = .TRUE.
        x1 = 1
        x2 = 1
        theSize = 0

        do num = 1, len(string), 1
            if (string(num:num) == " ") then
                if (newWord .EQV. .FALSE.) then
                    theSize = theSize +1
                end if
                newWord = .TRUE.
            else
                if (newWord .EQV. .TRUE.) then
                    x1 = num
                    x2 = num
                    newWord = .FALSE.
                else
                    x2 = num
                end if
            end if
        end do

        newWord = .TRUE.
        x1 = 1
        x2 = 1
        wordNum = 1

        if (theSize>maximum) theSize = maximum
        allocate(temp_array(theSize), stat=alloc)

        do num = 1, len(string), 1
            if (string(num:num) == " ") then
                if (newWord .EQV. .FALSE.) then
                    if (wordNum<theSize) then
                        temp_array(wordNum) = trim(string(x1:x2))
                        wordNum = wordNum +1
                    else
                        temp_array(wordNum) = trim(string(x1:len(string)))
                        exit
                    end if
                end if
                newWord = .TRUE.
            else
                if (newWord .EQV. .TRUE.) then
                    x1 = num
                    x2 = num
                    newWord = .FALSE.
                else
                    x2 = num
                end if
            end if
        end do
    end function

    function upper(s) result(s2)
        character(len=*, kind=1) :: s
        character(len=:, kind=1), allocatable :: s2
        integer :: num

        s2=s
        do num=1, len_trim(s), 1
            if (ichar(s(num:num))>96 .AND. ichar(s(num:num))<123) then
                s2(num:num) = char(ichar(s(num:num))-32)

            end if
        end do
    end function

    function lower(s) result(s2)
        character(len=*, kind=1) :: s
        character(len=:, kind=1), allocatable :: s2
        integer :: num

        s2=s
        do num=1, len_trim(s), 1
            if (ichar(s(num:num))>64 .AND. ichar(s(num:num))<91) then
                s2(num:num) = char(ichar(s(num:num))+32)

            end if
        end do
    end function

    function findAll(s, pattern) result(array)
        integer :: num, len_of_pattern, x1, x2, len_of_array, num2, i, alloc, array_num
        character(len=:, kind=1), allocatable :: s, pattern
        character(len=len(pattern), kind=1), dimension(:), allocatable :: array
        logical :: patternMatch
        character(len=:), allocatable :: temp_s

        !! Because of the easier syntax check, it's not the same as classic regex!
        !! \d = digit
        !! \c = character
        !! \s = space
        !! \t = tab
        !! \n = newline
        !! \r = return
        !! \\ = backslash
        !! \? = anything

        len_of_pattern = 0
        len_of_array=0
        num=1

        do while (num<=len(pattern))
            if (pattern(num:num)=="\") then
                if (pattern(num:num)=="\" .AND. num<len(pattern)) then
                    if (pattern(num+1:num+1)=="d"&
                    & .OR. pattern(num+1:num+1)=="c"&
                    & .OR. pattern(num+1:num+1)=="s"&
                    & .OR. pattern(num+1:num+1)=="t"&
                    & .OR. pattern(num+1:num+1)=="n"&
                    & .OR. pattern(num+1:num+1)=="r"&
                    & .OR. pattern(num+1:num+1)=="\"&
                    & .OR. pattern(num+1:num+1)=="?") num=num+1

                end if

            end if
            num=num+1
            len_of_pattern = len_of_pattern+1

        end do

        array_num=1

        do i=1, 2, 1
            do x1 = 1, len(s)-len_of_pattern+1, 1
                x2=x1+len_of_pattern
                temp_s = s(x1:x2-1)
                patternMatch = .TRUE.
                num=1
                num2=1
                do while (num<=len(pattern))
                    if (pattern(num:num)=="\" .AND. num<len(pattern)) then
                        num=num+1


                        if (pattern(num:num)=="d") then
                            if (ichar(temp_s(num2:num2))<48 .OR. ichar(temp_s(num2:num2))>57) patternMatch=.FALSE.

                        else if (pattern(num:num)=="c") then
                            if (ichar(temp_s(num2:num2))<65 .OR. ichar(temp_s(num2:num2))>90 .AND.&
                            & ichar(temp_s(num2:num2))<97 .OR. ichar(temp_s(num2:num2))>122) patternMatch=.FALSE.

                        else if (pattern(num:num)=="s") then
                            if (ichar(temp_s(num2:num2))/=32) patternMatch=.FALSE.

                        else if (pattern(num:num)=="t") then
                            if (ichar(temp_s(num2:num2))/=9) patternMatch=.FALSE.

                        else if (pattern(num:num)=="n") then
                            if (ichar(temp_s(num2:num2))/=10) patternMatch=.FALSE.

                        else if (pattern(num:num)=="r") then
                            if (ichar(temp_s(num2:num2))/=13) patternMatch=.FALSE.

                        else if (pattern(num:num)=="\") then
                            if (ichar(temp_s(num2:num2))/=92) patternMatch=.FALSE.

                        else if (pattern(num:num)=="?") then
                            !! Do nothing
                        else
                            patternMatch=.FALSE.
                        end if
                    else
                        if (pattern(num:num)/=temp_s(num2:num2)) patternMatch=.FALSE.
                    end if
                    num=num+1
                    num2=num2+1
                    if (patternMatch .EQV. .FALSE.) exit
                end do

                if (patternMatch .EQV. .TRUE.) then
                    if (i==1) then
                        len_of_array = len_of_array+1
                    else

                        array(array_num) = temp_s
                        array_num=array_num+1
                    end if
                end if
            end do
            if (.NOT. allocated(array)) allocate(array(len_of_array), stat=alloc)

        end do

    end function

    function sort(array_in, i) result(array_out)
        integer :: i
        character(len=i, kind=1), dimension(:), allocatable :: array_in
        character(len=i, kind=1), dimension(:), allocatable :: array_out
        integer :: alloc, start, ind, num, modified, charindex, charvalue
        character(len=i, kind=1) :: temp, temp2

        allocate(array_out(size(array_in)), stat=alloc)
        array_out = array_in

        start=1
        do while (start<=size(array_out))
            ind=start
            temp=""
            charindex=2147483647
            do num = start, size(array_out), 1

                if (ichar(array_out(num)(1:1))>64 .AND. ichar(array_out(num)(1:1))<91) then
                    charvalue = ichar(array_out(num)(1:1))-55
                else if (ichar(array_out(num)(1:1))>96 .AND. ichar(array_out(num)(1:1))<123) then
                    charvalue = ichar(array_out(num)(1:1))-87
                else if (ichar(array_out(num)(1:1))>47 .AND. ichar(array_out(num)(1:1))<58) then
                    charvalue = ichar(array_out(num)(1:1))-48
                else
                    charvalue = ichar(array_out(num)(1:1))+60

                end if

                if (charvalue<charindex) then
                    charindex=charvalue
                    ind = num
                    temp= array_out(num)

                end if
            end do

            if (ind/=start) then
                temp2 = array_out(start)
                array_out(start) = temp
                array_out(ind) = temp2
            end if
            start=start+1
        end do
    end function

    function charToInt(c) result(i)
        character(len=*) :: c
        integer :: i

        read(c, *) i

    end function

    function intToChar(i) result(c)
        character(len=10000) :: c_temp
        character(len=:), allocatable :: c
        integer :: i

        write(c_temp, "(I0)") i
        c = trim(c_temp)

    end function

    function charToReal(c) result(r)
        character(len=*) :: c
        real :: r

        read(c, *) r

    end function

    function realToChar(r) result(c)
        character(len=10000) :: c_temp
        character(len=:), allocatable :: c
        real :: r
        integer :: num

        write(c_temp, "(F0.12)") r
        if (c_temp(1:1) == ".") c_temp = "0"//c_temp
        do num = len_trim(c_temp), 1, -1
            if (c_temp(num:num) == "0") c_temp(num:num) = " "
            if (c_temp(num:num) == ".") exit
        end do

        c = trim(c_temp)

    end function


    function arrayJoin(array, ch, start, ender) result(string)
        character(10000), dimension(:), allocatable :: array
        character(:), allocatable :: string, ch
        integer :: num, start, ender, templinenum

        !Creates a string from array, joining from start to ender with c between.

        string = trim(array(start))

        do num = start+1, ender, 1
            string = string//ch//trim(array(num))

        end do

    end function

    function removeBlankLinesFromArray(arrayIn) result(arrayOut)
        character(10000), dimension(:), allocatable :: arrayIn, arrayOut
        integer :: num, linenum, alloc

        linenum = 0
        do num=1, size(arrayIn), 1
            if (len_trim(arrayIn(num))>0) linenum = linenum +1
        end do

        allocate(arrayOut(linenum), stat=alloc)
        linenum = 1
        do num=1, size(arrayIn), 1
            if (len_trim(arrayIn(num))>0) then
                arrayOut(linenum) = arrayIn(num)
                linenum = linenum + 1
            end if
        end do

    end function

end module
