import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Projet Cloud", layout="wide")
st.title("🛒 Dashboard Microservices")

URL_WRITE = "http://localhost:8000"
URL_READ  = "http://localhost:8001"

# --- GAUCHE : ENVOI ---
with st.sidebar:
    st.header("Envoyer Ticket")
    id_ticket = st.text_input("ID", value=f"T-{int(time.time())}")
    nb_pommes = st.number_input("Pommes", 1, 10, 1)
    
    if st.button("Envoyer"):
        payload = {
            "id_ticket": id_ticket,
            "date": time.strftime("%Y-%m-%d %H:%M"),
            "magasin": "Paris",
            "total": nb_pommes * 2.0,
            "articles": [{"produit": "Pomme", "prix": 2.0, "quantite": nb_pommes}]
        }
        try:
            requests.post(f"{URL_WRITE}/envoyer_ticket", json=payload)
            st.success("Envoyé !")
            time.sleep(1)
            st.rerun()
        except:
            st.error("Producer (8000) éteint")

# --- DROITE : LECTURE ---
st.header("Données en Temps Réel")
try:
    res = requests.get(f"{URL_READ}/tickets")
    data = res.json().get("tickets", [])
    
    if data:
        # On adapte les colonnes à ta base
        df = pd.DataFrame(data, columns=["ID", "Date", "Magasin", "Total"])
        st.dataframe(df, use_container_width=True)
        st.metric("Chiffre d'Affaires", f"{df['Total'].sum()} €")
    else:
        st.info("Base vide")
except:
    st.error("Reader (8001) éteint")