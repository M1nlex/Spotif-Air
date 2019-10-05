from pip._internal import main as pipmain
from tkinter import *
from tkinter import ttk
import sqlite3
try:
    import pygame
except ModuleNotFoundError:
    pipmain(['install', 'pygame'])


def playmusic(file):

    donnee = (f'{entry1.get()}',)
    print(donnee)
    curseur.execute("SELECT lien FROM Musique WHERE Nom = ?", donnee)
    file = curseur.fetchone()[0]
    print(file)
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops=0, start=0.0)


pygame.mixer.init()
fenetre = Tk()
fenetre.title("Spotif'Air")

Player = Frame(fenetre)
Player.grid(row=0,column=0)

MusicImage = Canvas(Player,relief = 'sunken')
MusicImage.grid(row=1, rowspan=3, column=1, columnspan=3)

connexion = sqlite3.connect("basededonnees.db")
curseur = connexion.cursor()

curseur.execute("SELECT Nom FROM Musique")
resultats = curseur.fetchall()
morceau = []
for i in range(len(resultats)):
    morceau.append(resultats[i][0])




entry1 = ttk.Combobox(Player, values =morceau)
entry1.grid(row=1, column=2)


MusicTitle = Label(Player,text="temporaire")
MusicTitle.grid(row=4,column=1,columnspan=3)

PreviousMusic = Button(Player,text="Prev")
PreviousMusic.grid(row=5,column=1)

PausePlay = Button(Player,text="Pause/Play",command=lambda:playmusic(entry1.get()))
PausePlay.grid(row=5,column=2)

NextMusic = Button(Player,text="Next")
NextMusic.grid(row=5,column=3)

fenetre.mainloop()


