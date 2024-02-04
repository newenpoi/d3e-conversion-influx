# app/models/import.py

'''
    Avec MongoDB les schémas sont inutiles, néanmoins on anticipe pour plus tard et ça permet de se mettre d'accord sur la structure.
'''

class ImportRecord:
    def __init__(self, csvFileName, uploadDateTime, processedDateTime = None):
        self.csvFileName = csvFileName
        self.uploadDateTime = uploadDateTime
        self.processedDateTime = processedDateTime

    # Method to save instance to MongoDB
    def save(self, db):
        db.imports.insert_one(self.to_dict())

    # Convert instance to dictionary suitable for MongoDB
    def to_dict(self):
        return {
            "csvFileName": self.csvFileName,
            "uploadDateTime": self.uploadDateTime,
            "processedDateTime": self.processedDateTime
        }