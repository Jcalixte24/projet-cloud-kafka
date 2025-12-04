FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances
RUN pip install fastapi uvicorn kafka-python pydantic

# IMPORTANT : On copie TOUS les fichiers du dossier courant (.) vers le conteneur (.)
COPY . .

# Commande par défaut (sera écrasée par le consumer dans le docker-compose)
CMD ["uvicorn", "producer:app", "--host", "0.0.0.0", "--port", "8000"]