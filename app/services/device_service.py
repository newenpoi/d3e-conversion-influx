'''
    Ce service permet de traiter la logique des appareils enregistrés.
'''

from app.models.base import Database

def recuperer_historique_fichiers():
    '''
        Récupère les informations des appareils enregistrés.
    '''
    # Appel à la base de données dans le but de requêter les appareils (le mot clé `with` permet d'ouvrir et de fermer le curseur automatiquement).
    with Database() as db: appareils = db.find_all(f'select hash, name, location, unit, digital, rate, category, threshold, comment from devices order by name')

    # Renvoyer le dictionnaire.
    return appareils

def ajouter_appareils(appareils: list):
    with Database() as db:
        for appareil in appareils:
            # Requête paramétrée.
            query = '''
                INSERT INTO devices (hash, name, location, unit, digital, rate, created)
                VALUES (%s, %s, %s, %s, %s, %s, now())
            '''

            # Exécute la requête.
            db.execute(query, (appareil['equipmentId'], appareil['device'], appareil['location'], appareil['unit'], appareil['digital'], appareil['rate']))