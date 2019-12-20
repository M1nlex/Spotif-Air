from pip._internal import main as pipmain
from tkinter import *
from tkinter import ttk

import threading
import time
import sqlite3
import os
from tkinter import messagebox
import cloudstorage

try:
    import pygame
except ModuleNotFoundError:
    pipmain(['install', 'pygame'])
    import pygame

sql_music = "SELECT Music_Link FROM Musique WHERE Music_Name = ?"
sql_image = "SELECT Image.Image_Link FROM Image,Musique WHERE ( Image.Image_Id = Musique.Image_Id AND Musique.Music_Name = ? )"
sql_list_music = "SELECT Music_Name FROM Musique"
sql_playlists = "SELECT Playlists.PL_Name, Playlists.PL_Nb, Playlists.PL_List, Genre.Genre_Name FROM Playlists, Genre WHERE Playlists.PL_genre = Genre.Genre_Id"
sql_playlists_music_part1 = "SELECT Musique.Music_Name, Compositeur.Compo_Name FROM Musique,Compositeur WHERE Music_Id IN "
sql_playlists_music_part2 = " AND Musique.Compo_Id = Compositeur.Compo_Id"
sql_add_listen = "UPDATE Musique SET Nb_Listen = Nb_Listen + 1 WHERE Music_Name = ?"
sql_search_music = "SELECT Musique.Music_Name, Compositeur.Compo_Name FROM Musique,Compositeur WHERE (Musique.Music_Name like ? OR Compositeur.Compo_Name like ? ) AND Musique.Music_Id=Compositeur.Compo_Id"
sql_test_music_exist = "SELECT COUNT(1) FROM Musique WHERE Music_Name = ? AND Compo_Id= ( SELECT Compo_Id FROM Compositeur WHERE Compo_Name= ? ) AND Album_Id= ( SELECT Album_Id FROM Album WHERE Album_Name= ? ) AND Genre_Id= ( SELECT Genre_Id FROM Genre WHERE Genre_Name= ? )"
sql_add_music = "INSERT INTO Musique( Music_Name, Music_Link, Nb_Listen, Compo_Id, Album_Id, Image_Id, Genre_Id ) VALUES (?, ?, 0, ( SELECT Compo_Id FROM Compositeur WHERE Compo_Name= ? ), ( SELECT Album_Id FROM Album WHERE Album_Name= ? ), ( SELECT Image_Id FROM Image WHERE Image_Name= ? ),( SELECT Genre_Id FROM Genre WHERE Genre_Name= ? ) )"
sql_classement_music = "SELECT Musique.Music_Name, Compositeur.Compo_Name From Musique, Compositeur WHERE Musique.Compo_Id = Compositeur.Compo_Id ORDER BY Nb_Listen DESC"
sql_get_sum_listen_compo = "SELECT SUM(Nb_Listen) FROM Musique WHERE Compo_Id = ?"
sql_get_nb_compo = "SELECT MAX(Compo_Id) FROM Compositeur"
sql_get_comp = "SELECT Compo_Name from Compositeur WHERE Compo_Id = ?"
sql_get_sum_listen_genre = "SELECT SUM(Nb_Listen) FROM Musique WHERE Genre_Id = ?"
sql_get_nb_genre = "SELECT MAX(Genre_Id) FROM Genre"
sql_get_genre = "SELECT Genre_Name from Genre WHERE Genre_Id = ?"
sql_add_music = "INSERT INTO Musique( Music_Name, Music_Link, Nb_Listen, Compo_Id, Album_Id, Image_Id, Genre_Id ) VALUES (?, ?, 0, ?, ( SELECT Album_Id FROM Album WHERE Album_Name= ? ), ( SELECT Image_Id FROM Image WHERE Image_Name= ? ),( SELECT Genre_Id FROM Genre WHERE Genre_Name= ? ) )"
sql_test_playlist_exist = "SELECT COUNT(1) FROM Playlists WHERE PL_Name = ?"
sql_test_playlist_exist_2 = "SELECT COUNT(1) FROM Playlists WHERE PL_Name = ? AND PL_List = ? AND PL_genre = (SELECT Genre_Id FROM Genre WHERE Genre_Name = ?) AND PL_Nb = ?"
sql_add_playlist = "INSERT INTO Playlists (PL_Name, PL_List, PL_genre, PL_Nb) VALUES (?, ?, (SELECT Genre_Id FROM Genre WHERE Genre_Name= ?), ?)"
sql_get_compo_id = "SELECT Genre_Id FROM Genre WHERE Genre_Name= ?"
sql_edit_playlsit = "UPDATE Playlists SET PL_Name = ?, PL_List = ?, PL_genre = (SELECT Genre_Id FROM Genre WHERE Genre_Name=?), PL_Nb = ? WHERE PL_Name = ?"

def on_closing():
    pygame.mixer_music.stop()
    connexion.close()
    print('end')
    os._exit(0)

def show_playlist(self, Programme, Name, Number, List, Genre, fenetre_de_retour, fenetre_playlist):
    if (Name == "Erreur" and Number == 0):
        return
    Playlist_Content(Programme=fenetre_playlist, Name=Name, Number=Number, List=List, Genre=Genre,
                     fenetre_de_retour=fenetre_de_retour)
    fenetre_playlist.tkraise()

def return_to_playlist(self, fenetre_de_retour):
    fenetre_de_retour.tkraise()
    self.destroy()

def add_music(Nom, Lien, Compositeur, Album, Image, Genre):
    if Nom == "" or Lien == "" or Compositeur == "" or Genre == "" or not (".ogg" in Lien):
        messagebox.showerror("Erreur", "Information(s) manquante(s)")
    elif curseur.execute(sql_test_music_exist, (Nom, Compositeur, Album, Genre)).fetchone()[0] == 1:
        messagebox.showwarning("Erreur", "Ce morceau existe déjà dans la base de donnée")
    else:
        if curseur.execute("SELECT COUNT(1) FROM Compositeur WHERE Compo_Name= ?", (Compositeur,)).fetchone()[0] == 0:
            curseur.execute("INSERT INTO Compositeur(Compo_Name) VALUES (?)", (Compositeur,))
        if curseur.execute("SELECT COUNT(1) FROM Album WHERE Album_Name=?", (Album,)).fetchone()[0] == 0:
            curseur.execute("INSERT INTO Album(Album_Name) VALUES (?)", (Album,))
            curseur.execute("INSERT INTO Image(Image_Name, Image_Link) VALUES (?, ?)", (Album, Image))
        if curseur.execute("SELECT COUNT(1) FROM Genre WHERE Genre_Name=?", (Genre,)).fetchone()[0] == 0:
            curseur.execute("INSERT INTO Genre(Genre_Name) VALUES (?)", (Genre,))
        curseur.execute(sql_add_music, (Nom, Lien, Compositeur, Album, Album, Genre))
        connexion.commit()
        messagebox.showinfo("Succès", "la musique a bien été ajoutée à la base de donnée.")

def add_playlist(Nom, List, Genre, Nb):

    if Nom=="" or Genre=="":
        messagebox.showerror("Erreur", "Des informations manquent pour créer la playlist")
    elif curseur.execute(sql_test_playlist_exist, (Nom,)).fetchone()[0] == 1:
        messagebox.showwarning("Erreur", "Une playlist du même nom existe déjà dans la base de donnée")
    elif curseur.execute("SELECT COUNT(1) FROM Genre WHERE Genre_Name=?", (Genre,)).fetchone()[0] == 0:
        curseur.execute("INSERT INTO Genre(Genre_Name) VALUES (?)", (Genre,))
    else:
        String_to_send = ""
        for i in List:
            String_to_send = String_to_send + ";" + str(curseur.execute( "SELECT Music_Id FROM Musique WHERE Music_Name= ? AND Compo_Id = (SELECT Compo_Id FROM Compositeur WHERE Compo_Name= ?)", (i[0],i[1]) ).fetchone()[0])
        if String_to_send[0]==";":
            String_to_send = String_to_send[1:]
        curseur.execute(sql_add_playlist, (Nom, String_to_send, Genre, Nb))
        connexion.commit()
        f.frames[Ajout].List_playlist_creation = []
        f.frames[Ajout].List_playlist_creation_number.set(0)
        messagebox.showinfo("Succès","La playlist a été créée")
        maj_playlist()

def maj_playlist():
    curseur.execute(sql_playlists)
    result_d = curseur.fetchall()
    result_f = []
    for i in result_d:
        result_f.append([i[0], i[1], i[2].split(";"), i[3]])
    for i in result_f:
        curseur.execute(sql_playlists_music_part1 + "(" + ",".join(i[2]) + ")" + sql_playlists_music_part2)
        res2 = curseur.fetchall()
        i[2] = res2
    for widget in f.frames[Recherche_Playlist].viewport.winfo_children():
        widget.destroy()
    for i in result_f:
        Playlist(Programme=f.frames[Recherche_Playlist].viewport, Name=i[0], Number=i[1], List=i[2], Genre=i[3], fenetre_de_retour=f.frames[Recherche_Playlist].Playlist_list, fenetre_playlist=f.frames[Recherche_Playlist].Playlist_Content)

def maj_music():
    pass

def playlist_add_music(name, artist):
    if [name, artist] not in f.frames[Ajout].List_playlist_creation:
        f.frames[Ajout].List_playlist_creation.append([name, artist])
        f.frames[Ajout].List_playlist_creation_number.set(f.frames[Ajout].List_playlist_creation_number.get()+1)
    else:
        f.frames[Ajout].List_playlist_creation.remove([name, artist])
        f.frames[Ajout].List_playlist_creation_number.set(f.frames[Ajout].List_playlist_creation_number.get()-1)

def confirm_edit(Name, List, Genre, Nb, oldName):
    String_to_send = ""
    for i in List:
        String_to_send = String_to_send + ";" + str(curseur.execute( "SELECT Music_Id FROM Musique WHERE Music_Name= ? AND Compo_Id = (SELECT Compo_Id FROM Compositeur WHERE Compo_Name= ?)", (i[0],i[1]) ).fetchone()[0])
    if String_to_send[0]==";":
        String_to_send = String_to_send[1:]
    if Name=="" or Genre == "":
        messagebox.showerror("Erreur", "Il manque des informations pour changer la playlist")
    elif curseur.execute(sql_test_playlist_exist_2, (Name, String_to_send, Genre, Nb) ).fetchone()[0] == 1:
        messagebox.showwarning("Erreur", "Une playlist du même nom existe déjà dans la base de donnée")
    else:
        curseur.execute(sql_edit_playlsit,(Name, String_to_send, Genre, Nb, oldName))
        messagebox.showinfo("Succès", "La playlist a été modifiée, veuillez\nretourner aux playlists")
        maj_playlist()

def edit_playlist(Name, List, Genre, Nb):

    def OnFrameConfigure(self):
        self.CanvasSearch.configure(scrollregion=self.CanvasSearch.bbox("all"))

    edit_win = Toplevel()

    edit_win.Name = StringVar()
    edit_win.Genre = StringVar()

    edit_win.Name.set(Name)
    edit_win.Genre.set(Genre)
    edit_win.oldName = Name

    List_tempo = []
    for i in List:
        List_tempo.append( [ i[0],i[1] ] )

    f.frames[Ajout].List_playlist_creation=(List_tempo)
    f.frames[Ajout].List_playlist_creation_number.set(Nb)



    Label(edit_win, text="Editer une playlist", font=('Segoe UI Light', '20')).grid(row=0, column=0, columnspan=2)

    Label(edit_win, text="Nom :").grid(row=1,column=0)
    edit_win.EntryName = Entry(edit_win, textvariable=edit_win.Name)
    edit_win.EntryName.grid(row=1,column=1)

    Label(edit_win, text="Genre :").grid(row=2,column=0)
    edit_win.EntryGenre = Entry(edit_win, textvariable=edit_win.Genre)
    edit_win.EntryGenre.grid(row=2,column=1)

    Label(edit_win, text="Nombre de musiques :").grid(row=3,column=0)
    edit_win.Label_Nb = Label(edit_win, textvariable=f.frames[Ajout].List_playlist_creation_number)
    edit_win.Label_Nb.grid(row=3,column=1)

    edit_win.FrameSearch = Frame(edit_win, bd=5, relief="raise")

    edit_win.CanvasSearch = Canvas(edit_win.FrameSearch)
    edit_win.viewport = Frame(edit_win.CanvasSearch, width=300)
    edit_win.Search_scrollbar = Scrollbar(edit_win.FrameSearch, orient='vertical', command=edit_win.CanvasSearch.yview)
    edit_win.CanvasSearch.configure(yscrollcommand=edit_win.Search_scrollbar.set)
    edit_win.Search_scrollbar.pack(side=RIGHT, fill=Y)
    edit_win.CanvasSearch.pack(side=LEFT, fill=BOTH, expand=1)
    edit_win.Search_window = edit_win.CanvasSearch.create_window((100,0), window=edit_win.viewport, anchor=NW, tags="edit_win.viewport")
    edit_win.viewport.bind("<Configure>", OnFrameConfigure(edit_win))

    edit_win.FrameSearch.grid(row=4,column=0,columnspan=2)

    edit_win.buttonleave = Button(edit_win, text="Fermer", command=edit_win.destroy)
    edit_win.buttonleave.grid(row=7,column=0)

    edit_win.buttonadd = Button(edit_win, text="Confirmer", command=lambda:confirm_edit(Name=edit_win.Name.get(), List=f.frames[Ajout].List_playlist_creation, Genre=edit_win.Genre.get(), Nb=f.frames[Ajout].List_playlist_creation_number.get(), oldName=edit_win.oldName))
    edit_win.buttonadd.grid(row=7,column=1)

    for widget in edit_win.viewport.winfo_children():
        widget.destroy()
    curseur.execute(sql_search_music, ('%', '%'))
    search_result = curseur.fetchall()
    for i in search_result:
        MusicInfo(edit_win.viewport, Name=i[0], Artist=i[1], Nb_in_Playlist=0, List_for_playlist=[i], add_option=1)

class Playlist(Frame):

    def __init__(self, Programme=None, Name="Erreur", Number=0, List=[], Genre="None",
                 fenetre_de_retour="Recherche.Playlist_list", fenetre_playlist="Recherche.Playlist_Content"):
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

        Frame.__init__(self, Programme, relief='groove', bd=2, bg='black')
        self.pack(fill=X, side=TOP, expand=1, anchor=NW, pady=10)

        self.LabelName = Label(self, textvariable=self.Name)
        self.LabelName.pack(side=LEFT, fill=BOTH, expand=1)

        self.Confirm_PL = Button(self, text="Voir la Playlist",
                                 command=lambda: show_playlist(self, self.Programme, self.Name.get(), self.Number.get(),
                                                               self.List, self.Genre.get(), self.fenetre_de_retour,
                                                               self.fenetre_playlist))
        self.Confirm_PL.pack(side=RIGHT, fill=BOTH)

        self.LabelGenre = Label(self, textvariable=self.Genre)
        self.LabelGenre.pack(side=RIGHT, fill=BOTH, expand=1)

        self.LabelNumber = Label(self, textvariable=self.Number)
        self.LabelNumber.pack(side=RIGHT, fill=BOTH, expand=1)

class MusicInfo(Frame):

    def __init__(self, Programme=None, Name="", Artist="", Nb_in_Playlist=0, List_for_playlist=[[]], add_option=0):

        self.Name=Name
        self.Artist=Artist
        self.Nb_in_Playlist = Nb_in_Playlist
        self.List_for_playlist = List_for_playlist
        self.add_option = add_option

        Frame.__init__(self, Programme, bd=2, relief="groove", bg="black")
        self.pack(side=TOP, fill=X, expand=1, anchor=NE, pady=10)

        self.labelname = Label(self, text=self.Name)
        self.labelname.pack(side=LEFT, fill=BOTH, expand=1)

        if self.add_option == 0:
            self.Playbutton = Button(self, text="Jouer", command=lambda:f.player.Launch_music(self.List_for_playlist, self.Nb_in_Playlist))
            self.Playbutton.pack(side=RIGHT, fill=BOTH)
        else:
            self.Addbutton = Button(self, text="Ajouter", command=lambda:playlist_add_music(name=self.Name, artist=self.Artist))
            self.Addbutton.pack(side=RIGHT, fill=BOTH)

        self.labelartist = Label(self, text=self.Artist)
        self.labelartist.pack(side=RIGHT, fill=BOTH, expand=1)

class Playlist_Content(Frame):

    def __init__(self, Programme=None, Name="", Number=0, List=[], Genre="Rien",
                 fenetre_de_retour="Recherche.Playlist_Content"):
        self.Programme = Programme
        self.Name = StringVar()
        self.Number = IntVar()
        self.List = List
        self.Genre = StringVar()
        self.fenetre_de_retour = fenetre_de_retour

        self.Name.set(Name)
        self.Number.set(Number)
        self.Genre.set(Genre)

        Frame.__init__(self, Programme, bd=5)
        self.pack(fill=BOTH)

        self.leavebutton = Button(self, text="Retour aux\nPlaylists",
                                  command=lambda: return_to_playlist(self, self.fenetre_de_retour),
                                  font=('TkDefaultFont', '8'))
        self.leavebutton.grid(row=0, column=0, rowspan=2, sticky="ns")

        self.labelname = Label(self, textvariable=self.Name, font=('Segoe UI Light', '18'), width=5)
        self.labelname.grid(row=0, column=1, rowspan=2, sticky="nsew")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)

        self.Labelfornumber = Label(self, text="Nombre de musiques :", font=('TkDefaultFont', '8'))
        self.Labelfornumber.grid(row=0, column=3)

        self.LabelNumber = Label(self, textvariable=self.Number, font=('TkDefaultFont', '8'))
        self.LabelNumber.grid(row=0, column=4)

        self.Labelforgenre = Label(self, text="Genre :", font=('TkDefaultFont', '8'))
        self.Labelforgenre.grid(row=1, column=3)

        self.LabelGenre = Label(self, textvariable=self.Genre, font=('TkDefaultFont', '8'))
        self.LabelGenre.grid(row=1, column=4)

        self.ButtonEdit = Button(self, text="Editer la\nplaylist", font=('TkDefaultFont', '8'), command=lambda:edit_playlist(Name=self.Name.get(), List=self.List, Genre=self.Genre.get(), Nb=self.Number.get()))
        self.ButtonEdit.grid(row=2,column=0,sticky="new")

        self.Musiclist = Frame(self, relief='groove', bd=5)
        self.Musiclist.grid(row=2, column=1, columnspan=4)
        self.rowconfigure(2, minsize=400)


        self.FrameMusic = Frame(self.Musiclist)

        self.CanvasMusic = Canvas(self.FrameMusic, height=350, width=300)
        self.viewport = Frame(self.CanvasMusic, width=300)
        self.music_scrollbar = Scrollbar(self.FrameMusic, orient='vertical', command=self.CanvasMusic.yview)
        self.CanvasMusic.configure(yscrollcommand=self.music_scrollbar.set)

        self.music_scrollbar.pack(side=RIGHT, fill=Y)
        self.CanvasMusic.pack(side=LEFT, fill=BOTH, expand=1)
        self.music_window = self.CanvasMusic.create_window((100, 0), window=self.viewport, anchor=NW,
                                                           tags="self.viewport")

        self.viewport.bind("<Configure>", self.OnFrameConfigure)

        l = 0
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
        # print(self.playlist, pygame.mixer_music.get_busy() == 1, self.pause == True)
        if pygame.mixer_music.get_busy() == 1 or self.pause == True:
            Musique.pause(self)
        else:
            if not (self.a):
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
            try:
                pygame.mixer.music.load(file)
            except:
                cloudstorage.download_random_file('spotif-air', 'Song', './Song/', file)
                pygame.mixer.music.load(file)

            curseur.execute(sql_image, [self.donnee])
            Lien_img = curseur.fetchone()[0]

            try:
                music_img = PhotoImage(file=Lien_img)
            except:
                cloudstorage.download_random_file('spotif-air', 'Music_Img', './Music_Img/', Lien_img)
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

            # print(f.player.currenttime.get())
            f.player.currenttime.set(format(float(pygame.mixer.music.get_pos() / 1000) + self.start_time, '.0f'))
            time.sleep(0.1)
            if int(self.length) == float(f.player.currenttime.get()):
                self.next_musique()
            if float(f.player.currenttime.get()) == 10 and self.count == 0:
                # print('add 1')
                curseur.execute(sql_add_listen, [self.donnee])
                connexion.commit()
                self.count = 1
            # print(self.thread_kill)

    def next_musique(self):
        pygame.mixer_music.stop()
        self.start_time = 0
        f.player.currenttime.set(0)
        self.play((self.i + 1) % (len(self.playlist)))

    def previous(self):
        pygame.mixer_music.stop()
        self.start_time = 0
        self.play((self.i - 1) % (len(self.playlist)))

    def set_vol(self, val):
        volume = int(val) / 100
        pygame.mixer.music.set_volume(volume)

class Mainwindow(Tk):
    def __init__(self):
        super().__init__()

        mainframe = Frame()
        mainframe.pack(side="top", fill="both", expand=True)
        self.resizable(False, False)
        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_columnconfigure(0, weight=1)
        self.frames = {}

        self.FrameButton = Frame(mainframe, relief='raise', bg='blue', bd=5)
        self.FrameButton.grid(row=0, column=0, columnspan=5, sticky='ew')
        self.FrameContent = Frame(mainframe, relief='raise', bg='blue', bd=5)
        self.FrameContent.grid(row=1, column=0, columnspan=5, sticky='ew')

        start = Recherche_Music(self.FrameContent, self)
        self.frames[Recherche_Music] = start
        start.grid(row=0, column=0, sticky="nsew")

        recherche_music = Recherche_Music(self.FrameContent, self)
        self.frames[Recherche_Music] = recherche_music
        recherche_music.grid(row=0, column=0, sticky="nsew")

        self.player = Player(self.FrameContent, self)
        self.frames[Player] = self.player
        self.player.grid(row=0, column=0, sticky="nsew")

        self.recherche = Recherche_Playlist(self.FrameContent, self)
        self.frames[Recherche_Playlist] = self.recherche
        self.recherche.grid(row=0, column=0, sticky="nsew")

        self.ajout = Ajout(self.FrameContent, self)
        self.frames[Ajout] = self.ajout
        self.ajout.grid(row=0, column=0, sticky='nsew')

        self.stat = Stat(self.FrameContent, self)
        self.frames[Stat] = self.stat
        self.stat.grid(row=0, column=0, sticky='nsew')

        self.start = Start(self.FrameContent, self)
        self.frames[Start] = self.start
        self.start.grid(row=0, column=0, sticky='nsew')

        self.show_frame(Start)

        self.ButtonafficherFrameIntro = Button(self.FrameButton, text="Recherche",
                                               command=lambda: self.show_frame(Recherche_Music))
        self.ButtonafficherFrameIntro.pack(side="left", expand="True", fill="x")
        self.ButtonafficherPlayer = Button(self.FrameButton, text="Player", command=lambda: self.show_frame(Player))
        self.ButtonafficherPlayer.pack(side="left", expand="True", fill="x")
        self.ButtonafficherRecherche = Button(self.FrameButton, text="Playlists",
                                              command=lambda: self.show_frame(Recherche_Playlist))
        self.ButtonafficherRecherche.pack(side="left", expand="True", fill="x")
        self.Buttonafficherajout = Button(self.FrameButton, text="Ajout musiques/playlists",
                                          command=lambda: self.show_frame(Ajout))
        self.Buttonafficherajout.pack(side="left", expand="True", fill="x")

        self.Buttonstat = Button(self.FrameButton, text="Stat",
                                          command=lambda: self.show_frame(Stat))
        self.Buttonstat.pack(side="left", expand="True", fill="x")





    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Start(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Label(self, text="Bienvenue sur Spotif'Air", anchor='center', font=('Segoe UI Light', 30, "bold")).place(relx=0.5, rely=0.4, anchor=CENTER)
        Label(self, text="Cliquez sur un onglet pour démarrer", anchor='center', font=('Segoe UI Light', 15)).place(relx=0.5, rely=0.55, anchor=CENTER)

class Recherche_Music(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="blue")

        Label(self, text="Recherche", anchor='center', font=('Segoe UI Light', 30)).pack(side=TOP, fill=X, anchor=N)
        self.searchvar = StringVar()

        self.framesearch_entry_button = Frame(self)
        self.framesearch_entry_button.pack(side=TOP, fill=X, expand=1, anchor=N)

        self.Entrysearch = Entry(self.framesearch_entry_button, textvariable=self.searchvar)
        self.Entrysearch.pack(side=LEFT, fill=X, expand=1)

        self.buttonsearch = Button(self.framesearch_entry_button, text="Recherche")
        self.buttonsearch.pack(side=RIGHT, fill=X)

        self.FrameSearch = Frame(self, bd=5, relief="raise")

        self.CanvasSearch = Canvas(self.FrameSearch)
        self.viewport = Frame(self.CanvasSearch, width=390)
        #self.viewport.pack_propagate(False)
        self.Search_scrollbar = Scrollbar(self.FrameSearch, orient='vertical', command=self.CanvasSearch.yview)
        self.CanvasSearch.configure(yscrollcommand=self.Search_scrollbar.set)
        self.Search_scrollbar.pack(side=RIGHT, fill=Y)
        self.CanvasSearch.pack(side=LEFT, fill=BOTH, expand=1)
        self.Search_window = self.CanvasSearch.create_window((100, 0), window=self.viewport, anchor=NW,
                                                             tags="self.viewport")
        self.viewport.bind("<Configure>", self.OnFrameConfigure)

        self.FrameSearch.pack(side=TOP, fill=BOTH, expand=1, anchor=N)

        self.buttonsearch.configure(command=lambda: self.Search_musics_artists())

    def OnFrameConfigure(self, event):
        self.CanvasSearch.configure(scrollregion=self.CanvasSearch.bbox("all"))

    def Search_musics_artists(self):
        for widget in self.viewport.winfo_children():
            widget.destroy()
        curseur.execute(sql_search_music, ('%' + self.searchvar.get() + '%', '%' + self.searchvar.get() + '%'))
        search_result = curseur.fetchall()
        for i in search_result:
            MusicInfo(self.viewport, Name=i[0], Artist=i[1], Nb_in_Playlist=0, List_for_playlist=[i] )

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
        self.scaletime = Scale(self, orient='horizontal', from_=0, to=360, resolution=0.1, length=350, label='time',
                               variable=self.currenttime, command=lambda x: self.set_time())
        self.scaletime.grid(row=4, column=1, columnspan=3)

        self.MusicTitle = Label(self, text="Spotif-Air")
        self.MusicTitle.grid(row=5, column=1, columnspan=3)

        MusicTime = Label(self)
        MusicTime.grid(row=5, column=3, columnspan=3)

        photoprevious = PhotoImage(file="IconsAndImages/buttonprevious50.gif")
        PreviousMusic = Button(self, image=photoprevious, command=lambda: self.previous())
        PreviousMusic.image = photoprevious
        PreviousMusic.grid(row=6, column=1)

        photopause = PhotoImage(file="IconsAndImages/pauseplay50.gif")
        PausePlay = Button(self, image=photopause, command=lambda: self.play())
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
        # abc = Musique(p)
        pygame.mixer_music.stop()
        # f.player.currenttime.set(0)
        f.player.start_time = 0
        f.player.playlist = p
        f.player.play(i=Nb_in_Playlist)

class Recherche_Playlist(Frame):

    def __init__(self, parent, controller):

        curseur.execute(sql_playlists)
        result_d = curseur.fetchall()
        self.result_f = []
        for i in result_d:
            self.result_f.append([i[0], i[1], i[2].split(";"), i[3]])
        for i in self.result_f:
            curseur.execute(sql_playlists_music_part1 + "(" + ",".join(i[2]) + ")" + sql_playlists_music_part2)
            res2 = curseur.fetchall()
            i[2] = res2

        Frame.__init__(self, parent)


        self.Playlist_Content = Frame(self)
        self.Playlist_Content.grid(row=0, column=0, sticky="nsew")

        self.Playlist_list = Frame(self)
        self.Playlist_list.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, minsize=450)

        self.Labeltitle = Label(self.Playlist_list, text="Playlists", font=('Segoe UI Light', '30'))
        self.Labeltitle.pack(fill=X, side=TOP,anchor=N)

        self.FramePlaylist = Frame(self.Playlist_list, relief='groove', bd=5)

        self.CanvasPlaylist = Canvas(self.FramePlaylist, height=100, width=400)
        # self.CanvasPlaylist.pack_propagate(0)
        self.viewport = Frame(self.CanvasPlaylist, width=300)
        self.playlist_scrollbar = Scrollbar(self.FramePlaylist, orient='vertical', command=self.CanvasPlaylist.yview)
        self.CanvasPlaylist.configure(yscrollcommand=self.playlist_scrollbar.set)

        self.playlist_scrollbar.pack(side=RIGHT, fill=Y)
        self.CanvasPlaylist.pack(side=LEFT, fill=BOTH, expand=1)
        self.playlist_window = self.CanvasPlaylist.create_window((100, 0), window=self.viewport, anchor=NW,
                                                                 tags="self.viewport")

        self.viewport.bind("<Configure>", self.OnFrameConfigure)

        for i in self.result_f:
            Playlist(Programme=self.viewport, Name=i[0], Number=i[1], List=i[2], Genre=i[3],
                     fenetre_de_retour=self.Playlist_list, fenetre_playlist=self.Playlist_Content)

        self.FramePlaylist.pack(side=TOP, fill=BOTH, expand=1, anchor=CENTER)

    def OnFrameConfigure(self, event):
        self.CanvasPlaylist.configure(scrollregion=self.CanvasPlaylist.bbox("all"))

class Ajout(Frame):

    def __init__(self, parent, controller):

        self.List_playlist_creation = []
        self.List_playlist_creation_number = IntVar()

        Frame.__init__(self,parent)

        self.Button_add_music = Button(self, text="Ajouter une musique", font=('Segoe UI Light', 30), bd=10, command=self.ajout_add_music)
        self.Button_add_music.pack(side=TOP, fill=BOTH, expand=1)

        self.Button_add_playlist = Button(self, text="Ajouter une playlist", font=('Segoe UI Light', 30), bd=10, command=self.ajout_add_playlist)
        self.Button_add_playlist.pack(side=TOP, fill=BOTH, expand=1)

    def ajout_add_music(self):
        fen_add_music = Toplevel()

        fen_add_music.Name = StringVar()
        fen_add_music.Lien = StringVar()
        fen_add_music.Compositeur = StringVar()
        fen_add_music.Album = StringVar()
        fen_add_music.Image = StringVar()
        fen_add_music.Genre = StringVar()

        Label(fen_add_music, text="Ajouter une musique", font=('Segoe UI Light', '20')).grid(row=0, column=0, columnspan=2)

        Label(fen_add_music, text="Nom :").grid(row=1, column=0)
        fen_add_music.EntryName = Entry(fen_add_music, textvariable=fen_add_music.Name)
        fen_add_music.EntryName.grid(row=1, column=1)

        Label(fen_add_music, text="Lien (fichier .ogg) :").grid(row=2, column=0)
        fen_add_music.EntryLien = Entry(fen_add_music, textvariable=fen_add_music.Lien)
        fen_add_music.EntryLien.grid(row=2, column=1)

        Label(fen_add_music, text="Compositeur :").grid(row=3, column=0)
        fen_add_music.EntryCompositeur = Entry(fen_add_music, textvariable=fen_add_music.Compositeur)
        fen_add_music.EntryCompositeur.grid(row=3, column=1)

        Label(fen_add_music, text="Album :").grid(row=4, column=0)
        fen_add_music.EntryAlbum = Entry(fen_add_music, textvariable=fen_add_music.Album)
        fen_add_music.EntryAlbum.grid(row=4, column=1)

        Label(fen_add_music, text="Image :").grid(row=5, column=0)
        fen_add_music.EntryImage = Entry(fen_add_music, textvariable=fen_add_music.Image)
        fen_add_music.EntryImage.grid(row=5, column=1)

        Label(fen_add_music, text="Genre :").grid(row=6, column=0)
        fen_add_music.EntryGenre = Entry(fen_add_music, textvariable=fen_add_music.Genre)
        fen_add_music.EntryGenre.grid(row=6, column=1)

        fen_add_music.buttonleave = Button(fen_add_music, text="Fermer", command=fen_add_music.destroy)
        fen_add_music.buttonleave.grid(row=7, column=0)

        fen_add_music.buttonadd = Button(fen_add_music, text="Ajouter",
                                         command=lambda: add_music(fen_add_music.Name.get(), fen_add_music.Lien.get(),
                                                                   fen_add_music.Compositeur.get(),
                                                                   fen_add_music.Album.get(), fen_add_music.Image.get(),
                                                                   fen_add_music.Genre.get()))
        fen_add_music.buttonadd.grid(row=7, column=1)

    def ajout_add_playlist(self):

        self.fen_add_playlist = Toplevel()

        self.fen_add_playlist.Name = StringVar()
        self.fen_add_playlist.List = []
        self.fen_add_playlist.Genre = StringVar()

        Label(self.fen_add_playlist, text="Ajouter une playlist", font=('Segoe UI Light', '20')).grid(row=0, column=0, columnspan=2)

        Label(self.fen_add_playlist, text="Nom :").grid(row=1,column=0)
        self.fen_add_playlist.EntryName = Entry(self.fen_add_playlist, textvariable=self.fen_add_playlist.Name)
        self.fen_add_playlist.EntryName.grid(row=1,column=1)

        Label(self.fen_add_playlist, text="Genre :").grid(row=2,column=0)
        self.fen_add_playlist.EntryGenre = Entry(self.fen_add_playlist, textvariable=self.fen_add_playlist.Genre)
        self.fen_add_playlist.EntryGenre.grid(row=2,column=1)

        Label(self.fen_add_playlist, text="Nombre de musiques :").grid(row=3,column=0)
        self.fen_add_playlist.Label_Nb = Label(self.fen_add_playlist, textvariable=self.List_playlist_creation_number)
        self.fen_add_playlist.Label_Nb.grid(row=3,column=1)

        self.fen_add_playlist.FrameSearch = Frame(self.fen_add_playlist, bd=5, relief="raise")

        self.fen_add_playlist.CanvasSearch = Canvas(self.fen_add_playlist.FrameSearch)
        self.fen_add_playlist.viewport = Frame(self.fen_add_playlist.CanvasSearch, width=300)
        self.fen_add_playlist.Search_scrollbar = Scrollbar(self.fen_add_playlist.FrameSearch, orient='vertical', command=self.fen_add_playlist.CanvasSearch.yview)
        self.fen_add_playlist.CanvasSearch.configure(yscrollcommand=self.fen_add_playlist.Search_scrollbar.set)
        self.fen_add_playlist.Search_scrollbar.pack(side=RIGHT, fill=Y)
        self.fen_add_playlist.CanvasSearch.pack(side=LEFT, fill=BOTH, expand=1)
        self.fen_add_playlist.Search_window = self.fen_add_playlist.CanvasSearch.create_window((100,0), window=self.fen_add_playlist.viewport, anchor=NW, tags="self.fen_add_playlist.viewport")
        self.fen_add_playlist.viewport.bind("<Configure>", self.OnFrameConfigure)

        self.fen_add_playlist.FrameSearch.grid(row=4,column=0,columnspan=2)

        self.fen_add_playlist.buttonleave = Button(self.fen_add_playlist, text="Fermer", command=self.fen_add_playlist.destroy)
        self.fen_add_playlist.buttonleave.grid(row=7,column=0)

        self.fen_add_playlist.buttonadd = Button(self.fen_add_playlist, text="Ajouter", command=lambda:add_playlist(Nom=self.fen_add_playlist.Name.get(), List=self.List_playlist_creation, Genre=self.fen_add_playlist.Genre.get(), Nb=self.List_playlist_creation_number.get() ))
        self.fen_add_playlist.buttonadd.grid(row=7,column=1)

        for widget in self.fen_add_playlist.viewport.winfo_children():
            widget.destroy()
        curseur.execute(sql_search_music, ('%', '%'))
        search_result = curseur.fetchall()
        for i in search_result:
            MusicInfo(self.fen_add_playlist.viewport, Name=i[0], Artist=i[1], Nb_in_Playlist=0, List_for_playlist=[i], add_option=1)

    def OnFrameConfigure(self, event):
        self.fen_add_playlist.CanvasSearch.configure(scrollregion=self.fen_add_playlist.CanvasSearch.bbox("all"))

class Stat(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="blue")

        Label(self, text="Statistique", anchor='center', font=('Segoe UI Light', 30)).pack(side=TOP, fill=X, anchor=N)

        self.framesearch_entry_button = Frame(self)
        self.framesearch_entry_button.pack(side=TOP, fill=X, expand=1, anchor=N)
        Label(self.framesearch_entry_button, text='Top : ').pack(side=LEFT)
        self.Entrysearch = ttk.Combobox(self.framesearch_entry_button, values=["Musique", "Artiste", "Genre"])
        self.Entrysearch.pack(side=LEFT, fill=X, expand=1)

        self.buttonsearch = Button(self.framesearch_entry_button, text="Recherche", command=self.top10)
        self.buttonsearch.pack(side=LEFT, fill=X)
        self.buttonsearch = Button(self.framesearch_entry_button, text="Diagramme", command=self.diagramme)
        self.buttonsearch.pack(side=RIGHT, fill=X)

        self.FrameSearch = Frame(self, bd=5, relief="raise")

        self.CanvasSearch = Canvas(self.FrameSearch)
        self.viewport = Frame(self.CanvasSearch, width=300)
        self.Search_scrollbar = Scrollbar(self.FrameSearch, orient='vertical', command=self.CanvasSearch.yview)
        self.CanvasSearch.configure(yscrollcommand=self.Search_scrollbar.set)
        self.Search_scrollbar.pack(side=RIGHT, fill=Y)
        self.CanvasSearch.pack(side=LEFT, fill=BOTH, expand=1)
        self.Search_window = self.CanvasSearch.create_window((100, 0), window=self.viewport, anchor=NW,
                                                             tags="self.viewport")
        self.viewport.bind("<Configure>", self.OnFrameConfigure)

        self.FrameSearch.pack(side=TOP, fill=BOTH, expand=1, anchor=N)

    def OnFrameConfigure(self, event):
        self.CanvasSearch.configure(scrollregion=self.CanvasSearch.bbox("all"))

    def top10(self):
        for widget in self.viewport.winfo_children():
            widget.destroy()
        recherche = self.Entrysearch.get()
        if recherche == "Music":
            curseur.execute(sql_classement_music)
            l = curseur.fetchall()
            a = 0
            for i in l:
                a = a + 1
                frame = Frame(self.viewport)
                frame.pack(side=TOP, fill=X, expand=1, anchor=NE)
                Label(frame, text="Top " + str(a) + " : ").pack(side='left')
                MusicInfo(frame, Name=i[0], Artist=i[1], Nb_in_Playlist=0, List_for_playlist=[i])

        if recherche == "Artiste":
            l = []
            for i in range(1, curseur.execute(sql_get_nb_compo).fetchone()[0]+1):
                a = curseur.execute(sql_get_sum_listen_compo, (i,)).fetchone()[0]
                if a is not None:
                    l.append([i, a])
            l.sort(key=lambda x: x[1], reverse=True)
            a = 0
            for i in l:
                a = a + 1
                comp = (curseur.execute(sql_get_comp, (i[0],)).fetchone()[0])
                frame = Frame(self.viewport, relief="groove", bd=5)
                frame.pack(side=TOP, fill=X, expand=1, anchor=NE)
                Label(frame, text="Top " + str(a) + " : " + comp).pack(side='left', fill=X)
                Label(frame, text= "\t nb écoute : " + str(i[1])).pack(side='right')

        if recherche == "Genre":
            l = []
            for i in range(1, curseur.execute(sql_get_nb_genre).fetchone()[0] + 1):
                a = curseur.execute(sql_get_sum_listen_genre, (i,)).fetchone()[0]
                if a is not None:
                    l.append([i, a])
            l.sort(key=lambda x: x[1], reverse=True)
            a = 0
            for i in l:
                a = a + 1
                comp = (curseur.execute(sql_get_genre, (i[0],)).fetchone()[0])
                frame = Frame(self.viewport, relief="groove", bd=5)
                frame.pack(side=TOP, fill=X, expand=1, anchor=NE)
                Label(frame, text="Top " + str(a) + " : " + comp).pack(side='left', fill=X)
                Label(frame, text="\t nb écoute : " + str(i[1])).pack(side='right')

    def diagramme(self):
        try:
            import matplotlib.pyplot as plt

        except ModuleNotFoundError:
            pipmain(['install', 'matplotlib'])
            import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        for widget in self.viewport.winfo_children():
            widget.destroy()

        recherche = self.Entrysearch.get()
        if recherche == "Genre":
            l = []
            for i in range(1, curseur.execute(sql_get_nb_genre).fetchone()[0] + 1):
                a = curseur.execute(sql_get_sum_listen_genre, (i,)).fetchone()[0]
                if a is not None:
                    l.append([i, a])
            l.sort(key=lambda x: x[1], reverse=True)
            a = 0
            for i in l:
                a = a + 1
                comp = (curseur.execute(sql_get_genre, (i[0],)).fetchone()[0])

                i[0] = comp
            label = []
            size = []
            for i in l:
                if i[1] != 0:
                    label.append(i[0])
                    size.append(i[1])
        if recherche == "Artiste":
            l = []
            for i in range(1, curseur.execute(sql_get_nb_compo).fetchone()[0]+1):
                a = curseur.execute(sql_get_sum_listen_compo, (i,)).fetchone()[0]
                if a is not None:
                    l.append([i, a])
            l.sort(key=lambda x: x[1], reverse=True)
            a = 0
            for i in l:
                a = a + 1
                comp = (curseur.execute(sql_get_comp, (i[0],)).fetchone()[0])
                i[0] = comp
            label = []
            size = []
            for i in l:
                if i[1] != 0:
                    label.append(i[0])
                    size.append(i[1])
        if recherche == "Genre" or recherche == "Artiste":

            fig1, ax1 = plt.subplots(figsize=(4, 3), dpi=100)
            ax1.pie(size, labels=label, autopct='%1.1f%%', shadow=True, startangle=90)
            ax1.axis('equal')
            canvas = FigureCanvasTkAgg(fig1, master=self.viewport)
            plot_widget = canvas.get_tk_widget()
            plot_widget.grid(row=0, column=0)

# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    connexion = sqlite3.connect("basededonnees.db", check_same_thread=False)
    curseur = connexion.cursor()
    f = Mainwindow()
    f.title("Spotif'Air")
    f.mainloop()
    connexion.commit()
    on_closing()
