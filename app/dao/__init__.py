# app/dao/__init__.py
from pymongo import MongoClient
import os

# Données de configuration récupérées depuis les variables d'environnement.
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'influx')

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]