# app/models/device.py
from pymongo import MongoClient

class Device:
    def __init__(self, db):
        self.collection = db.devices

    def insert_device(self, device_data):
        return self.collection.insert_one(device_data).inserted_id