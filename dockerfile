FROM python:3.9-slim

WORKDIR /app

# On installe les librairies nécessaires
# (On peut aussi utiliser un requirements.txt, mais ici c'est plus direct)
RUN pip install fastapi uvicorn kafka-python pydantic

# COPIE CORRIGÉE : On copie le script depuis le dossier Projet vers le conteneur
# Attention : Docker utilise des slashs "/" même si tu es sur Windows
COPY producer.py .

CMD ["uvicorn", "producer:app", "--host", "0.0.0.0", "--port", "8000"]