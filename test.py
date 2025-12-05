import requests
import json

# L'URL du Reader (Port 8001 défini dans docker-compose)
URL_READER = "http://localhost:8001/tickets"

def verifier_la_base():
    print(f"🔍 Interrogation de la base de données via {URL_READER}...")
    
    try:
        # On fait une requête GET (Lecture)
        response = requests.get(URL_READER)
        
        if response.status_code == 200:
            data = response.json()
            tickets = data.get("tickets", [])
            
            nombre = len(tickets)
            print(f"\n✅ RÉUSSITE : {nombre} tickets trouvés en base de données !")
            
            if nombre > 0:
                print("\n📜 Voici les 3 derniers tickets enregistrés :")
                # On affiche les 3 derniers pour vérifier (slicing python [-3:])
                for t in tickets[-3:]:
                    print(f"   - {t}")
            else:
                print("   (La base est vide pour l'instant)")
                
        else:
            print(f"❌ Erreur Reader ({response.status_code}) : {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de joindre le Reader sur le port 8001.")
        print("   👉 Vérifie que le conteneur 'api_read' tourne bien.")

if __name__ == "__main__":
    verifier_la_base()