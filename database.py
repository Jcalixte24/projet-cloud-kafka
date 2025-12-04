import sqlite3
def connexion():
    return sqlite3.Connection("cloudDB.db")

def create_table_ticket():
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            commande =  """ CREATE TABLE tickets (
                                id_ticket INTEGER PRIMARY KEY,
                                date_achat TEXT,
                                magasin VARCHAR(60),
                                total REAL
                                );"""
            cursor.execute(commande)
            conn.commit()

    except Exception as e:
        print(f"l'erreur est {e}")


def create_table_article():
    try:
        with connexion() as conn : 
            cursor = conn.cursor()
            commande = """CREATE TABLE article(
                            id_article INTEGER PRIMARY KEY, 
                            id_ticket INTEGER,                          
                            Article VARCHAR(60),
                            quantite REAL,
                            prix_unitaire REAL,
                            FOREIN KEY(id_ticket) REFERENCES Tickets(id_ticket) ON DELETE CASCADE
                            );"""
            cursor.execute(commande)
            conn.commit()
    except Exception as e :
        print(f"l'erreur est {e}")

def insert_titcket(id_ticket:int, date_achat:str, magasin:str, total:float|int):
    try:
        with connexion() as conn : 
            cursor = conn.cursor()
            commande = """ INSERT INTO Tickets (id_ticket, date_achat, magasin,total) VALUES (?,?,?,?)"""
            cursor.execute(commande,  _Parameters = (id_ticket, date_achat, magasin , total))
            conn.commit()


    except Exception as e : 
        print(f"l'erreure est {e}")

def insert_article(id_article: int, id_ticket:int , Article:str, quantite:float, prix_unitaire:float):
    try:
        with connexion() as conn :
            cursor = conn.cursor()
            commande = """ INSERT INTO Article (id_article, id_ticket, Article, quantite, prix_unitaire) VALUES (?,?,?,?,?)"""
            cursor.execute(commande,  _Parameters = (id_article, id_ticket, Article, quantite, prix_unitaire))
            conn.commit()
    except Exception as e:
        print(f"l'erreur est {e}")



