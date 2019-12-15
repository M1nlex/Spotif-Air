if __name__ == '__main__':
    from tkinter import *
    from tkinter import ttk
    from tkinter import font

def testcommand(self, Programme, Name, Number, List, Genre):

    # print(self.Name.get())
    Playlist_Content(fenetre1)
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

        self.Confirm_PL = Button(self, text = "Voir la Playlist", command=lambda:testcommand(self, self.Programme, self.Name, self.Number, self.List, self.Genre))
        self.Confirm_PL.pack(side=RIGHT, fill=BOTH)

        self.LabelGenre = Label(self, textvariable = self.Genre)
        self.LabelGenre.pack(side=RIGHT, fill=BOTH, expand=1)

        self.LabelNumber = Label(self, textvariable = self.Number)
        self.LabelNumber.pack(side=RIGHT, fill=BOTH, expand=1)



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
        self.leavebutton.pack()


if __name__ == '__main__':
    main = Tk()

    fenetre1 = Frame(main)
    fenetre1.grid(row=0, column=0, sticky = "nsew")

    fenetre2 = Frame(main)
    fenetre2.grid(row=0, column=0, sticky = "nsew")

    Playlist(Programme = fenetre2, Name="yes", Number=2, Genre="Rock")
    Playlist(fenetre2, "essai", 4, [], "Classique")
    Playlist(fenetre2)
    main.mainloop()
