if __name__ == '__main__':
    liste_essai = [ ["Jigsaw Falling Into Place", "Radiohead"], ["Classic Pursuit", "cYsmix"] ]
    from tkinter import *
    from tkinter import ttk
    from tkinter import font

def show_playlist(self, Programme, Name, Number, List, Genre):
    if (Name == "Erreur" and Number == 0):
        return
    Playlist_Content(Programme=fenetre1, Name=Name, Number=Number, List=List, Genre=Genre)
    fenetre1.tkraise()

def return_to_playlist(self):
    fenetre2.tkraise()
    self.destroy()

class Playlist(Frame):

    def __init__(self, Programme=None, Name="Erreur", Number=0, List=[], Genre="None"):
        self.Programme = Programme
        self.Name = StringVar()
        self.Number = IntVar()
        self.List = List
        self.Genre = StringVar()

        self.Name.set(Name)
        self.Number.set(Number)
        self.Genre.set(Genre)

        Frame.__init__(self, Programme, relief = SUNKEN, bd = 5)
        self.pack(fill = BOTH)

        self.LabelName = Label(self, textvariable = self.Name)
        self.LabelName.pack(side=LEFT, fill=BOTH, expand=1)

        self.Confirm_PL = Button(self, text = "Voir la Playlist", command=lambda:show_playlist(self, self.Programme, self.Name.get(), self.Number.get(), self.List, self.Genre.get()))
        self.Confirm_PL.pack(side=RIGHT, fill=BOTH)

        self.LabelGenre = Label(self, textvariable = self.Genre)
        self.LabelGenre.pack(side=RIGHT, fill=BOTH, expand=1)

        self.LabelNumber = Label(self, textvariable = self.Number)
        self.LabelNumber.pack(side=RIGHT, fill=BOTH, expand=1)

class MusicInfo(Frame):

    def __init__(self, Programme=None, Name="", Artist=""):

        self.Name=Name
        self.Artist=Artist

        Frame.__init__(self, Programme, bd=2, relief="groove")
        self.pack(fill = BOTH)

        self.labelname = Label(self, text=self.Name)
        self.labelname.pack(side=LEFT, fill=BOTH, expand=1)

        self.Playbutton = Button(self, text="Jouer")
        self.Playbutton.pack(side=RIGHT, fill=BOTH)

        self.labelartist = Label(self, text=self.Artist)
        self.labelartist.pack(side=RIGHT, fill=BOTH, expand=1)



class Playlist_Content(Frame):

    def __init__(self, Programme=None, Name="", Number=0, List=[], Genre="Rien"):
        self.Programme = Programme
        self.Name = StringVar()
        self.Number = IntVar()
        self.List = List
        self.Genre = StringVar()



        self.Name.set(Name)
        self.Number.set(Number)
        self.Genre.set(Genre)

        Frame.__init__(self, Programme, bd = 5)
        self.pack(fill = BOTH)

        self.leavebutton = Button(self, text="Playlists", command=lambda:return_to_playlist(self))
        self.leavebutton.grid(row=0, column=0, rowspan=2, sticky="ns")

        self.labelname = Label(self, textvariable=self.Name,)
        self.labelname.grid(row=0, column=1, rowspan=2, sticky="nsew")

        self.Labelfornumber = Label(self, text="Nombre de musiques :")
        self.Labelfornumber.grid(row=0, column=3)

        self.LabelNumber = Label(self, textvariable=self.Number)
        self.LabelNumber.grid(row=0, column=4)

        self.Labelforgenre = Label(self, text="Genre :")
        self.Labelforgenre.grid(row=1, column=3)

        self.LabelGenre = Label(self, textvariable=self.Genre)
        self.LabelGenre.grid(row=1, column=4)

        self.Musics = Frame(self, relief=SUNKEN, bd=5, padx=5, pady=5)
        self.Musics.grid(row=2, column=0, columnspan=4, sticky="nsew")

        for i in self.List:
            MusicInfo(self.Musics, Name=i[0], Artist=i[1])


if __name__ == '__main__':
    main = Tk()

    fenetre1 = Frame(main)
    fenetre1.grid(row=0, column=0, sticky = "nsew")

    fenetre2 = Frame(main)
    fenetre2.grid(row=0, column=0, sticky = "nsew")

    Playlist(Programme = fenetre2, Name="yes", Number=2, Genre="Rock")
    Playlist(fenetre2, "essai", 4, liste_essai, "Classique")
    Playlist(fenetre2)
    main.mainloop()
