from tkinter import *
from winsound import *
from tkinter import ttk
import sqlite3

filename = "song/wiimusic.wav"


def playmusic(file):

    donnee = (f'{entry1.get()}',)
    print(donnee)
    curseur.execute("SELECT lien FROM Musique WHERE Nom = ?", donnee)
    file = curseur.fetchone()[0]
    print(file)
    PlaySound(file, SND_FILENAME | SND_ASYNC)

connexion = sqlite3.connect("basededonnees.db")
curseur = connexion.cursor()

fenetre = Tk()
fenetre.title("Spotif'Air")

Player = Frame(fenetre)
Player.grid(row=0,column=0)

volumecontrol = Scale()

MusicImage = Canvas(Player,relief = 'sunken')
MusicImage.grid(row=1, rowspan=3, column=1, columnspan=3)



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
