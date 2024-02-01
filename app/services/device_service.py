'''
    Ce service permet de traiter la logique de récupération des capteurs récemment ajoutés.
'''

from app.dao.devices import DeviceDAO

def find_devices():
    '''
        Récupère l'historique de tous les imports depuis la base de données.
    '''
    import_dao = DeviceDAO()
    return import_dao.find_devices()