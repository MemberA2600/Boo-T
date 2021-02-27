module dict
    use list
    implicit none

    private
    public :: Dictionary, DictConstructor, AddDict, GetDict, RemoveDict
    public :: GetKeys, containsKey, containsValue, GetSizeDict, SetKey
    public :: GetAsInt, GetAsReal

    type Dictionary
        type(CharList) :: keys, values

        contains
            procedure :: create => DictConstructor          !Call this as you declared the dict!
            procedure :: add => AddDict                     !Add a key and a value, if key exists, overrites key's value
            procedure :: get => GetDict                     !Get value of key
            procedure :: remove => RemoveDict               !Remove a key and it's value
            procedure :: getKeys => GetKeys                 !Get keys as array
            procedure :: getValues => GetValues             !Get values as array
            procedure :: containsKey => containsKey         !Returns if key exits
            procedure :: containsValue => containsValue     !Returns if value exists
            procedure :: getSize => GetSizeDict             !Gets size of dict
            procedure :: set => SetKey                      !Sets value of key
            procedure :: getAsInt => GetAsInt               !Returns value as integer
            procedure :: getAsReal => GetAsReal             !Returns value as real

    end type

    contains

    subroutine DictConstructor(this)
        class(Dictionary), intent(inout) :: this

        call this%keys%create()
        call this%values%create()
    end subroutine

    subroutine SetKey(this, key, value)
        class(Dictionary), intent(inout) :: this
        character(:), allocatable :: key, value

        call this%values%set(value, this%keys%indexOf(key))
    end subroutine

    subroutine AddDict(this, key, value)
        class(Dictionary), intent(inout) :: this
        character(:), allocatable :: key, value

        if (this%keys%containsItem(key).EQV..FALSE.) then
            call this%keys%add(key)
            call this%values%add(value)
        else
            call SetKey(this, key, value)
        end if
    end subroutine

    function GetDict(this, key) result(value)
        class(Dictionary) :: this
        character(:), allocatable :: key, value

        value=this%values%get(this%keys%indexOf(key))
    end function

    subroutine RemoveDict(this, key)
        class(Dictionary), intent(inout) :: this
        character(:), allocatable :: key, value

        call this%values%removeByNum(this%keys%indexOf(key))
        call this%keys%removeByName(key)
    end subroutine

    function GetKeys(this) result(array)
        class(Dictionary) :: this
        character(len=10000, kind=1), dimension(:), allocatable :: array

        array = this%keys%getAll()
    end function

    function GetValues(this) result(array)
        class(Dictionary) :: this
        character(len=10000, kind=1), dimension(:), allocatable :: array

        array = this%values%getAll()
    end function

    function containsKey(this, key) result(bool)
        class(Dictionary) :: this
        character(:), allocatable :: key
        logical :: bool

        bool = this%keys%containsItem(key)

    end function

    function containsValue(this, value) result(bool)
        class(Dictionary) :: this
        character(:), allocatable :: value
        logical :: bool

        bool = this%values%containsItem(value)

    end function

    function GetSizeDict(this) result(s)
        class(Dictionary) :: this
        integer :: s

        s = this%keys%getSize()

    end function

    function GetAsInt(this, key) result(intValue)
        class(Dictionary) :: this
        character(:), allocatable :: key
        integer :: intValue

        intValue = this%values%char2Int(this%values%get(this%keys%indexOf(key)))

    end function

        function GetAsReal(this, key) result(realValue)
        class(Dictionary) :: this
        character(:), allocatable :: key
        real :: realValue

        realValue = this%values%char2Real(this%values%get(this%keys%indexOf(key)))

    end function


end module
