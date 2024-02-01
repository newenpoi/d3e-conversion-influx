# app/models/import.py
from pymongo import MongoClient

class ImportRecord:
    def __init__(self, db):
        self.collection = db.imports

    def insert_import_record(self, import_data):
        return self.collection.insert_one(import_data).inserted_id