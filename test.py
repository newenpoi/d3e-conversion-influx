'''
    Ce fichier fourni des exemples de test.
    La méthode write_single() ajoute une nouvelle mesure (my_measure_04) dans le bucket.
    Le nom de l'équipement est fourni et sa valeur à un moment donné, ainsi que l'unité de mesure et le sample rate (interval des prises de mesures).
    Les chaînes sont toujours des tags d'après leur vidéo et les fields (champs) des données (int, bool, etc... sauf string).
'''

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

client = InfluxDBClient(url = url, token = token, org = org)

def write_single():
    write_api = client.write_api(write_options = SYNCHRONOUS)

    # Création d'un point unique.
    point_one = (Point("my_measure_04").tag("name", "QUAI 2 EXPEDITION: U17 THER AIR").tag("unit", "degc").field("valeur", 12.11).field("rate", 1).time("2023-12-18T17:00:00Z"))
    point_two = (Point("my_measure_04").tag("name", "QUAI 2 EXPEDITION: U17 THER AIR").tag("unit", "degc").field("valeur", 12.39).field("rate", 1).time("2023-12-18T17:00:01Z"))
    
    # Écriture vers l'api.
    write_api.write(bucket = bucket, org = org, record = [point_one, point_two])

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