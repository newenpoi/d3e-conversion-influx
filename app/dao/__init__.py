# app/dao/__init__.py
from pymongo import MongoClient
import os

# Données de configuration récupérées depuis les variables d'environnement.
MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('MONGODB_DB_NAME')

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

def indexation(db):
    # Pour des requêtes très performantes on utilise l'indexation.
    db.devices.create_index([('equipmentId', 1)], unique = True)
    db.devices.create_index([('date', 1)])

    # On peut rajouter davantage d'indexations ci-dessous.
    # ...