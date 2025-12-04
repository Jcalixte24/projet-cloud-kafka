from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from kafka import KafkaProducer
import uvicorn
import json
import os

app = FastAPI()

# Connexion directe à Kafka (sans attente de sécurité)
KAFKA_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# --- Modèles de données ---
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

# --- Route POST ---
@app.post("/envoyer_ticket")
def recevoir_ticket(ticket: Ticket):
    # Envoi direct dans le topic 'tickets_caisse'
    producer.send('tickets_caisse', value=ticket.model_dump())
    producer.flush()
    return {"message": "Ticket envoyé", "id": ticket.id_ticket}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)