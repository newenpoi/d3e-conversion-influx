'''
    Ce service permet de traiter la logique de l'historique d'importation.
'''

from app.dao.imports import ImportDAO

def find_history_imports():
    '''
        Récupère l'historique de tous les imports depuis la base de données.
    '''
    import_dao = ImportDAO()
    return import_dao.find_history()