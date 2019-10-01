import sqlite3
connexion = sqlite3.connect("basededonnees.db")
curseur = connexion.cursor()

donnee = ("Wii Main Theme", )
curseur.execute("SELECT Compositeur FROM Musique WHERE Nom = ?", donnee)
print(curseur.fetchone())

