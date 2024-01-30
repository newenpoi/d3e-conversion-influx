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

    # Écriture des données.
    for record in data:
        
        # Le nom de la mesure.
        point = Point("TEST" + "04")

        for key, value in record.items():
            # Si la clé parcourue est lieu ou device (nom de l'appareil) on s'en sert de tag afin de l'indéxer.
            # Remarque, les valeurs ne sont pas indexées.
            if key in ["location", "device"]: point.tag(key, value)
            elif key != 'updated': point.field(key, value)

        point.time(record['updated'])
        
        if not test: write_api.write(bucket = bucket, org = org, record = point)
        else: print(point)

    # Close the client
    client.close()

# Amorce.
if __name__ == "__main__":
    print("Importation en cours vers InfluxDB encore quelques instants...")
    convert(test = False)