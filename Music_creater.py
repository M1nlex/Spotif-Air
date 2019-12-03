from tkinter import *
from tkinter.messagebox import *
import sqlite3

class Creator(Toplevel):

    def __init__(self):
        self.title = Label(self,text="Ajouter une musique").grid(row=0,column=0,columnspan=3)
        




if __name__ == '__main__':
    necessary = Tk()
    fen = Creator()
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
