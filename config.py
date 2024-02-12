# config.py
import os
from dotenv import load_dotenv

'''
    TODO : Mettre à jour ce fichier de configuration, utiliser exclusivement celui ci qui charge les variables env en fonction de l'environnement.
'''

# Données des variables d'environnement contenues dans le fichier .env qui est ignoré par notre git.
load_dotenv()

class Config:
    WATCHDOG_SLEEP_INTERVAL = os.getenv('WATCHDOG_SLEEP_INTERVAL')

class DevelopmentConfig(Config):
    DEBUG = True
    
    # Si dans le fichier d'environnement (.env) la variable `CSV_FOLDER_PATH` n'existe pas alors on prend `app/storage` par défaut.
    CSV_FOLDER_PATH = 'app/storage'

    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_USERNAME = "root"
    MYSQL_PASSWORD = ".Logme1nn"
    MYSQL_DATABASE = "aksm"
    MYSQL_AUTOCOMMIT = True

class ProductionConfig(Config):
    DEBUG = False

    # TODO: Déterminer le dossier partagé contenant les csv.
    CSV_FOLDER_PATH = os.getenv('CSV_FOLDER_PATH')

    MYSQL_HOST = ""
    MYSQL_PORT = 0000
    MYSQL_USERNAME = ""
    MYSQL_PASSWORD = ""
    MYSQL_DATABASE = ""
    MYSQL_AUTOCOMMIT = True