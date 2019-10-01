from tkinter import *
from winsound import *


filename = "song/wiimusic.wav"


def playmusic(file):
    file = 'song/'+file+'.wav'
    print(file)
    PlaySound(file, SND_FILENAME | SND_ASYNC)

fenetre = Tk()
fenetre.title("Spotif'Air")

Player = Frame(fenetre)
Player.grid(row=0,column=0)

MusicImage = Canvas(Player,relief = 'sunken')
MusicImage.grid(row=1,rowspan=3,column=1,columnspan=3)

entry1 =Entry(Player)
entry1.grid(row=1,column=2)


MusicTitle = Label(Player,text="temporaire")
MusicTitle.grid(row=4,column=1,columnspan=3)

PreviousMusic = Button(Player,text="Prev")
PreviousMusic.grid(row=5,column=1)

PausePlay = Button(Player,text="Pause/Play",command=lambda:playmusic(entry1.get()))
PausePlay.grid(row=5,column=2)

NextMusic = Button(Player,text="Next")
NextMusic.grid(row=5,column=3)



fenetre.mainloop()
