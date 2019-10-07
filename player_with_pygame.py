from pip._internal import main as pipmain
from tkinter import *
from tkinter import ttk
import sqlite3
try:
    import pygame
except ModuleNotFoundError:
    pipmain(['install', 'pygame'])


def playmusic():

    if pygame.mixer.music.get_busy() is False or playmusic.donnee != (f'{entry1.get()}',):
        playmusic.donnee = (f'{entry1.get()}',)
        curseur.execute("SELECT lien FROM Musique WHERE Nom = ?", playmusic.donnee)
        file = curseur.fetchone()[0]
        print(file)
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(loops=0, start=0.0)
    else:
        if playmusic.pause:
            pygame.mixer.music.unpause()
            playmusic.pause = False
        else:
            pygame.mixer.music.pause()
            playmusic.pause = True

def set_vol(val):
    volume = int(val)/100
    pygame.mixer.music.set_volume(volume)



playmusic.donnee = ''
playmusic.pause = False
pygame.mixer.init()

connexion = sqlite3.connect("basededonnees.db")
curseur = connexion.cursor()

fenetre = Tk()
fenetre.title("Spotif'Air")

Player = Frame(fenetre)
Player.grid(row=0,column=0)

volumecontrol = Scale(Player,from_=100,to=0,orient=VERTICAL,command=set_vol)
volumecontrol.set(100)
volumecontrol.grid(row=1,column=4,columnspan=3)

MusicImage = Canvas(Player,relief = 'sunken')
MusicImage.grid(row=1, rowspan=3, column=1, columnspan=3)

curseur.execute("SELECT Nom FROM Musique")
resultats = curseur.fetchall()
morceau = []
for i in range(len(resultats)):
    morceau.append(resultats[i][0])

entry1 = ttk.Combobox(Player, values =morceau)
entry1.grid(row=1, column=2)


MusicTitle = Label(Player, text="temporaire")
MusicTitle.grid(row=4, column=1, columnspan=3)

PreviousMusic = Button(Player, text="Prev")
PreviousMusic.grid(row=5, column=1)

PausePlay = Button(Player, text="Pause/Play", command=lambda: playmusic())
PausePlay.grid(row=5, column=2)

NextMusic = Button(Player, text="Next")
NextMusic.grid(row=5, column=3)

fenetre.mainloop()
