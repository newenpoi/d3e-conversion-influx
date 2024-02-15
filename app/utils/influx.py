'''
    Script pour l'import du fichier json vers InfluxDB.
    Les données json correspondent en gros à des points contenant leurs données qu'on envoi vers le moteur.
'''

import json
import time
import os

import pandas as pd

from dotenv import load_dotenv
from colorama import Fore

from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

# Données des variables d'environnement contenues dans le fichier .env qui est ignoré par notre git.
load_dotenv()

# Données de configuration d'influx DB.
url = os.getenv("HOST")
token = os.getenv("TOKEN")
org = os.getenv("ORG")
bucket = os.getenv("BUCKET")

def transmute(data: dict, test = False):
    '''
        On doit convertir les données json en line protocol pour les rendre compatibles avec influx db.
        InfluxDB s'occupe de cette conversion à partir du moment où on lui fourni les points avec l'objet Point (suivi de field value).
        Voir la documentation si nécessaire à l'adresse suivante :
        https://www.influxdata.com/blog/import-json-data-influxdb-using-python-go-javascript-client-libraries/
    '''

    print(Fore.LIGHTYELLOW_EX + "Importation vers InfluxDB en cours...")

    # Initialisation du client InfluxDB.
    client = InfluxDBClient(url = url, token = token, org = org)
    
    # Charger les données json.
    # with open(file_name, 'r') as file: data = json.load(file)

    # Timer start.
    start_time = time.time()
    total = 0

    with client.write_api(write_options = WriteOptions(batch_size = 10_000)) as write_api:
        # Pour chaque enregistrement.
        for record in data:
            # Compteur de points.
            counter = 0
            
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
                point = Point(device)
                
                # Les tags (toujours des chaines, seront indexées).
                point.tag("equipmentId", equipment_id)
                point.tag("location", location)
                
                # Les champs (peuvent être différents types de données).
                point.field("value", measurement["value"])
                
                # Le point dans le temps.
                point.time(measurement["time"])
                
                if not test: write_api.write(bucket = bucket, org = org, record = point)
                counter = counter + 1

            # Pour déboggage.
            # datetime_obj = pd.to_datetime(measurement["time"])
            # formatted_datetime = datetime_obj.strftime("%d/%m/%Y %H:%M:%S")

            total = total + counter
            print(Fore.LIGHTGREEN_EX + f"Ajout de {counter} mesures pour l'équipement {device}.")
        
        end_time = time.time()
        print(Fore.GREEN + f"{total} nouveaux points ont été ajoutés au bucket.")
        print(Fore.LIGHTMAGENTA_EX + f"Temps de traitement du dictionnaire vers influx environ {round(end_time - start_time, 2)} secondes.")