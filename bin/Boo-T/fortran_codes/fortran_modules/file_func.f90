module file_func
    implicit none

    private
    public :: loadText, loadLines, saveLines, saveText, arrayToText, textToArray, arrayToTextWithoutNewLines

    contains

    function loadText(path) result(text)
        character(len=:, kind=1), allocatable :: path, text
        character(len=10000, kind=1), dimension(:), allocatable :: array
        integer :: lastChar, io

        array = load(path)
        text = arrayToText(array)
        !write(*,*) path, "::", len(text), "::", text(len(text)-10: len(text))
        lastChar = getTheLastChar(text)
        text=text(1:lastChar)
    end function

    function getTheLastChar(text) result(lastChar)
        integer :: num, lastChar
        character(:), allocatable :: text


        lastChar=1
        do num=1,len_trim(text), 1
            if (ichar(text(num:num))>32 .AND. ichar(text(num:num))<127) lastChar=num

        end do

    end function


    function loadLines(path) result(array)
        character(len=:, kind=1), allocatable :: path
        character(len=10000, kind=1), dimension(:), allocatable :: array

        array = load(path)

    end function

    function load(path) result(array)
        character(len=:, kind=1), allocatable :: path
        character(len=10000, kind=1), dimension(:), allocatable :: array
        integer :: io, lineNumber, alloc, num
        logical :: exists

        inquire(file=path, exist=exists)
        if (exists .EQV. .FALSE.) then
            write(*,"(A,A,A)") "File(", path, ") does not exist!"
            allocate(array(0), stat=alloc)
        else
            lineNumber=checkLines(path)
            allocate(array(lineNumber), stat=alloc)
            open(UNIT=11, FILE=path, iostat=io, STATUS="old", action="read")
            do num = 1, lineNumber, 1
                read(11, "(A)", iostat=io) array(num)
            end do

            close(11)

        end if

    end function

    function checkLines(path) result(lineNumber)
        character(len=:), allocatable :: path
        integer :: io, lineNumber
        character(len=:), allocatable :: temp

        open(UNIT=11, FILE=path, iostat=io, STATUS="old", action="read")
        lineNumber=1
        do
            read(11,"(A)", iostat=io) temp
            if (io/=0) exit
            lineNumber = lineNumber + 1
        end do
        close(11)

    end function

    function arrayToText(array) result(text)
        character(len=:, kind=1), allocatable :: text
        character(len=10000, kind=1), dimension(:), allocatable :: array
        integer :: num

        text=""

        do num=1, size(array), 1
            text = text//trim(array(num))//achar(13)//achar(10)

        end do

    end function

    function arrayToTextWithoutNewLines(array) result(text)
        character(len=:, kind=1), allocatable :: text
        character(len=10000, kind=1), dimension(:), allocatable :: array
        integer :: num

        text=""

        do num=1, size(array), 1
            text = text//trim(array(num))

        end do

    end function

    subroutine saveLines(path, array)
        character(len=:, kind=1), allocatable :: path
        character(len=10000, kind=1), dimension(:), allocatable :: array
        integer :: io, num

        open(UNIT=11, FILE=path, iostat=io, STATUS="replace", action="write")
        do num = 1, size(array), 1
            write(11, *) trim(array(num))
        end do
        close(11)
    end subroutine

    subroutine saveText(path, string)
        character(len=:, kind=1), allocatable :: string, path
        integer :: io

        open(UNIT=11, FILE=path, iostat=io, STATUS="replace", action="write")
        write(*,*) trim(string)
        close(11)

    end subroutine

    function textToArray(string) result(array)
        character(len=10000, kind=1), dimension(:), allocatable :: array
        character(len=:, kind=1), allocatable :: string
        integer :: lines, alloc, num, line_num, charnum

        lines = countNewLines(string)
        allocate(array(lines), stat=alloc)

        line_num = 1
        charnum=1
        do num = 1, len_trim(string), 1
            if (charnum==1) array(line_num) = ""
            if (ichar(string(num:num))==10) then
                line_num = line_num + 1
                charnum=1
            else
                array(line_num)(charnum:charnum) = string(num:num)
                charnum = charnum + 1
            end if
        end do

    end function

    function countNewLines(string) result(lines)
        character(len=:, kind=1), allocatable :: string
        integer :: lines, num

        lines = 0
        do num = 1 , len_trim(string), 1
            if (ichar(string(num:num))==10) lines = lines + 1
        end do

    end function
end module
