import sqlite3
def connexion():
    return sqlite3.connect("cloudDB.db")

def create_table_ticket():
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            commande =  """ CREATE TABLE IF NOT EXISTS tickets(
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
            commande = """CREATE TABLE IF NOT EXISTS article(
                            id_article INTEGER PRIMARY KEY, 
                            id_ticket INTEGER,                          
                            Article VARCHAR(60),
                            quantite REAL,
                            prix_unitaire REAL,
                            FOREIGN KEY(id_ticket) REFERENCES Tickets(id_ticket) ON DELETE CASCADE
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
            cursor.execute(commande,(id_ticket, date_achat, magasin , total))
            conn.commit()


    except Exception as e : 
        print(f"l'erreure est {e}")

def insert_article(id_article: int, id_ticket:int , Article:str, quantite:float, prix_unitaire:float):
    try:
        with connexion() as conn :
            cursor = conn.cursor()
            commande = """ INSERT INTO Article (id_article, id_ticket, Article, quantite, prix_unitaire) VALUES (?,?,?,?,?)"""
            cursor.execute(commande,(id_article, id_ticket, Article, quantite, prix_unitaire))
            conn.commit()
    except Exception as e:
        print(f"l'erreur est {e}")


create_table_article()
create_table_ticket()
insert_titcket(1, "2002", "moi", 100.0)
insert_article(1, 1, "rien", 20.0, 20.)
