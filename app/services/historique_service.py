'''
    Ce service permet de traiter la logique de l'historique d'importation.
'''

from app.models.base import Database

def recuperer_historique_fichiers():
    '''
        Récupère l'historique de tous les imports depuis la base de données.
    '''
    # Appel à la base de données dans le but de requêter les appareils (le mot clé `with` permet d'ouvrir et de fermer le curseur automatiquement).
    with Database() as db: historique = db.find_all(f'select date_imported, reading_start, reading_end, nb_missing, status from history order by date_imported desc')

    # Renvoyer le dictionnaire.
    return historique