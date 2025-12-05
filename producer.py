from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from kafka import KafkaProducer
import uvicorn
import json
import os
import time

app = FastAPI()

# --- CONFIGURATION KAFKA ---
KAFKA_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
producer = None

# Boucle de connexion robuste
print(f"⏳ Tentative de connexion à Kafka sur {KAFKA_SERVER}...")
for i in range(30): # On essaie pendant 30 fois (environ 1 min)
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        print("✅ Producer connecté à Kafka !")
        break
    except Exception as e:
        print(f"⚠️ Essai {i+1}/30 échoué. Kafka n'est pas prêt. Nouvelle tentative dans 2s...")
        time.sleep(2)

if producer is None:
    print("❌ ECHEC CRITIQUE : Impossible de se connecter à Kafka après 60s.")

# --- MODÈLES ---
class Article(BaseModel):
    produit: str
    prix: float
    quantite: int

class Ticket(BaseModel):
    id_ticket: str
    date: str
    magasin: str
    total: float
    articles: List[Article]

# --- ROUTE POST ---
@app.post("/envoyer_ticket")
def recevoir_ticket(ticket: Ticket):
    if producer:
        try:
            producer.send('tickets_caisse', value=ticket.model_dump())
            producer.flush()
            return {"message": "Ticket envoyé", "id": ticket.id_ticket}
        except Exception as e:
            return {"error": f"Erreur lors de l'envoi Kafka : {str(e)}"}
    else:
        return {"error": "Kafka non connecté"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)