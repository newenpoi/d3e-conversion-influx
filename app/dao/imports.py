# app/dao/imports.py
from . import db

class ImportDAO:
    def __init__(self):
        # Mongo en déduis automatiquement le nom de la collection (ici imports).
        self.collection = db.imports

    def find_history(self):
        '''
            Renvoie la collection des imports triés par date d'import.
        '''
        return list(self.collection.find().sort('uploadDateTime', -1))
