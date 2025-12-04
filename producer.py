from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from kafka import KafkaProducer
import uvicorn
import json

app = FastAPI()

# Connexion Kafka ultra-simplifiée
producer = KafkaProducer(bootstrap_servers='localhost:9092')

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

@app.post("/envoyer_ticket")
def recevoir_ticket(ticket: Ticket):
    message_en_bytes = json.dumps(ticket.model_dump()).encode('utf-8')
    producer.send('tickets_caisse', value=message_en_bytes)
    producer.flush()
    return {"message": "Ticket envoyé", "ticket": ticket.model_dump()}

#========================================
def start_server():
    print('Starting Server...')       
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )

if __name__ == "__main__":
    start_server()