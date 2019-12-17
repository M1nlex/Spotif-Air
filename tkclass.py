from tkinter import *
from tkinter import ttk
import pygame
import threading
import time
import sqlite3
import os
from tkinter import messagebox

sql_music = "SELECT Music_Link FROM Musique WHERE Music_Name = ?"
sql_image = "SELECT Image.Image_Link FROM Image,Musique WHERE ( Image.Image_Id = Musique.Image_Id AND Musique.Music_Name = ? )"
sql_list_music = "SELECT Music_Name FROM Musique"
sql_playlists = "SELECT Playlists.PL_Name, Playlists.PL_Nb, Playlists.PL_List, Genre.Genre_Name FROM Playlists, Genre WHERE Playlists.PL_genre = Genre.Genre_Id"
sql_playlists_music_part1 = "SELECT Musique.Music_Name, Compositeur.Compo_Name FROM Musique,Compositeur WHERE Music_Id IN "
sql_playlists_music_part2=" AND Musique.Compo_Id = Compositeur.Compo_Id"
sql_add_listen = "UPDATE Musique SET Nb_Listen = Nb_Listen + 1 WHERE Music_Name = ?"
sql_search_music = "SELECT Musique.Music_Name, Compositeur.Compo_Name FROM Musique,Compositeur WHERE (Musique.Music_Name like ? OR Compositeur.Compo_Name like ? ) AND Musique.Music_Id=Compositeur.Compo_Id"


connexion = sqlite3.connect("basededonnees.db", check_same_thread=False)
curseur = connexion.cursor()

def on_closing():
    pygame.mixer_music.stop()
    os._exit(0)

def show_playlist(self, Programme, Name, Number, List, Genre, fenetre_de_retour, fenetre_playlist):
    if (Name == "Erreur" and Number == 0):
        return
    Playlist_Content(Programme=fenetre_playlist, Name=Name, Number=Number, List=List, Genre=Genre, fenetre_de_retour=fenetre_de_retour)
    fenetre_playlist.tkraise()

def return_to_playlist(self, fenetre_de_retour):
    fenetre_de_retour.tkraise()
    self.destroy()

def add_music(Nom, Lien, Compositeur, Album, Image, Genre):
    if Nom=="" or Lien=="" or Compositeur=="" or Genre=="" or not(".ogg" in Lien):
        messagebox.showerror("Erreur","Information(s) manquante(s)")
        return
    


class Playlist(Frame):

    def __init__(self, Programme=None, Name="Erreur", Number=0, List=[], Genre="None", fenetre_de_retour="Recherche.Playlist_list", fenetre_playlist="Recherche.Playlist_Content"):
        self.Programme = Programme
        self.Name = StringVar()
        self.Number = IntVar()
        self.List = List
        self.Genre = StringVar()
        self.fenetre_de_retour = fenetre_de_retour
        self.fenetre_playlist = fenetre_playlist

        self.Name.set(Name)
        self.Number.set(Number)
        self.Genre.set(Genre)

        Frame.__init__(self, Programme, relief = SUNKEN, bd = 5)
        self.pack(fill = BOTH)

        self.LabelName = Label(self, textvariable = self.Name)
        self.LabelName.pack(side=LEFT, fill=BOTH, expand=1)

        self.Confirm_PL = Button(self, text = "Voir la Playlist", command=lambda:show_playlist(self, self.Programme, self.Name.get(), self.Number.get(), self.List, self.Genre.get(), self.fenetre_de_retour, self.fenetre_playlist))
        self.Confirm_PL.pack(side=RIGHT, fill=BOTH)

        self.LabelGenre = Label(self, textvariable = self.Genre)
        self.LabelGenre.pack(side=RIGHT, fill=BOTH, expand=1)

        self.LabelNumber = Label(self, textvariable = self.Number)
        self.LabelNumber.pack(side=RIGHT, fill=BOTH, expand=1)

class MusicInfo(Frame):

    def __init__(self, Programme=None, Name="", Artist="", Nb_in_Playlist=0, List_for_playlist=[[]]):

        self.Name=Name
        self.Artist=Artist
        self.Nb_in_Playlist = Nb_in_Playlist
        self.List_for_playlist = List_for_playlist

        Frame.__init__(self, Programme, bd=2, relief="groove")
        self.pack(side=TOP, fill=X, expand=1, anchor=NE)

        self.labelname = Label(self, text=self.Name)
        self.labelname.pack(side=LEFT, fill=BOTH, expand=1)

        self.Playbutton = Button(self, text="Jouer", command=lambda:f.player.Launch_music(self.List_for_playlist, self.Nb_in_Playlist))
        self.Playbutton.pack(side=RIGHT, fill=BOTH)

        self.labelartist = Label(self, text=self.Artist)
        self.labelartist.pack(side=RIGHT, fill=BOTH, expand=1)

class Playlist_Content(Frame):

    def __init__(self, Programme=None, Name="", Number=0, List=[], Genre="Rien", fenetre_de_retour="Recherche.Playlist_Content"):
        self.Programme = Programme
        self.Name = StringVar()
        self.Number = IntVar()
        self.List = List
        self.Genre = StringVar()
        self.fenetre_de_retour = fenetre_de_retour

        self.Name.set(Name)
        self.Number.set(Number)
        self.Genre.set(Genre)

        Frame.__init__(self, Programme, bd = 5)
        self.pack(fill = BOTH)

        self.leavebutton = Button(self, text="Retour aux\nPlaylists", command=lambda:return_to_playlist(self, self.fenetre_de_retour), font=('Helvetica', '10'))
        self.leavebutton.grid(row=0, column=0, rowspan=2, sticky="ns")

        self.labelname = Label(self, textvariable=self.Name, font=('Helvetica', '15'), width=10)
        self.labelname.grid(row=0, column=1, rowspan=2, sticky="nsew")

        self.Labelfornumber = Label(self, text="Nombre de musiques :", font=('Helvetica', '8'))
        self.Labelfornumber.grid(row=0, column=3)

        self.LabelNumber = Label(self, textvariable=self.Number, font=('Helvetica', '8'))
        self.LabelNumber.grid(row=0, column=4)

        self.Labelforgenre = Label(self, text="Genre :", font=('Helvetica', '8'))
        self.Labelforgenre.grid(row=1, column=3)

        self.LabelGenre = Label(self, textvariable=self.Genre, font=('Helvetica', '8'))
        self.LabelGenre.grid(row=1, column=4)

        self.Musiclist = Frame(self)
        self.Musiclist.grid(row=2, column=0, columnspan=5, sticky = "nsew")

        self.FrameMusic = Frame(self.Musiclist)

        self.CanvasMusic = Canvas(self.FrameMusic, height=100, width=400)
        self.viewport = Frame(self.CanvasMusic, width=300)
        self.music_scrollbar = Scrollbar(self.FrameMusic, orient='vertical', command=self.CanvasMusic.yview)
        self.CanvasMusic.configure(yscrollcommand=self.music_scrollbar.set)

        self.music_scrollbar.pack(side=RIGHT, fill=Y)
        self.CanvasMusic.pack(side=LEFT, fill=BOTH, expand=1)
        self.music_window = self.CanvasMusic.create_window((100,0), window=self.viewport, anchor=NW, tags="self.viewport")

        self.viewport.bind("<Configure>", self.OnFrameConfigure)

        l=0
        for i in self.List:
            MusicInfo(self.viewport, Name=i[0], Artist=i[1], Nb_in_Playlist=l, List_for_playlist=self.List)
            l += 1

        self.FrameMusic.pack()

    def OnFrameConfigure(self, event):
        self.CanvasMusic.configure(scrollregion=self.CanvasMusic.bbox("all"))

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
        self.count = 0
        self.thread_kill = False

    def play(self, i=0):
        #print(self.playlist, pygame.mixer_music.get_busy() == 1, self.pause == True)
        if pygame.mixer_music.get_busy() == 1 or self.pause == True:
            Musique.pause(self)
        else:
            if not(self.a):
                self.a = True
                self.t1 = threading.Thread(target=lambda: self.musique_time())
                self.t1.start()
            self.i = i
            self.count = 0
            self.donnee = (self.playlist[self.i])
            f.player.MusicTitle.config(text=self.donnee)
            curseur.execute(sql_music, [self.donnee])
            file = curseur.fetchone()[0]
            #print(file)
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

            #print(f.player.currenttime.get())
            f.player.currenttime.set(format(float(pygame.mixer.music.get_pos() / 1000) + self.start_time, '.0f'))
            time.sleep(0.1)
            if int(self.length) == float(f.player.currenttime.get()):
                self.next_musique()
            if float(f.player.currenttime.get()) == 10 and self.count == 0:
                #print('add 1')
                curseur.execute(sql_add_listen, [self.donnee])
                connexion.commit()
                self.count = 1
            #print(self.thread_kill)


    def next_musique(self):
        pygame.mixer_music.stop()
        self.start_time = 0
        f.player.currenttime.set(0)
        self.play((self.i+1) % (len(self.playlist)))

    def previous(self):
        pygame.mixer_music.stop()
        self.start_time = 0
        self.play((self.i-1) % (len(self.playlist)))

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

        self.recherche = Recherche(self.FrameContent, self)
        self.frames[Recherche] = self.recherche
        self.recherche.grid(row=0, column=0, sticky="nsew")

        self.ajout = Ajout(self.FrameContent, self)
        self.frames[Ajout] = self.ajout
        self.ajout.grid(row=0, column=0, sticky='nsew')

        self.show_frame(Player)

        self.ButtonafficherFrameIntro = Button(self.FrameButton, text="Recherche", command=lambda: self.show_frame(StartPage))
        self.ButtonafficherFrameIntro.pack(side="left", expand="True", fill="x")
        self.ButtonafficherPlayer = Button(self.FrameButton, text="Player", command=lambda: self.show_frame(Player))
        self.ButtonafficherPlayer.pack(side="left", expand="True", fill="x")
        self.ButtonafficherRecherche = Button(self.FrameButton, text="Playlists", command=lambda: self.show_frame(Recherche))
        self.ButtonafficherRecherche.pack(side="left", expand="True", fill="x")
        self.Buttonafficherajout = Button(self.FrameButton, text="Ajout musiques/playlists", command=lambda:self.show_frame(Ajout))
        self.Buttonafficherajout.pack(side="left", expand="True", fill="x")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="blue")

        Label(self, text="Recherche", anchor='center', font=("TkDefaultFont", 30, "bold")).pack(side=TOP, fill=X, anchor=N)
        self.searchvar = StringVar()

        self.framesearch_entry_button = Frame(self)
        self.framesearch_entry_button.pack(side=TOP, fill=X, expand=1, anchor=N)

        self.Entrysearch = Entry(self.framesearch_entry_button, textvariable=self.searchvar)
        self.Entrysearch.pack(side=LEFT, fill=X, expand=1)

        self.buttonsearch = Button(self.framesearch_entry_button, text="Recherche")
        self.buttonsearch.pack(side=RIGHT, fill=X)

        self.FrameSearch = Frame(self, bd=5, relief="raise")

        self.CanvasSearch = Canvas(self.FrameSearch)
        self.viewport = Frame(self.CanvasSearch, width=300)
        self.Search_scrollbar = Scrollbar(self.FrameSearch, orient='vertical', command=self.CanvasSearch.yview)
        self.CanvasSearch.configure(yscrollcommand=self.Search_scrollbar.set)
        self.Search_scrollbar.pack(side=RIGHT, fill=Y)
        self.CanvasSearch.pack(side=LEFT, fill=BOTH, expand=1)
        self.Search_window = self.CanvasSearch.create_window((100,0), window=self.viewport, anchor=NW, tags="self.viewport")
        self.viewport.bind("<Configure>", self.OnFrameConfigure)

        self.FrameSearch.pack(side=TOP, fill=BOTH, expand=1, anchor=N)

        self.buttonsearch.configure(command=lambda:self.Search_musics_artists())

    def OnFrameConfigure(self, event):
        self.CanvasSearch.configure(scrollregion=self.CanvasSearch.bbox("all"))

    def Search_musics_artists(self):
        for widget in self.viewport.winfo_children():
            widget.destroy()
        curseur.execute(sql_search_music, ('%'+self.searchvar.get()+'%', '%'+self.searchvar.get()+'%'))
        search_result = curseur.fetchall()
        for i in search_result:
            MusicInfo(self.viewport, Name=i[0], Artist=i[1], Nb_in_Playlist=0, List_for_playlist=[i])

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

        self.MusicTitle = Label(self, text="Spotif-Air")
        self.MusicTitle.grid(row=5, column=1, columnspan=3)

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

    def Launch_music(self, List_for_playlist, Nb_in_Playlist=0):
        p = []
        for i in List_for_playlist:
            p.append(i[0])
        #abc = Musique(p)
        pygame.mixer_music.stop()
        #f.player.currenttime.set(0)
        f.player.start_time = 0
        f.player.playlist = p
        f.player.play(i=Nb_in_Playlist)

class Recherche(Frame):

    def __init__(self, parent, controller):

        curseur.execute(sql_playlists)
        result_d = curseur.fetchall()
        self.result_f = []
        for i in result_d:
            self.result_f.append( [ i[0], i[1], i[2].split(";"), i[3] ] )
        for i in self.result_f:
            curseur.execute(sql_playlists_music_part1 + "(" + ",".join(i[2]) + ")" + sql_playlists_music_part2 )
            res2 = curseur.fetchall()
            i[2]=res2


        Frame.__init__(self, parent)

        self.Playlist_Content = Frame(self)
        self.Playlist_Content.grid(row=0, column=0, sticky = "nsew")

        self.Playlist_list = Frame(self)
        self.Playlist_list.grid(row=0, column=0, sticky = "nsew")


        self.Labeltitle = Label(self.Playlist_list, text="Playlists", font=('Helvetica', '20'))
        self.Labeltitle.pack(fill=X)

        self.FramePlaylist = Frame(self.Playlist_list)

        self.CanvasPlaylist = Canvas(self.FramePlaylist, height=100, width=400)
        #self.CanvasPlaylist.pack_propagate(0)
        self.viewport = Frame(self.CanvasPlaylist, width=300)
        self.playlist_scrollbar = Scrollbar(self.FramePlaylist, orient='vertical', command=self.CanvasPlaylist.yview)
        self.CanvasPlaylist.configure(yscrollcommand=self.playlist_scrollbar.set)

        self.playlist_scrollbar.pack(side=RIGHT, fill=Y)
        self.CanvasPlaylist.pack(side=LEFT, fill=BOTH, expand=1)
        self.playlist_window = self.CanvasPlaylist.create_window((100,0), window=self.viewport, anchor=NW, tags="self.viewport")

        self.viewport.bind("<Configure>", self.OnFrameConfigure)

        for i in self.result_f:
            Playlist(Programme=self.viewport, Name=i[0], Number=i[1], List=i[2], Genre=i[3], fenetre_de_retour=self.Playlist_list, fenetre_playlist=self.Playlist_Content)

        self.FramePlaylist.pack()


    def OnFrameConfigure(self, event):
        self.CanvasPlaylist.configure(scrollregion=self.CanvasPlaylist.bbox("all"))

class Ajout(Frame):

    def __init__(self, parent, controller):

        Frame.__init__(self,parent)

        self.Button_add_music = Button(self, text="Ajouter une musique", command=self.ajout_add_music)
        self.Button_add_music.pack(side=TOP, fill=BOTH, expand=1)

        self.Button_add_playlist = Button(self, text="Ajouter une playlist")
        self.Button_add_playlist.pack(side=TOP, fill=BOTH, expand=1)

        self.Button_edit_musics = Button(self, text="Modifier les musiques")
        self.Button_edit_musics.pack(side=TOP, fill=BOTH, expand=1)

        self.Button_edit_playlists = Button(self, text="Modifier les playlists")
        self.Button_edit_playlists.pack(side=TOP, fill=BOTH, expand=1)


    def ajout_add_music(self):

        fen_add_music = Toplevel()

        fen_add_music.Name = StringVar()
        fen_add_music.Lien = StringVar()
        fen_add_music.Compositeur = StringVar()
        fen_add_music.Album = StringVar()
        fen_add_music.Image = StringVar()
        fen_add_music.Genre = StringVar()



        Label(fen_add_music, text="Ajouter une musique", font=('Helvetica', '20')).grid(row=0, column=0, columnspan=2)

        Label(fen_add_music, text="Nom :").grid(row=1,column=0)
        fen_add_music.EntryName = Entry(fen_add_music, textvariable=fen_add_music.Name)
        fen_add_music.EntryName.grid(row=1,column=1)

        Label(fen_add_music, text="Lien (fichier .ogg) :").grid(row=2,column=0)
        fen_add_music.EntryLien = Entry(fen_add_music, textvariable=fen_add_music.Lien)
        fen_add_music.EntryLien.grid(row=2,column=1)

        Label(fen_add_music, text="Compositeur :").grid(row=3,column=0)
        fen_add_music.EntryCompositeur = Entry(fen_add_music, textvariable=fen_add_music.Compositeur)
        fen_add_music.EntryCompositeur.grid(row=3,column=1)

        Label(fen_add_music, text="Album :").grid(row=4,column=0)
        fen_add_music.EntryAlbum = Entry(fen_add_music, textvariable=fen_add_music.Album)
        fen_add_music.EntryAlbum.grid(row=4,column=1)

        Label(fen_add_music, text="Image :").grid(row=5,column=0)
        fen_add_music.EntryImage = Entry(fen_add_music, textvariable=fen_add_music.Image)
        fen_add_music.EntryImage.grid(row=5,column=1)

        Label(fen_add_music, text="Genre :").grid(row=6,column=0)
        fen_add_music.EntryGenre = Entry(fen_add_music, textvariable=fen_add_music.Genre)
        fen_add_music.EntryGenre.grid(row=6,column=1)

        fen_add_music.buttonleave = Button(fen_add_music, text="Fermer", command=fen_add_music.destroy)
        fen_add_music.buttonleave.grid(row=7,column=0)

        fen_add_music.buttonadd = Button(fen_add_music, text="Ajouter")
        fen_add_music.buttonadd.grid(row=7,column=1)




#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    f = Mainwindow()
    f.title("Spotif'Air")
    f.mainloop()
    on_closing()
    connexion.close()
