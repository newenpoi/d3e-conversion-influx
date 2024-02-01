# app/models/device.py

class Device:
    def __init__(self, equipmentId, location, device, date, measurements, unit, digital, rate):
        self.equipmentId = equipmentId
        self.location = location
        self.device = device
        self.date = date
        self.measurements = measurements
        self.unit = unit
        self.digital = digital
        self.rate = rate

    # Method to save instance to MongoDB
    def save(self, db):
        db.devices.insert_one(self.to_dict())

    # Convert instance to dictionary suitable for MongoDB
    def to_dict(self):
        return {
            "equipmentId": self.equipmentId,
            "location": self.location,
            "device": self.device,
            "date": self.date,
            "measurements": self.measurements,
            "unit": self.unit,
            "digital": self.digital,
            "rate": self.rate
        }