from tkinter import *
from abc import *
from tkinter.filedialog import *

class AboutMenu_REAL(ABC):

    @abstractmethod
    def __init__(self, dicts, config, hammer, master, main, fontSize, monitor):
        from PIL import ImageTk, Image


        self.__dicts = dicts
        self.__Config = config
        self.__hammerFont = hammer
        self.master = master
        self.__main = main

        self.__AboutM=Toplevel()
        self.__AboutM.title(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "about"))
        self.__AboutM.resizable(False, False)

        __monitor = monitor
        size=__monitor.get_screensize()
        __h = size[1] / 2 - 300
        if __h<100:
            __h=100
        self.__AboutM.geometry("%dx%d+%d+%d" % (400, 350, size[0]/2-200, __h))

        authorFrame=Frame(self.__AboutM, background="black", width=390, height=22)
        versionFrame=Frame(self.__AboutM, background="black", width=390, height=22)

        authorFrame.pack_propagate(False)
        versionFrame.pack_propagate(False)

        self.__gameField=Canvas(self.__AboutM, width=390, height=250, bg="black")
        self.__gameField.place(x=3, y=5)

        self.__authorLabel = Label(authorFrame, text="Fehér János Zoltán", font=(hammer[0], 14),
            fg = "white", bg="black")

        self.__versionLabel = Label(versionFrame, text=str("Boo-T v"+
            self.__Config.get_Element("version")), font=(hammer[0], 14),
            fg= "white", bg="black")

        versionFrame.place(x=5, y=260)
        authorFrame.place(x=5, y=325)

        creatorLabel=Label(self.__AboutM, text=self.__dicts.getWordFromDict(
        self.__Config.get_Element("Language"), "author"), font=(hammer[0], 14))

        self.__direction=False
        self.__theX=0
        self.__theX2=230

        self.__placeText()

        self.__sound=False

        creatorLabel.place(x=5, y=295)

        self.__resetThings("123")

        self.__AboutM.bind("<Up>", self.__upPressed)
        self.__AboutM.bind("<Down>", self.__downPressed)
        self.__AboutM.bind("<R>", self.__resetThings)
        self.__AboutM.bind("<r>", self.__resetThings)
        self.__AboutM.bind("<S>", self.__soundChange2)
        self.__AboutM.bind("<s>", self.__soundChange2)
        self.__AboutM.bind("<MouseWheel>", self.__wheel)
        self.__AboutM.bind("<Button-4>", self.__wheel)
        self.__AboutM.bind("<Button-5>", self.__wheel)


        self.__imageOff=ImageTk.PhotoImage(Image.open("icons/sound-off.png"))
        self.__imageOn=ImageTk.PhotoImage(Image.open("icons/sound-on.png"))

        self.__soundButton=Button(self.__AboutM, image=self.__imageOff, width=32, height=32, command=self.__soundChange, relief=FLAT)
        self.__soundButton.place(x=355, y=285)

        self.master.create_StatLabel(self.__dicts.getWordFromDict(self.__Config.get_Element("Language"), "wheel"))

        self.__AboutM.focus()
        self.__AboutM.after(20, self.__Animation)
        self.__AboutM.wait_window()

    def __wheel(self, event):
        if (event.delta > 0 or event.num==4):
            self.__upPressed("123")
        elif (event.delta < 0 or event.num==5):
            self.__downPressed("123")

    def __soundChange2(self, event):
        self.__soundChange()

    def __soundChange(self):
        if self.__sound==False:
            self.__sound=True
            self.__soundButton.config(image=self.__imageOn)
            self.__playsound("p/p3.wav")
        else:
            self.__sound=False
            self.__soundButton.config(image=self.__imageOff)

    def __Animation(self):
        if self.__direction==False:
            if self.__theX2==0:
                self.__direction=True
                self.__theX=295
            else:
                self.__theX2-=2
                self.__theX+=2.6

        else:
            if self.__theX2==230:
                self.__direction=False
                self.__theX=0
            else:
                self.__theX2+=2
                self.__theX-=2.6

        self.__placeText()
        self.__modifyPlayField()
        self.__AboutM.after(20, self.__Animation)

    def __modifyPlayField(self):
        self.__gameField.delete("all")
        self.__plaffieldHalf()
        self.__createElements()
        self.__moveBall()
        if self.__collisionDelay==0:
            self.__checkballCollision()
        else:
            self.__collisionDelay-=1
        self.__CPU()

    def __resetThings(self, event):
        self.__bat1XY = [30, 105]
        self.__bat2XY = [350, 105]
        self.__points = [0, 0]
        self.__resetBall()
        self.__collisionDelay=0
        self.__CPUCounter = 0
        self.__CPUMoveUnit=0

    def __resetBall(self):
        import random
        import datetime

        self.__ballXY = [190, 120]
        if self.__sound==True:
            self.__playsound("p/p1.wav")
        random.seed(int(str(datetime.datetime.now()).split(".")[1]))
        self.__ballDir=random.randint(0,7)
        self.__ballSpeed = 1

    def __plaffieldHalf(self):
        for num in range (0, 240, 20):
            self.__gameField.create_rectangle(190, 10+num , 200, 20+num, fill="white")


    def __CPU(self):
        import random
        import datetime
        random.seed(int(str(datetime.datetime.now()).split(".")[1]))
        num = random.randint(-100, 100)

        if self.__CPUCounter==0:



            if num<-90 and self.__bat2XY[1]>5:
                self.__CPUMoveUnit=-10
                self.__CPUCounter=4
            elif num>90 and self.__bat2XY[1]<205:
                self.__CPUMoveUnit=10
                self.__CPUCounter=4
            else:
                if ((self.__bat2XY[1]+20)-(self.__ballXY[1]+5))<-10:
                    self.__CPUMoveUnit = 10
                elif ((self.__bat2XY[1] + 20) - (self.__ballXY[1] + 5)) > 10:
                    self.__CPUMoveUnit = -10
                self.__CPUCounter=2
        else:
            self.__CPUCounter-=1
            if self.__bat2XY[1]>5 and self.__CPUMoveUnit==-10:
                self.__bat2XY[1] -= 10
            elif self.__bat2XY[1]<205 and self.__CPUMoveUnit==10:
                self.__bat2XY[1] += 10

    def __playsound(self, sound):
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        import pygame.mixer
        pygame.mixer.init()
        sound = pygame.mixer.Sound(sound)
        sound.play()


    def __checkballCollision(self):
        import random
        import datetime
        random.seed(int(str(datetime.datetime.now()).split(".")[1]))
        num=random.randint(-1,1)

        if self.__ballXY[1]<5:
            self.__collisionDelay = 10
            self.__ballXY[1]=5
            if self.__points[0]<15 and self.__points[1]<15 and self.__sound==True:
                self.__playsound("p/p3.wav")

            if self.__ballDir==1:
                num2 = random.randint(-3, 3)

                if num==-1:
                    self.__ballDir=4
                else:
                    self.__ballDir=3
            elif self.__ballDir==7:
                num2 = random.randint(-3, 3)

                if num==-1:
                    self.__ballDir=4
                else:
                    self.__ballDir=5
            elif self.__ballDir==0:
                num2 = random.randint(-10, 10)

                if num2<0:
                    self.__ballDir=3
                elif num2>0:
                    self.__ballDir=5
                else:
                    self.__ballDir=4


        elif self.__ballXY[1]>240:
            self.__collisionDelay = 10
            self.__ballXY[1]=240
            if self.__points[0]<15 and self.__points[1]<15 and self.__sound==True:
                self.__playsound("p/p3.wav")

            if self.__ballDir==3:
                num2 = random.randint(-3, 3)

                if num==-1:
                    self.__ballDir=0
                else:
                    self.__ballDir=7
            elif self.__ballDir==5:
                num2 = random.randint(-3, 3)

                if num==-1:
                    self.__ballDir=0
                else:
                    self.__ballDir=1
            elif self.__ballDir==4:
                num2 = random.randint(-10, 10)

                if num2<0:
                    self.__ballDir=1
                elif num2>0:
                    self.__ballDir=7
                else:
                    self.__ballDir=0

        elif (abs((self.__bat1XY[0]+5)-(self.__ballXY[0]+5))<5) and (abs((self.__bat1XY[1]+20)-(self.__ballXY[1]+5))<25):
            self.__collisionDelay = 10
            if self.__points[0]<15 and self.__points[1]<15 and self.__sound==True:
                self.__playsound("p/p3.wav")
            if ((self.__bat1XY[1]+20)-(self.__ballXY[1]+5))<-4:
                self.__ballDir=5
            elif ((self.__bat1XY[1]+20)-(self.__ballXY[1]+5))>4:
                self.__ballDir=7
            else:
                self.__ballDir=6


        elif (abs((self.__bat2XY[0]+5)-(self.__ballXY[0]+5))<5) and (abs((self.__bat2XY[1]+20)-(self.__ballXY[1]+5))<25):
            self.__collisionDelay = 10
            if self.__points[0]<15 and self.__points[1]<15 and self.__sound==True:
                self.__playsound("p/p3.wav")
            if ((self.__bat2XY[1]+20)-(self.__ballXY[1]+5))<-4:
                self.__ballDir=3
            elif ((self.__bat2XY[1]+20)-(self.__ballXY[1]+5))<4:
                self.__ballDir=1
            else:
                self.__ballDir=2


        elif self.__ballXY[0]<-10:
            if self.__points[0]<15 and self.__points[1]<15:
                self.__points[1]+=1
                self.__resetBall()

        elif self.__ballXY[0]>390:
            if self.__points[0]<15 and self.__points[1]<15:
                self.__points[0]+=1
                self.__resetBall()

    def __moveBall(self):
        self.__ballSpeed+=1
        ballMove=round(self.__ballSpeed/1000)+2
        if self.__ballDir==0:
            self.__ballXY[1]-=ballMove
        elif self.__ballDir == 1:
            self.__ballXY[0] -= ballMove
            self.__ballXY[1] -= ballMove
        elif self.__ballDir == 2:
            self.__ballXY[0] -= ballMove
        elif self.__ballDir == 3:
            self.__ballXY[0] -= ballMove
            self.__ballXY[1] += ballMove
        elif self.__ballDir == 4:
            self.__ballXY[1] += ballMove
        elif self.__ballDir == 5:
            self.__ballXY[0] += ballMove
            self.__ballXY[1] += ballMove
        elif self.__ballDir == 6:
            self.__ballXY[0] += ballMove
        else:
            self.__ballXY[0] += ballMove
            self.__ballXY[1] -= ballMove

    def __createElements(self):
        self.__gameField.create_rectangle(self.__bat1XY[0], self.__bat1XY[1], self.__bat1XY[0]+10, self.__bat1XY[1]+40, fill="white")
        self.__gameField.create_rectangle(self.__bat2XY[0], self.__bat2XY[1], self.__bat2XY[0]+10, self.__bat2XY[1]+40, fill="white")
        self.__gameField.create_rectangle(self.__ballXY[0], self.__ballXY[1], self.__ballXY[0]+10, self.__ballXY[1]+10, fill="white")

        scoreFont=[self.__hammerFont[0], 40, "bold"]

        self.__gameField.create_text(155,30,fill="white",font=scoreFont,
                        text="{:2}".format(self.__points[0]))

        self.__gameField.create_text(235,30,fill="white",font=scoreFont,
                        text="{:2}".format(self.__points[1]))

    def __upPressed(self, event):
        if self.__bat1XY[1]>5:
            self.__bat1XY[1]-=10

    def __downPressed(self, event):
        if self.__bat1XY[1]<205:
            self.__bat1XY[1]+=10

    def __placeText(self):
        self.__versionLabel.place(x=self.__theX, y=-3)
        self.__authorLabel.place(x=self.__theX2, y=-3)


class AboutMenu(AboutMenu_REAL):

    def __init__(self, dicts, config, hammer, master, main, fontSize, monitor):
        super().__init__(dicts, config, hammer, master, main, fontSize, monitor)
