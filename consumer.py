from kafka import KafkaConsumer
import json
import os
from database import create_tables, insert_ticket, insert_article

# 1. Initialisation directe
create_tables()
KAFKA_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# 2. Connexion directe (Si Kafka n'est pas là, ça plante ici)
print(f"Connexion à Kafka sur {KAFKA_SERVER}...")
consumer = KafkaConsumer(
    'tickets_caisse',
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset='earliest',
    group_id='groupe_worker_sqlite',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)
print("Connecté !")

# 3. Boucle de travail brute
for message in consumer:
    ticket = message.value
    print(f"Traitement du ticket : {ticket.get('id_ticket')}")

    # Enregistrement direct (Si erreur SQL, ça plante ici)
    insert_ticket(
        ticket['id_ticket'], 
        ticket['date'], 
        ticket['magasin'], 
        ticket['total']
    )

    if 'articles' in ticket:
        for art in ticket['articles']:
            insert_article(
                ticket['id_ticket'],
                art['produit'],
                art['quantite'],
                art['prix']
            )
            
    print("OK.")