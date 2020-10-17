from abc import *

class Monitor_Real(ABC):
    """This the real class that is supposed to get the current
    resolution of the primary monitor."""

    @abstractmethod
    def __init__(self):
        import ctypes as ctypes

        user32 = ctypes.windll.user32
        self.__screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    @abstractmethod
    def get_screensize(self):
        return(self.__screensize)

class Monitor(Monitor_Real):
    """This is the class the user can primary access to get the resolution of the screen."""

    def __init__(self):
        super().__init__()

    def get_screensize(self):
        return(super().get_screensize())