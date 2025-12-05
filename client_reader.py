import requests

# URL de l'API de lecture (Reader)
URL = "http://localhost:8001"

def lire_tickets():
    print("--- LISTE DES TICKETS ---")
    try:
        # On interroge la route /tickets
        reponse = requests.get(f"{URL}/tickets")
        
        if reponse.status_code == 200:
            donnees = reponse.json()
            tickets = donnees.get("tickets", [])
            
            print(f"Nombre total de tickets : {len(tickets)}")
            
            # On affiche chaque ticket ligne par ligne
            for t in tickets:
                print(t)
        else:
            print(f"Erreur serveur : {reponse.status_code}")
            
    except Exception as e:
        print(f"Impossible de se connecter : {e}")

def lire_stats():
    print("\n--- CHIFFRE D'AFFAIRES ---")
    try:
        # On interroge la route des statistiques
        reponse = requests.get(f"{URL}/stats/chiffre_affaires")
        
        if reponse.status_code == 200:
            donnees = reponse.json()
            # On affiche directement le résultat brut (liste des magasins et totaux)
            print(donnees.get("CA"))
        else:
            print(f"Erreur serveur : {reponse.status_code}")

    except Exception as e:
        print(f"Impossible de se connecter : {e}")

if __name__ == "__main__":
    lire_tickets()
    lire_stats()