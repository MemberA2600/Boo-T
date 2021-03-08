from tkinter import *

class DisplayLoading():
    """This class only opens a loading screen image and swaits for 3 seccnds,
    then destroys the window and then goes back to the main window."""

    def __init__(self, size):
        from PIL import ImageTk, Image

        if size[0]>1268 and size[1]>768:
            self.__w_Size=800
        else:
            self.__w_Size=640

        self.__h_Size=round((self.__w_Size/800)*300)
        self.__Loading_Window=Toplevel()
        self.__Loading_Window.geometry("%dx%d+%d+%d" % (self.__w_Size, self.__h_Size,
                                                        (size[0]/2)-self.__w_Size/2,
                                                        (size[1]/2)-self.__h_Size/2-50))
        self.__Loading_Window.overrideredirect(True)
        self.__Loading_Window.resizable(False, False)
        self.__Img = ImageTk.PhotoImage(Image.open("loading.png").resize((self.__w_Size,self.__h_Size)))

        self.__ImgLabel = Label(self.__Loading_Window, image=self.__Img)
        self.__ImgLabel.pack()

        self.__Loading_Window.after(3500, self.destroy_loader)
        self.__Loading_Window.wait_window()


    def destroy_loader(self):
        self.__Loading_Window.destroy()
