module OS_func
    use list
    use file_func
    use string_func
    implicit none

    private
    public :: getFilesFromSubFolder, getSep, getFileNameFromPath, getLineSep,&
             &getFilesFromSubFolderLinux

    contains

    function getFilesFromSubFolder(os, dir) result(array)
        character(:), allocatable :: os, dir
        character(1000), dimension(:), allocatable :: array

        if (os == "Windows") then
            array = getFilesFromSubFolderWin(dir)
        else
            array = getFilesFromSubFolderLinux(dir)

        end if

    end function

    function getFilesFromSubFolderWin(dir) result(array)
        character(:), allocatable :: dir, command, path
        character(10000), dimension(:), allocatable :: array, array2
        integer :: alloc, num

        call system(command="dir "//dir//" /s /b /o:gn>filelist.txt")
        path = "filelist.txt"
        array2 = loadLines(path)

        allocate(array(size(array2)-1), stat=alloc)
        call system(command="del filelist.txt")
        !allocate(array(1), stat=alloc)
        do num = 1, size(array2)-1, 1
            array(num) = array2(num)
        end do

    end function

    function getFilesFromSubFolderLinux(dir) result(array)
        character(:), allocatable :: dir, command, path
        character(10000), dimension(:), allocatable :: array, array2
        integer :: alloc, num

        call system(command="ls -R "//dir//" >filelist.txt")
        path = "filelist.txt"
        array2 = loadLines(path)
        allocate(array(size(array2)-1), stat=alloc)
        do num = 1, size(array), 1
            array(num) = dir//"/"//array2(num+1)
        end do
        call system(command="rm filelist.txt")

    end function

    function getSep(os_name) result(sep)
        character(len=:), allocatable :: os_name
        character(1) :: sep

        if (os_name=="Windows") then
            sep="\"
        else
            sep="/"
        end if

    end function

    function getLineSep(os_name) result(sep)
        character(len=:), allocatable :: os_name
        character(:), allocatable :: sep

        if (os_name=="Windows") then
            sep=achar(13)//achar(10)
        else
            sep=achar(10)
        end if
        sep = trim(sep)
    end function

    function getFileNameFromPath(path, os, ext) result(filename)
        character(:), allocatable :: path, filename, os
        logical :: ext
        character(100), dimension(:), allocatable :: parts
        !Ext is about if you want to have the extension or don't.

        parts = split(path, getSep(os), 99999)
        filename = parts(size(parts))
        if (ext .EQV. .FALSE.) then
            parts = split(filename, ".", 2)
            filename = parts(1)
        end if

    end function

end module
