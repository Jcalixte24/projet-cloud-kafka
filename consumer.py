from kafka import KafkaConsumer
import json
import time
import os
from database import create_tables, insert_ticket, insert_article

# 1. On prépare la base de données
print("⏳ Démarrage du Consumer...")
create_tables()

# 2. On se connecte à 
consumer = None
while not consumer:
    try:
        consumer = KafkaConsumer(
            'tickets_caisse',
            bootstrap_servers=[os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')],
            auto_offset_reset='earliest',       # Lit les vieux messages ratés
            group_id='groupe_sqlite',           # ID du groupe de travailleurs
            value_deserializer=lambda x: json.loads(x.decode('utf-8')) # Décode le JSON
        )
        print("✅ Connecté à Kafka !")
    except:
        print("⚠️ En attente de Kafka...")
        time.sleep(2)

# 3. La boucle de travail infinie
print("🎧 Prêt à travailler...")

for message in consumer:
    ticket = message.value
    print(f"📥 Nouveau ticket reçu : {ticket.get('id_ticket')}")

    # A. On sauvegarde l'entête (Date, Magasin, Total)
    insert_ticket(
        ticket['id_ticket'], 
        ticket['date'], 
        ticket['magasin'], 
        ticket['total']
    )

    # B. On sauvegarde les articles (Pommes, Eau...)
    if 'articles' in ticket:
        for art in ticket['articles']:
            insert_article(
                ticket['id_ticket'],
                art['produit'],
                art['quantite'],
                art['prix']
            )
    
    print("💾 Ticket sauvegardé en base de données.")