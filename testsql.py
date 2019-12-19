import sqlite3
#from tkinter import *


sql_line_1 = "SELECT Playlists.PL_Name, Playlists.PL_Nb, Playlists.PL_List, Genre.Genre_Name FROM Playlists, Genre WHERE Playlists.PL_genre = Genre.Genre_Id"
sql_line_2_part1 = "SELECT Musique.Music_Name, Compositeur.Compo_Name FROM Musique,Compositeur WHERE Music_Id IN "
sql_line_2_part2=" AND Musique.Compo_Id = Compositeur.Compo_Id"
sql_test_music_exist = """SELECT COUNT(1) FROM Musique WHERE Music_Name = ? AND Compo_Id= ( SELECT Compo_Id FROM Compositeur WHERE Compo_Name= ? ) AND Album_Id= ( SELECT Album_Id FROM Album WHERE Album_Name= ? ) AND Genre_Id= ( SELECT Genre_Id FROM Genre WHERE Genre_Name= ? )"""

Compositeur = 'Chopin'

connexion = sqlite3.connect("basededonnees.db", check_same_thread=False)
curseur = connexion.cursor()

curseur.execute("SELECT COUNT(1) FROM Compositeur WHERE Compo_Name= ?", ("Chopin",) )


print(curseur.fetchone()[0])

connexion.close()
