from pip._internal import main as pipmain
from tkinter import *
from tkinter import ttk
import time
import threading
import sqlite3
from tkinter import font
import random

try:
    import pygame

except ModuleNotFoundError:
    pipmain(['install', 'pygame'])

global threadkill
threadkill = False


#----------------------------------------------Requêtes------------------------------------------------------------

sql_music = "SELECT Music_Link FROM Musique WHERE Music_Name = ?"
sql_image = "SELECT Image.Image_Link FROM Image,Musique WHERE ( Image.Image_Id = Musique.Image_Id AND Musique.Music_Name = ? )"
sql_list_music = "SELECT Music_Name FROM Musique"

# ---------------------------------------------fonctions----------------------------------------------------------------


def resize(event):
    width = int(fenetre.winfo_width())
    resize.font = font.Font(size=int(fenetre.winfo_width()/13))
    Label123.config(font=resize.font)


def playmusic():

    if (f'{entry1.get()}' == ""):
        entry1.set(random.choice(morceaux))

    if pygame.mixer.music.get_busy() == 0 or playmusic.donnee != (f'{entry1.get()}',):
        scaletime.set(0)
        MusicTitle.config(text=entry1.get())
        playmusic.donnee = (f'{entry1.get()}',)
        curseur.execute(sql_music, playmusic.donnee)
        file = curseur.fetchone()[0]

        # Changement image album
        curseur.execute(sql_image, playmusic.donnee)
        Lien_img = curseur.fetchone()[0]
        music_img = PhotoImage(file=Lien_img)
        canvasimage.delete(image_on_canvas)
        canvasimage.create_image(20,20,anchor=NW,image=music_img)
        canvasimage.image = music_img

        # Lancement musique
        pygame.mixer.music.load(file)
        playmusic.a = pygame.mixer.Sound(file).get_length()
        scaletime.config(to=playmusic.a)
        pygame.mixer.music.play(loops=0, start=set_time.starttime)
        t1 = threading.Thread(target=lambda : musiquetime(playmusic.a))
        t1.start()
    else:
        if playmusic.pause:
            pygame.mixer.music.unpause()
            cursortime(currenttime.get())
            playmusic.pause = False
        else:
            pygame.mixer.music.pause()
            playmusic.pause = True


def set_vol(val):
    volume = int(val)/100
    pygame.mixer.music.set_volume(volume)

def cursortime(val):
    #print(val, currenttime.get())
    global threadkill
    threadkill = 3


def set_time(val):
    global threadkill
    pygame.mixer.music.stop()
    set_time.starttime = float(val)
    playmusic.donnee = (f'{entry1.get()}',)
    curseur.execute(sql_music, playmusic.donnee)
    file = curseur.fetchone()[0]
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops=0, start=set_time.starttime)
    t1 = threading.Thread(target=lambda: musiquetime(playmusic.a))
    t1.start()

def musiquetime(a):
    global threadkill

    while pygame.mixer.music.get_busy():
        currenttime.set(format(float(pygame.mixer.music.get_pos()/1000)+set_time.starttime, '.0f'))
        time.sleep(0.1)
        #print(a, currenttime.get(), threadkill)
        if int(a) == currenttime.get():
            print('next')
            Nextinplaylist()
            break
        if threadkill == 4:
            break
        if threadkill == 1:
            threadkill = False
            Nextinplaylist()
            break
        if threadkill == 2:
            threadkill = False
            Previousinplaylist()
            break
        if threadkill == 3:
            threadkill = False
            set_time(scaletime.get())
            break

def next():
    global threadkill
    threadkill = 1

def previous():
    global threadkill
    threadkill = 2


def Nextinplaylist():
    entry1.current((entry1.current()+1) % 8)
    playmusic()
    set_time(0)

def Previousinplaylist():
    entry1.current((entry1.current()-1) % 8)
    playmusic()
    set_time(0)

# ----------------------------------------------------------INTERFACE---------------------------------------------------


set_time.starttime = 0
playmusic.donnee = ''
playmusic.pause = False
pygame.mixer.init()

connexion = sqlite3.connect("basededonnees.db", check_same_thread=False)
curseur = connexion.cursor()

fenetre = Tk()
fenetre.title("Spotif'Air")

FrameButton = Frame(fenetre,relief='raise',bg='blue',bd=5)
FrameButton.grid(row=0,column=0,columnspan=5,sticky='ew')

ButtonafficherFrameIntro = Button(FrameButton, text="Intro", command=lambda:FrameIntro.tkraise())
ButtonafficherFrameIntro.pack(side="left",expand="True",fill="x")

ButtonafficherPlayer = Button(FrameButton, text="Player", command=lambda:Player.tkraise())
ButtonafficherPlayer.pack(side="left",expand="True",fill="x")

ButtonafficherRecherche = Button(FrameButton, text="Recherche", command=lambda:FrameRecherche.tkraise())
ButtonafficherRecherche.pack(side="left",expand="True",fill="x")

# -------------------------------------------------------------------Accueil-------------------------------------------------------------------------------

FrameIntro = Frame(fenetre)
FrameIntro.grid(row=1, column=0, columnspan=2, sticky='nsew')

Label123 = Label(FrameIntro, text="Welcome on Spotif'air", anchor='center')
Label123.grid(row=0, column=0, sticky='nsew')

# -------------------------------------------------------------------Recherche-------------------------------------------------------------------------------

FrameRecherche = Frame(fenetre)
FrameRecherche.grid(row=1, column=0, columnspan=2, sticky='nsew')

Label223 = Label(FrameRecherche, text="Recherche", anchor='center')
Label223.grid(row=0, column=0, sticky='nsew')

curseur.execute(sql_list_music)
resultats = curseur.fetchall()
morceaux = []
for i in range(len(resultats)):
    morceaux.append(resultats[i][0])
currenttime = IntVar()

entry1 = ttk.Combobox(FrameRecherche, values =morceaux)
entry1.grid(row=1, column=0)

# --------------------------------------------------------------------Player-------------------------------------------------------------------------

Player = Frame(fenetre)
Player.grid(row=1, column=0,columnspan=2, sticky='nsew')


volumecontrol = Scale(Player, from_=100, to=0, orient=VERTICAL, command=set_vol)
volumecontrol.set(100)
volumecontrol.grid(row=1, column=4,columnspan=5)

FrameImage = Frame(Player, height=300, width=250)
FrameImage.grid(row=1, rowspan=3, column=1, columnspan=3, sticky='nsew')
FrameImage.grid_propagate(0)
music_img = PhotoImage(file="IconsAndImages/logo.gif")
canvasimage = Canvas(FrameImage,height=250,width=250,bd=5,relief='sunken')
canvasimage.place(relx=0.5, rely=0.5, anchor=CENTER)
#img2 = music_img.subsample(2,2)
#canvasimage.create_image(20,20,anchor=NW,image=music_img)
image_on_canvas = canvasimage.create_image(20,20,anchor=NW,image=music_img)


scaletime = Scale(Player, orient='horizontal', from_=0, to=360, resolution=0.1, length=350, label='time', variable=currenttime, command=cursortime)
scaletime.grid(row=4, column=1, columnspan=3)

MusicTitle = Label(Player, text="Spotif-Air")
MusicTitle.grid(row=5, column=1, columnspan=3)

MusicTime = Label(Player, textvariable=(currenttime))
MusicTime.grid(row=5, column=3, columnspan=3)

photoprevious= PhotoImage(file="IconsAndImages/buttonprevious50.gif")
PreviousMusic = Button(Player, image=photoprevious,command=previous)
PreviousMusic.grid(row=6, column=1)

photopause= PhotoImage(file="IconsAndImages/pauseplay50.gif")
PausePlay = Button(Player, image=photopause, command=lambda: playmusic())
PausePlay.grid(row=6, column=2)

photonext= PhotoImage(file="IconsAndImages/buttonnext50.gif")
NextMusic = Button(Player, image=photonext,command=next)
NextMusic.grid(row=6, column=3)
FrameIntro.tkraise()
# fenetre.bind('<Configure>', resize)
def on_closing():
    global threadkill
    threadkill = 4

    fenetre.destroy()

fenetre.protocol("WM_DELETE_WINDOW", on_closing)
fenetre.mainloop()

# fermeture connexion
connexion.close()

sys.exit()
