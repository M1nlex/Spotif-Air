from tkinter import *
from tkinter import ttk
from tkinter import font
#from tkclass import *

def show_playlist(self, Programme, Name, Number, List, Genre, fenetre_de_retour, fenetre_playlist):
    if (Name == "Erreur" and Number == 0):
        return
    Playlist_Content(Programme=fenetre_playlist, Name=Name, Number=Number, List=List, Genre=Genre, fenetre_de_retour=fenetre_de_retour)
    fenetre_playlist.tkraise()

def return_to_playlist(self, fenetre_de_retour):
    fenetre_de_retour.tkraise()
    self.destroy()

def Launch_music(List_for_playlist, Nb_in_Playlist=0):
    p = []
    for i in List_for_playlist:
        p.append(i[0])
    abc = Musique(p)
    Musique.play(abc, i=Nb_in_Playlist)


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

        self.Playbutton = Button(self, text="Jouer", command=lambda:Launch_music(self.List_for_playlist, self.Nb_in_Playlist))
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
        self.Musiclist.grid(row=2, column=0, columnspan=5)


        self.scrollmusic = Scrollbar(self.Musiclist, orient='vertical')
        self.scrollmusic.pack(side=RIGHT, fill=Y)


        self.Musics = Canvas(self.Musiclist, relief=SUNKEN, bd=2, height=100, width=400, background="blue", yscrollcommand = self.scrollmusic.set, scrollregion=(0, 0, 100, 500))
        self.Musics.pack(side=RIGHT)
        self.Musics.pack_propagate(0)

        l=0
        for i in self.List:
            MusicInfo(self.Musics, Name=i[0], Artist=i[1], Nb_in_Playlist=l, List_for_playlist=self.List)
            l += 1


        #self.Musics.configure(scrollregion = self.Musics.bbox("all"))
        self.scrollmusic.configure(command=self.Musics.yview)


if __name__ == '__main__':
    liste_essai = [ ["Jigsaw Falling Into Place", "Radiohead"], ["Classic Pursuit", "cYsmix"], ["Ma couille", "SAH"], ["wesh alors", "JUL"], ["AU DD", "PNL"] ]
    main = Tk()

    fenetre1 = Frame(main)
    fenetre1.grid(row=0, column=0, sticky = "nsew")

    fenetre2 = Frame(main)
    fenetre2.grid(row=0, column=0, sticky = "nsew")

    Playlist(Programme = fenetre2, Name="yes", Number=2, Genre="Rock")
    Playlist(fenetre2, "essai", 4, liste_essai, "Classique")
    Playlist(fenetre2)
    main.mainloop()
