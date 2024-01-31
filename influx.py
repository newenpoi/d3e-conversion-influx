'''
    Script pour l'import du fichier json vers InfluxDB.
    Les données json correspondent en gros à des points contenant leurs données qu'on envoi vers le moteur.
'''

import json

from dotenv import load_dotenv
from os import environ

from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

# Données des variables d'environnement contenues dans le fichier .env qui est ignoré par notre git.
load_dotenv()

# Données de configuration d'influx DB.
url = environ["HOST"]
token = environ["TOKEN"]
org = environ["ORG"]
bucket = environ["BUCKET"]

def convert(test = True):
    '''
        On doit convertir les données json en line protocol pour les rendre compatibles avec influx db.
        InfluxDB s'occupe de cette conversion à partir du moment où on lui fourni les points avec l'objet Point (suivi de field value).
        Voir la documentation si nécessaire à l'adresse suivante :
        https://www.influxdata.com/blog/import-json-data-influxdb-using-python-go-javascript-client-libraries/
    '''

    # Initialisation du client InfluxDB.
    client = InfluxDBClient(url = url, token = token, org = org)
    write_api = client.write_api(write_options = SYNCHRONOUS)
    
    # Charger les données json.
    with open('output.json', 'r') as file: data = json.load(file)

    # Pour chaque enregistrement.
    for record in data:
        # Ces données sont fixes et ne changent pas pour un équipement.
        equipment_id = record["equipmentId"]
        location = record["location"]
        device = record["device"]
        unit = record["unit"]
        digital = record["digital"]
        rate = record["rate"]
        
        # Pour chaque mesure d'un équipement.
        for measurement in record["measurements"]:
            # Création d'un point pour chaque mesure.
            point = Point("mesure")
            
            # Les tags (toujours des chaines, seront indexées).
            point.tag("equipmentId", equipment_id)
            point.tag("location", location)
            point.tag("device", device)
            
            # Les champs (peuvent être différents types de données).
            point.field("value", measurement["value"])
            point.field("unit", unit)
            point.field("digital", digital)
            point.field("rate", rate)
            
            # Le point dans le temps.
            point.time(measurement["time"])
            
            if not test: write_api.write(bucket = bucket, org = org, record = point)
            else: print(point.to_line_protocol())

    # Fermeture du client.
    client.close()

# Amorce.
if __name__ == "__main__":
    print("Importation en cours vers InfluxDB encore quelques instants...")
    convert(test = False)