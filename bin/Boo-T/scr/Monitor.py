class Monitor():
    """This the real class that is supposed to get the current
    resolution of the primary monitor."""

    def __init__(self, system):
        """Has different methods to get the main monitor's metrics on the two OS."""

        if system=="Windows":
            from ctypes import windll as windll

            user32 = windll.user32
            self.__screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        else:
            from Xlib.display import Display
            screen=Display(":0").screen()
            self.__screensize=screen.width_in_pixels, screen.height_in_pixels

    def get_screensize(self):
        return(self.__screensize)