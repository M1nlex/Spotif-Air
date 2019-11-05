from pip._internal import main as pipmain
from tkinter import *
from tkinter import ttk
import time
import threading
import sqlite3

try:
    import pygame

except ModuleNotFoundError:
    pipmain(['install', 'pygame'])


def playmusic():

    if pygame.mixer.music.get_busy() == 0 or playmusic.donnee != (f'{entry1.get()}',):
        scaletime.set(0)
        MusicTitle.config(text=entry1.get())
        playmusic.donnee = (f'{entry1.get()}',)
        curseur.execute("SELECT lien FROM Musique WHERE Nom = ?", playmusic.donnee)
        file = curseur.fetchone()[0]
        print(file)
        pygame.mixer.music.load(file)
        a = pygame.mixer.Sound(file).get_length()
        scaletime.config(to=a)
        pygame.mixer.music.play(loops=0, start=set_time.starttime)
        t1 = threading.Thread(target=musiquetime)
        t1.start()
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


def set_time(val):
    pygame.mixer.music.stop()
    set_time.starttime = float(val)
    playmusic.donnee = (f'{entry1.get()}',)
    curseur.execute("SELECT lien FROM Musique WHERE Nom = ?", playmusic.donnee)
    file = curseur.fetchone()[0]
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops=0, start=set_time.starttime)
    t1 = threading.Thread(target=musiquetime)
    t1.start()

def musiquetime():
    while pygame.mixer.music.get_busy():
        currenttime.set(float(pygame.mixer.music.get_pos()/1000)+set_time.starttime)
        time.sleep(0.1)

def afficherFrameIntro():

    FrameIntro.grid(row=1,column=0,columnspan=2)

def afficherPlayer():
    Player.grid(row=1,column=0,columnspan=2)


set_time.starttime = 0
playmusic.donnee = ''
playmusic.pause = False
pygame.mixer.init()

connexion = sqlite3.connect("basededonnees.db")
curseur = connexion.cursor()

fenetre = Tk()
fenetre.title("Spotif'Air")

ButtonafficherFrameIntro = Button(fenetre,text="Intro",command=lambda:FrameIntro.tkraise())
ButtonafficherFrameIntro.grid(row=0,column=0)

ButtonafficherPlayer = Button(fenetre,text="Player",command=lambda:Player.tkraise())
ButtonafficherPlayer.grid(row=0,column=1)

#-------------------------------------------------------------------Accueil-------------------------------------------------------------------------------

FrameIntro = Frame(fenetre)
FrameIntro.grid(row=1, column=0, columnspan=2, sticky='nsew')

Label123 = Label(FrameIntro, text="voila c'est un test")
Label123.grid(row=0, column=0)

#--------------------------------------------------------------------Player-------------------------------------------------------------------------

Player = Frame(fenetre)
Player.grid(row=1, column=0,columnspan=2)


volumecontrol = Scale(Player, from_=100, to=0, orient=VERTICAL, command=set_vol)
volumecontrol.set(100)
volumecontrol.grid(row=1, column=4, columnspan=3)

MusicImage = Canvas(Player,relief = 'sunken')
MusicImage.grid(row=1, rowspan=3, column=1, columnspan=3)

curseur.execute("SELECT Nom FROM Musique")
resultats = curseur.fetchall()
morceaux = []
for i in range(len(resultats)):
    morceaux.append(resultats[i][0])
currenttime = IntVar()

entry1 = ttk.Combobox(Player, values =morceaux)
entry1.grid(row=1, column=2)

scaletime = Scale(Player, orient='horizontal', from_=0, to=360, resolution=0.1, length=350, label='time', variable=currenttime, command=set_time)
scaletime.grid(row=3, column=1, columnspan=3)

MusicTitle = Label(Player, text="Spotif-Air")
MusicTitle.grid(row=4, column=1, columnspan=3)

MusicTime = Label(Player, textvariable=currenttime)
MusicTime.grid(row=4, column=3, columnspan=3)

PreviousMusic = Button(Player, text="Prev")
PreviousMusic.grid(row=5, column=1)

PausePlay = Button(Player, text="Pause/Play", command=lambda: playmusic())
PausePlay.grid(row=5, column=2)

NextMusic = Button(Player, text="Next")
NextMusic.grid(row=5, column=3)

fenetre.mainloop()
