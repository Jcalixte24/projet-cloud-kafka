import sqlite3

DB_NAME = "cloudDB.db"

def connexion():
    return sqlite3.connect(DB_NAME)

def create_tables():
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            
            # Table Tickets
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id_ticket TEXT PRIMARY KEY,
                    date_achat TEXT,
                    magasin TEXT,
                    total REAL
                );
            """)
            
            # Table Articles
            # J'ai corrigé la syntaxe FOREIGN KEY
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_ticket TEXT,
                    produit TEXT,
                    quantite INTEGER,
                    prix_unitaire REAL,
                    FOREIGN KEY(id_ticket) REFERENCES tickets(id_ticket) ON DELETE CASCADE
                );
            """)
            conn.commit()
            print("✅ Tables SQLite vérifiées/créées.")
    except Exception as e:
        print(f"❌ Erreur création tables : {e}")

def insert_ticket(id_ticket, date_achat, magasin, total):
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            # On utilise INSERT OR IGNORE pour éviter de planter si le ticket existe déjà
            cursor.execute(
                "INSERT OR IGNORE INTO tickets (id_ticket, date_achat, magasin, total) VALUES (?, ?, ?, ?)",
                (id_ticket, date_achat, magasin, total)
            )
            conn.commit()
    except Exception as e:
        print(f"❌ Erreur insert ticket : {e}")

def insert_article(id_ticket, produit, quantite, prix_unitaire):
    try:
        with connexion() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO articles (id_ticket, produit, quantite, prix_unitaire) VALUES (?, ?, ?, ?)",
                (id_ticket, produit, quantite, prix_unitaire)
            )
            conn.commit()
    except Exception as e:
        print(f"❌ Erreur insert article : {e}")