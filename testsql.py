import sqlite3


sql_line_1 = "SELECT Playlists.PL_Name, Playlists.PL_Nb, Playlists.PL_List, Genre.Genre_Name FROM Playlists, Genre WHERE Playlists.PL_genre = Genre.Genre_Id"
sql_line_2_part1 = "SELECT Musique.Music_Name, Compositeur.Compo_Name FROM Musique,Compositeur WHERE Music_Id IN "
sql_line_2_part2=" AND Musique.Compo_Id = Compositeur.Compo_Id"

connexion = sqlite3.connect("basededonnees.db", check_same_thread=False)
curseur = connexion.cursor()





curseur.execute(sql_line_1)
result_d = curseur.fetchall()
result_f = []
for i in result_d:
    result_f.append( [ i[0], i[1], i[2].split(";"), i[3] ] )
for i in result_f:
    curseur.execute(sql_line_2_part1 + "(" + ",".join(i[2]) + ")" + sql_line_2_part2 )
    res2 = curseur.fetchall()
    i[2]=res2


print(result_f)
print("[['Radiohead Classics', 2, [('Jigsaw Falling Into Place', 'Radiohead'), ('Optimistic', 'Radiohead')], 'Rock']]")

connexion.close()

m = [1,"gfrez",3,4]
print(m[1:])
