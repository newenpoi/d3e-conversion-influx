# app/models/__init__.py
import os
from colorama import Fore # Haut en couleurs.

from .base import Database
from .aksm.device import Device
from .aksm.history import History

'''
    TODO : Il faudra voir pour un fichier d'environnement par société, genre aksm.env, societex.env, etc...
'''

def setup():
    '''
        Initialize les bases de données et leurs schémas.
    '''
    with Database() as db:
        print(Fore.YELLOW + "Création de la base de données pour AKSM.")
        
        # Créé la base de données (on pourrait avoir un fichier avec une liste de db à créer).
        db.create_database(os.getenv('MYSQL_DB'))

        # On se positionne sur la base.
        db.execute(f"USE {os.getenv('MYSQL_DATABASE')}")
        
        print(Fore.YELLOW + "Préparation du schéma sql.")
        
        # Créé les tables.
        db.execute(Device.model)
        db.execute(History.model)

        print(Fore.LIGHTGREEN_EX + "Exécution du schéma terminé.")