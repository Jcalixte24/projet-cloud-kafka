from fastapi import FastAPI
import sqlite3
import uvicorn

app = FastAPI()

# Base de données 
DB_NAME = "cloudDB.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Pour avoir des réponses lisibles
    return conn

# --- Route 1 : Lire tous les tickets 
@app.get("/tickets")
def lire_historique():
    conn = get_db_connection()
    tickets = conn.execute("SELECT * FROM tickets").fetchall()
    conn.close()
    return {"tickets": tickets}

# --- Route 2 : Lire les stats 
@app.get("/stats/chiffre_affaires")
def lire_stats():
    conn = get_db_connection()
    ca = conn.execute("SELECT magasin, SUM(total) FROM tickets GROUP BY magasin").fetchall()
    conn.close()
    return {"CA": ca}

if __name__ == "__main__":
    # Port 8001 obligatoire car le producer utilise le 8000)
    uvicorn.run(app, host="0.0.0.0", port=8001)