# config.py
import os

class Config:
    DEBUG = False
    WATCHDOG_SLEEP_INTERVAL = 20
    CSV_FOLDER_PATH = 'app/storage'

    # Oui bah si t'es veux écrire des tests t'es les écrira tout seul eu'n fois.
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    WATCHDOG_SLEEP_INTERVAL = 10
    
    # Si dans le fichier d'environnement (.env) la variable `CSV_FOLDER_PATH` n'existe pas alors on prend `app/storage` par défaut.
    CSV_FOLDER_PATH = 'app/storage'

class ProductionConfig(Config):
    DEBUG = False
    WATCHDOG_SLEEP_INTERVAL = os.getenv('WATCHDOG_SLEEP_INTERVAL')

    # TODO: Déterminer le dossier partagé contenant les csv.
    CSV_FOLDER_PATH = os.getenv('CSV_FOLDER_PATH')