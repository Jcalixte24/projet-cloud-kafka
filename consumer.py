from kafka import KafkaConsumer
import json
import os
import time
# IMPORT ADAPTÉ
from database import create_table_ticket, create_table_article, insert_ticket, insert_article

print("⏳ Initialisation de la base de données...")
create_table_ticket()
create_table_article()

# Connexion Kafka
KAFKA_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
print(f"Connexion à Kafka sur {KAFKA_SERVER}...")

consumer = None

for i in range(30):  # On tente pendant 60 secondes max
    try:
        consumer = KafkaConsumer(
            'tickets_caisse',
            bootstrap_servers=[KAFKA_SERVER],
            auto_offset_reset='earliest',
            group_id='groupe_worker_sqlite_v2',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        print(" Connecté à Kafka !")
        break
    except Exception as e:
        time.sleep(2)

if consumer is None:
    print("❌ Erreur critique : Impossible de joindre Kafka.")
    exit(1)
# --------------------------------------------

# Boucle de travail
print("🎧 En attente de messages...")
for message in consumer:
    ticket = message.value
    print(f"Traitement du ticket : {ticket.get('id_ticket')}")

    # 1. Insertion Ticket
    insert_ticket(
        ticket['id_ticket'], 
        ticket['date'], 
        ticket['magasin'], 
        ticket['total']
    )

    # 2. Insertion Articles
    if 'articles' in ticket:
        for art in ticket['articles']:
            # Rappel : assurez-vous que database.py est bien corrigé (4 arguments)
            insert_article(
                ticket['id_ticket'],
                art['produit'],
                art['quantite'],
                art['prix']
            )
            
    print("Sauvegardé.")