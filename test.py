import requests
import json
import time

# --- CONFIGURATION ---
URL_PRODUCER = "http://localhost:8000"
URL_READER   = "http://localhost:8001"

print("--- 🚀 DÉBUT DU TEST CLIENT ROBUSTE ---")

# 1. Création d'un ticket UNIQUE (pour être sûr de le repérer)
id_unique = f"T-TEST-{int(time.time())}"
ticket_test = {
    "id_ticket": id_unique,
    "date": "2023-12-06",
    "magasin": "Debug-Store",
    "total": 42.0,
    "articles": [{"produit": "Test-Item", "prix": 42.0, "quantite": 1}]
}

# 2. Envoi au Producer
print(f"📡 Envoi du ticket {id_unique} au Producer...")
try:
    resp = requests.post(f"{URL_PRODUCER}/envoyer_ticket", json=ticket_test)
    if resp.status_code == 200:
        print(f"✅ Producer a répondu : {resp.json()}")
    else:
        print(f"❌ Erreur Producer ({resp.status_code}) : {resp.text}")
        exit() # On arrête si l'envoi échoue
except Exception as e:
    print(f"❌ Impossible de joindre le Producer : {e}")
    exit()

# 3. Boucle de vérification (Polling)
print(f"\n🔍 Recherche du ticket {id_unique} dans la base via le Reader...")
ticket_trouve = False

# On va vérifier toutes les 2 secondes pendant 20 secondes max
for i in range(10):
    time.sleep(2) 
    print(f"   Essai {i+1}/10...")
    
    try:
        resp = requests.get(f"{URL_READER}/tickets")
        if resp.status_code == 200:
            data = resp.json()
            tickets = data.get("tickets", [])
            
            # On cherche notre ID spécifique dans la liste
            # La structure dépend de ton reader.py (liste de listes ou de dicts)
            for t in tickets:
                # Si c'est une liste : t[0] est l'id
                # Si c'est un dict : t['id_ticket'] est l'id
                valeur_id = t[0] if isinstance(t, list) else t.get('id_ticket')
                
                if valeur_id == id_unique:
                    ticket_trouve = True
                    print(f"\n🎉 SUCCÈS ! Le ticket {id_unique} a été trouvé en base !")
                    print(f"   Détail : {t}")
                    break
        
        if ticket_trouve:
            break
            
    except Exception as e:
        print(f"   ⚠️ Erreur temporaire du Reader : {e}")

if not ticket_trouve:
    print("\n❌ ÉCHEC : Le ticket n'est jamais apparu dans la base après 20s.")
    print("👉 Pistes à vérifier :")
    print("   1. Regarde les logs du consumer : 'docker logs consumer_worker'")
    print("   2. Vérifie que le Consumer et le Reader partagent le même volume docker.")

print("\n--- FIN DU TEST ---")