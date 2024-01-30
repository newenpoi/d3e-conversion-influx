'''
    Ce fichier fourni des exemples de test.
    La méthode write_single() ajoute une nouvelle mesure (my_measure_04) dans le bucket.
    Le nom de l'équipement est fourni et sa valeur à un moment donné, ainsi que l'unité de mesure et le sample rate (interval des prises de mesures).
    Les chaînes sont toujours des tags d'après leur vidéo et les fields (champs) des données (int, bool, etc... sauf string).
'''

from dotenv import load_dotenv
from os import environ
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

# Données des variables d'environnement contenues dans le fichier .env qui est ignoré par notre git.
load_dotenv()

# Données de configuration d'influx DB.
url = environ["HOST"]
token = environ["TOKEN"]
org = environ["ORG"]
bucket = environ["BUCKET"]

client = InfluxDBClient(url = url, token = token, org = org)

def write_single():
    '''
        Rappel : En principe un data point dans InfluxDB se constituerai de cette manière :
        measurementName,equipmentId=<hash>,location=QUAI 2 EXPEDITION,unit=UnitType,measurementType=Type,isDigital=DigitalIndicator value=Value Timestamp
        ex :
        temperature,equipmentId=ff587999dc2fa5101,location=QUAI 2 EXPEDITION,unit=degC,isDigital=0 value=12.11 1671375600
        D'où l'importance de l'utentifiant unique.
    '''
    write_api = client.write_api(write_options = SYNCHRONOUS)

    timestamps = ["2023-12-18T16:00:00Z", "2023-12-18T16:01:00Z"]
    values = [12.11, 12.19]
    points = []

    test_now = datetime.now().today()
    print(test_now)

    for i in range(2):
        # Création d'un point unique.
        points.append(Point("TEMPERATURE_" + "03").tag("equipmentId", "ff587999dc2fa5101").tag("location", "QUAI 2 EXPEDITION").tag("unit", "degC").tag("isDigital", "0").tag("rate", "1").field("value", values[i]).time(timestamps[i]))
        
    # Écriture vers l'api.
    write_api.write(bucket = bucket, org = org, record = points)

def query():
    query_api = client.query_api()

    query = """from(bucket: "tiberian")
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "measurement1")"""
    
    tables = query_api.query(query, org = org)

    for table in tables:
        for record in table.records: print(record)

# Amorce.
if __name__ == "__main__":
    print("Test en cours vers InfluxDB encore quelques instants...")
    write_single()

    # Ferme le client.
    client.close()