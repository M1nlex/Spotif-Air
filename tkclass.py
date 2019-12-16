from tkinter import *
from tkinter import ttk
import pygame
import threading
import time
import sqlite3

sql_music = "SELECT Music_Link FROM Musique WHERE Music_Name = ?"
sql_image = "SELECT Image.Image_Link FROM Image,Musique WHERE ( Image.Image_Id = Musique.Image_Id AND Musique.Music_Name = ? )"
sql_list_music = "SELECT Music_Name FROM Musique"
connexion = sqlite3.connect("basededonnees.db", check_same_thread=False)
curseur = connexion.cursor()


class Musique():
    def __init__(self, playlist=['Etude Op. 25 No. 11 (Winter Wind)', 'Mii Channel Theme']):
        self.donnee = ''
        self.busy = False
        self.playlist = playlist
        self.pause = False
        self.length = 0
        self.start_time = 0
        self.t1 = 0
        self.stop_thread = False
        pygame.mixer.init()
        self.a = False

    def play(self, i=0):

        if pygame.mixer_music.get_busy() == 1 or self.pause == True:
            Musique.pause(self)
        else:
            if not(self.a):
                self.a = True
                self.t1 = threading.Thread(target=lambda: self.musique_time())
                self.t1.start()
            self.i = i

            self.donnee = (self.playlist[self.i])
            curseur.execute(sql_music, [self.donnee])
            file = curseur.fetchone()[0]
            print(file)
            pygame.mixer.music.load(file)

            curseur.execute(sql_image, [self.donnee])
            Lien_img = curseur.fetchone()[0]
            music_img = PhotoImage(file=Lien_img)
            f.player.canvasimage.delete(f.player.image_on_canvas)
            f.player.canvasimage.create_image(20, 20, anchor=NW, image=music_img)
            f.player.canvasimage.image = music_img

            self.length = pygame.mixer.Sound(file).get_length()
            f.player.scaletime.config(to=self.length)
            pygame.mixer.music.play(start=0)
            self.busy = True
            self.pause = False

    def pause(self):
        if not self.pause:
            pygame.mixer_music.pause()
            self.pause = True
        else:
            pygame.mixer_music.unpause()
            self.pause = False

    def stop(self):
        pygame.mixer_music.stop()
        self.busy = False
        self.pause = False

    def add(self, musique):
        self.playlist.append(musique)

    def set_time(self):
        a = float(f.player.currenttime.get())
        f.player.start_time = a
        pygame.mixer.music.play(start=float(f.player.currenttime.get()))

    def musique_time(self):
        while True:

            print(f.player.currenttime.get())
            f.player.currenttime.set(format(float(pygame.mixer.music.get_pos() / 1000) + self.start_time, '.0f'))
            time.sleep(0.1)
            if int(self.length) == float(f.player.currenttime.get()):
                self.next_musique()

    def next_musique(self):
        pygame.mixer_music.stop()
        self.start_time = 0
        f.player.currenttime.set(0)
        self.play(self.i+1)

    def previous(self):
        pygame.mixer_music.stop()
        self.start_time = 0
        self.play(self.i-1)

    def set_vol(self, val):
        volume = int(val) / 100
        pygame.mixer.music.set_volume(volume)


class Mainwindow(Tk):
    def __init__(self):
        super().__init__()

        mainframe = Frame()
        mainframe.pack(side="top", fill="both", expand=True)

        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_columnconfigure(0, weight=1)
        self.frames = {}

        self.FrameButton = Frame(mainframe, relief='raise', bg='blue', bd=5)
        self.FrameButton.grid(row=0, column=0, columnspan=5, sticky='ew')
        self.FrameContent = Frame(mainframe, relief='raise', bg='blue', bd=5)
        self.FrameContent.grid(row=1, column=0, columnspan=5, sticky='ew')

        start = StartPage(self.FrameContent, self)
        self.frames[StartPage] = start
        start.grid(row=0, column=0, sticky="nsew")

        start = StartPage(self.FrameContent, self)
        self.frames[StartPage] = start
        start.grid(row=0, column=0, sticky="nsew")

        self.player = Player(self.FrameContent, self)
        self.frames[Player] = self.player
        self.player.grid(row=0, column=0, sticky="nsew")

        pagetwo = PageTwo(self.FrameContent, self)
        self.frames[PageTwo] = pagetwo
        pagetwo.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        self.ButtonafficherFrameIntro = Button(self.FrameButton, text="Intro", command=lambda: self.show_frame(StartPage))
        self.ButtonafficherFrameIntro.pack(side="left", expand="True", fill="x")
        self.ButtonafficherPlayer = Button(self.FrameButton, text="Player", command=lambda: self.show_frame(Player))
        self.ButtonafficherPlayer.pack(side="left", expand="True", fill="x")
        self.ButtonafficherRecherche = Button(self.FrameButton, text="Recherche", command=lambda: self.show_frame(PageTwo))
        self.ButtonafficherRecherche.pack(side="left", expand="True", fill="x")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        Label(self, text="Welcome on Spotif'air", anchor='center').grid(row=0, column=0, sticky='nsew')


class Player(Musique, Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Musique.__init__(self)

        volumecontrol = Scale(self, from_=100, to=0, orient=VERTICAL, command=self.set_vol)
        volumecontrol.set(100)
        volumecontrol.grid(row=1, column=4, columnspan=5)

        FrameImage = Frame(self, height=300, width=250)
        FrameImage.grid(row=1, rowspan=3, column=1, columnspan=3, sticky='nsew')
        FrameImage.grid_propagate(0)
        music_img = PhotoImage(file="IconsAndImages/logo.gif")
        self.canvasimage = Canvas(self, height=250, width=250, bd=5, relief='sunken')
        self.canvasimage.place(relx=0.45, rely=0.35, anchor=CENTER)

        self.image_on_canvas = self.canvasimage.create_image(20, 20, anchor=NW, image=music_img)
        self.canvasimage.image = music_img
        self.currenttime = StringVar()
        self.scaletime = Scale(self, orient='horizontal', from_=0, to=360, resolution=0.1, length=350, label='time', variable=self.currenttime, command=lambda x: self.set_time())
        self.scaletime.grid(row=4, column=1, columnspan=3)

        MusicTitle = Label(self, text="Spotif-Air")
        MusicTitle.grid(row=5, column=1, columnspan=3)

        MusicTime = Label(self)
        MusicTime.grid(row=5, column=3, columnspan=3)

        photoprevious = PhotoImage(file="IconsAndImages/buttonprevious50.gif")
        PreviousMusic = Button(self, image=photoprevious, command = lambda: self.previous())
        PreviousMusic.image = photoprevious
        PreviousMusic.grid(row=6, column=1)

        photopause = PhotoImage(file="IconsAndImages/pauseplay50.gif")
        PausePlay = Button(self, image=photopause, command = lambda: self.play())
        PausePlay.image = photopause
        PausePlay.grid(row=6, column=2)

        photonext = PhotoImage(file="IconsAndImages/buttonnext50.gif")
        NextMusic = Button(self, image=photonext, command=lambda: self.next_musique())
        NextMusic.image = photonext
        NextMusic.grid(row=6, column=3)


class PageTwo(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Label223 = Label(self, text="Recherche", anchor='center')
        Label223.grid(row=0, column=0, sticky='nsew')
        entry1 = ttk.Combobox(self)
        entry1.grid(row=1, column=0)


def on_closing():
    pygame.mixer_music.stop()
    sys.exit()


f = Mainwindow()
f.mainloop()