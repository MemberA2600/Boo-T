from abc import *

class Monitor_Real(ABC):
    """This the real class that is supposed to get the current
    resolution of the primary monitor."""

    @abstractmethod
    def __init__(self, system):
        if system=="Windows":
            import ctypes as ctypes

            user32 = ctypes.windll.user32
            self.__screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        else:
            from Xlib.display import Display
            screen=Display(":0").screen()
            self.__screensize=screen.width_in_pixels, screen.height_in_pixels

    @abstractmethod
    def get_screensize(self):
        return(self.__screensize)

class Monitor(Monitor_Real):
    """This is the class the user can primary access to get the resolution of the screen."""

    def __init__(self, system):
        super().__init__(system)

    def get_screensize(self):
        return(super().get_screensize())