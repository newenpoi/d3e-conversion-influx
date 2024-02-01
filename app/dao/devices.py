# app/dao/devices.py
from . import db

class DeviceDAO:
    def __init__(self):
        # Mongo en déduis automatiquement le nom de la collection (ici devices).
        self.collection = db.devices

    def find_devices(self):
        '''
            Renvoie la collection des capteurs.
        '''
        return list(self.collection.find())
