# app/dao/__init__.py
from pymongo import MongoClient
import os

# Données de configuration récupérées depuis les variables d'environnement.
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'influx')

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

def initialize():
    # Liste des collections requises.
    required_collections = ['imports', 'devices']

    # Liste des collections existantes.
    existing_collections = db.list_collection_names()
    
    # Pour chaque collection on vérifie qu'elle existe sinon on tente de la créer.
    for collection in required_collections:
        if collection not in existing_collections:
            try:
                db.create_collection(collection)
                print(f"La collection {collection} a été créée avec succès.")
            except:
                # This block might actually never be reached due to the check against existing_collections
                print(f"La collection {collection} existe déjà.")