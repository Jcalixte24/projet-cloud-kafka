import sqlite3

# Connexion au fichier créé par le Consumer
conn = sqlite3.connect('cloudDB.db')
cursor = conn.cursor()

print("--- CONTENU DES TICKETS ---")
try:
    for row in cursor.execute("SELECT * FROM tickets"):
        print(row)
except Exception as e:
    print("Pas de table tickets ou base vide:", e)

conn.close()