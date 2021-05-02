module randomInteger
    implicit none

    contains

    function randInt(minN, maxN) result(numb)
        logical :: integ
        integer :: numb, minN, maxN
        real :: temp

        CALL RANDOM_NUMBER(temp)
        numb = (temp*(MaxN-MinN))+MinN

    end function


end module