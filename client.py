import requests
import random
import time
import uuid
from datetime import datetime

# --- CONFIGURATION ---
# Si tu as changé le port dans docker-compose (ex: 8005), change-le ici aussi.
API_URL = "http://localhost:8000/envoyer_ticket"

# Catalogue factice pour générer de la donnée réaliste
CATALOGUE = [
    {"produit": "Ordinateur Portable", "prix": 899.99},
    {"produit": "Souris sans fil", "prix": 25.50},
    {"produit": "Clavier Mécanique", "prix": 120.00},
    {"produit": "Écran 24 pouces", "prix": 180.00},
    {"produit": "Câble HDMI", "prix": 15.00},
    {"produit": "Casque Audio", "prix": 59.90},
    {"produit": "Clé USB 64Go", "prix": 12.00},
]

MAGASINS = ["Paris-Champs", "Lyon-Part-Dieu", "Marseille-Vieux-Port", "Bordeaux-Lac"]

def generer_ticket():
    """Crée un ticket avec des données aléatoires."""
    
    # 1. On choisit entre 1 et 5 articles au hasard
    nb_articles = random.randint(1, 5)
    articles_choisis = []
    total_ticket = 0.0
    
    for _ in range(nb_articles):
        item = random.choice(CATALOGUE)
        qty = random.randint(1, 3)
        
        # On construit l'objet article
        art = {
            "produit": item["produit"],
            "prix": item["prix"],
            "quantite": qty
        }
        articles_choisis.append(art)
        total_ticket += (item["prix"] * qty)

    # 2. Construction du JSON final
    payload = {
        "id_ticket": str(uuid.uuid4()),  # ID unique format texte (ex: f47ac10b-...)
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "magasin": random.choice(MAGASINS),
        "total": round(total_ticket, 2),
        "articles": articles_choisis
    }
    return payload

def envoyer_simulation(nb_tickets=5, intervalle=1):
    """Envoie une série de tickets au serveur."""
    print(f" Démarrage: Envoi de {nb_tickets}")
    
    reussis = 0
    
    for i in range(nb_tickets):
        ticket = generer_ticket()
        
        try:
            print(f"Envoi ticket {i+1}/{nb_tickets} (ID: {ticket['id_ticket']})...")
            response = requests.post(API_URL, json=ticket)
            
            if response.status_code == 200:
                print(f" Succès ! Reçu par le Producer.")
                reussis += 1
            else:
                print(f"Erreur API ({response.status_code}) : {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(" Impossible de se connecter au Producer. Vérifie que Docker tourne et le port 8000.")
            break
            
        time.sleep(intervalle) # Pause pour simuler le temps réel

    print(f"\n--- BILAN ---")
    print(f"Tickets envoyés : {reussis}/{nb_tickets}")

if __name__ == "__main__":
    # Tu peux changer le nombre de tickets ici
    envoyer_simulation(nb_tickets=2, intervalle=1)