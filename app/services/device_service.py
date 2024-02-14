'''
    Ce service permet de traiter la logique des appareils enregistrés.
'''

from app.models.base import Database

def recuperer_appareils():
    '''
        Récupère les informations des appareils enregistrés.
    '''
    # Appel à la base de données dans le but de requêter les appareils (le mot clé `with` permet d'ouvrir et de fermer le curseur automatiquement).
    with Database() as db: appareils = db.find_all(f'select hash, name, location, unit, digital, rate, category, threshold, comment from devices order by name')

    # Renvoyer le dictionnaire.
    return appareils

def ajouter_appareils(appareils: list):
    '''
        Ajouter une succession d'appareils, généralement lors de la récupération des données d'un fichier csv converti en json.
        TODO : Adapter avec le nouveau fichier.
        TODO : Éviter qu'il y ai des doublons (OK).
    '''
    with Database() as db:
        for appareil in appareils:
            # Requête paramétrée.
            query = '''
                INSERT INTO devices (hash, name, location, unit, digital, rate, created)
                VALUES (%s, %s, %s, %s, %s, %s, now())
                ON DUPLICATE KEY UPDATE unit = VALUES(unit), digital = VALUES(digital), rate = VALUES(rate)
            '''

            # Exécute la requête.
            db.execute(query, (appareil['equipmentId'], appareil['device'], appareil['location'], appareil['unit'], appareil['digital'], appareil['rate']))

def ajouter_appareil(device):
    '''
        Ajouter un appareil depuis le client ui (device est du json).
    '''
    with Database() as db:
        # Requête paramétrée.
        query = '''
            INSERT INTO devices (hash, name, location, unit, digital, rate, threshold, comment, created)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())
        '''

        # Exécute la requête.
        db.execute(query, (device['hash'], device['name'], device['location'], device['unit'], device['digital'], device['rate'], device['threshold'], device['comment']))