from tkinter import *
from tkinter.messagebox import *
import sqlite3

class Creator(Toplevel):

    def __init__(self,conteneur):

        Toplevel.__init__(self,conteneur)

        self.titlelabel = Label(self,text="Ajouter une musique").grid(row=0,column=0,columnspan=3)


        self.Label_lien_music = Label(self,text="Fichier musique (format ogg)").grid(row=1,column=1)
        self.lien_music = Entry(self)
        self.lien_music.grid(row=1,column=1)

        self.Label_lien_image = Label(self,text="Fichier musique (format ogg)").grid(row=1,column=2)
        self.lien_image = Entry(self)
        self.lien_image.grid(row=2,column=1)

        self.Name = Entry(self)
        self.Name.grid(row=3,column=1)

        self.Compo = Entry(self)
        self.Compo.grid(row=4,column=1)

        self.Album = Entry(self)
        self.Album.grid(row=5,column=1)

        self.Genre = Entry(self)
        self.Genre.grid(row=6,column=1)



if __name__ == '__main__':
    necessary = Tk()
    fen = Creator(necessary)

    necessary.mainloop()


"""
Music_Name
Music_Link
Music_Length
Compo_Id
Album_Id
Image_Id
Genre_Id
"""
