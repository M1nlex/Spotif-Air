from tkinter import *
from PIL import ImageTk


def imgbouton():
    root = Tk()

    photopause= PhotoImage(file="IconsAndImages/pauseplay50.gif")
    button0 = Button(root, image=photopause)
    button0.pack()

    photonext= PhotoImage(file="IconsAndImages/buttonnext50.gif")
    button1 = Button(root, image=photonext)
    button1.pack()

    photoprevious= PhotoImage(file="IconsAndImages/buttonprevious50.gif")
    button2 = Button(root, image=photoprevious)
    button2.pack()

    root.mainloop()

def imglabel():
    root = Tk()

    photopause= PhotoImage(file="Music_Img/Kid A.gif")
    button0 = Label(root, image=photopause,relief='sunken')
    button0.pack()

    root.mainloop()

if __name__ == '__main__':
    #imgbouton()
    imglabel()
