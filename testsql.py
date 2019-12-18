import sqlite3
#from tkinter import *


sql_line_1 = "SELECT Playlists.PL_Name, Playlists.PL_Nb, Playlists.PL_List, Genre.Genre_Name FROM Playlists, Genre WHERE Playlists.PL_genre = Genre.Genre_Id"
sql_line_2_part1 = "SELECT Musique.Music_Name, Compositeur.Compo_Name FROM Musique,Compositeur WHERE Music_Id IN "
sql_line_2_part2=" AND Musique.Compo_Id = Compositeur.Compo_Id"
sql_test_music_exist = """SELECT * FROM Musique WHERE Music_Name = ? AND Music_Link = ?"""
# AND Compo_Id= ? AND Album_Id= ? AND Image_Id= ? AND Genre_Id= ?

connexion = sqlite3.connect("basededonnees.db", check_same_thread=False)
curseur = connexion.cursor()


curseur.execute(sql_test_music_exist , ('Test', 'blabla'))
# , 4, 2, 3, 5

print(curseur.fetchone()[0])

connexion.close()
