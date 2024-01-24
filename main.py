'''
    Script pour transformer le fichier CSV en format compatible avec InfluxDB
'''

import pandas as pd
from datetime import datetime
import json

def convert_old(file_path: str):
    # Lecture des premières lignes pour obtenir les en-têtes et les métadonnées (ce qu'on appelle les dataframes df).
    metadata_df = pd.read_csv(file_path, nrows = 5)

    # Extraction des en-têtes et des métadonnées.
    sensor_names = metadata_df.iloc[0].tolist()
    units = metadata_df.iloc[1].tolist()
    data_types = metadata_df.iloc[2].tolist()
    periodicity = metadata_df.iloc[3].tolist()

    print(sensor_names)
    return

    # Lecture du fichier CSV en ignorant les 5 premières lignes.
    data_df = pd.read_csv(file_path, skiprows = 5)

    # Préparation des données pour InfluxDB.
    data = []

    for index, row in data_df.iterrows():
        # Extraction et formatage de la date et de l'heure (supposons que c'est le premier élément de chaque ligne).
        date_time_str = row.iloc[0]
        
        try:
            time = datetime.strptime(date_time_str, " %H:%M:%S  %d/%m/%Y").isoformat() + "Z"
        except ValueError:
            # Ignorer les lignes où la date et l'heure ne sont pas valides.
            print(f"Erreur lors du formatatge de la date à la ligne : {index}")
            continue

        # Traitement des valeurs de chaque capteur.
        for i in range(1, len(row)):
            print(f"Traitement de la valeur {i}...")

            measurement = sensor_names[i]
            value = row.iloc[i]

            print(f"Mesure : {measurement} - Valeur : {value}")
            
            # Création d'un tag à partir de l'unité et du type de données.
            tag = f"{units[i]}_{data_types[i]}" 
            
            data.append([measurement, tag, value, time])

    # Création d'un nouveau DataFrame.
    influxdb_df = pd.DataFrame(data, columns = ['measurement', 'tag', 'value', 'time'])

    # Sauvegarde du nouveau fichier CSV.
    output = 'influxdb.csv'
    influxdb_df.to_csv(output, index = False)

def convert(file_path: str):
    '''
        Réorganisation du DataFrame pour simplifier la structure de l'index et des en-têtes.
    '''

    # Ignorer les premières lignes qui ne sont pas des données et recharger le fichier CSV.
    csv_data = pd.read_csv(file_path, skiprows = 4)

    # Redéfinir les en-têtes de colonne
    column_headers = ["time"] + [f"sensor_{i}" for i in range(1, len(csv_data.columns))]
    csv_data.columns = column_headers

    # Extraire à nouveau les entêtes de chaque colonne (cette fois-ci, ce sont les noms des capteurs).
    headers = csv_data.columns.tolist()

    # Réinitialiser la structure JSON.
    json_data = []

    # Parcourir chaque ligne du fichier CSV.
    for index, row in csv_data.iterrows():
        # Extraire l'heure et la date.
        time = row["time"].strip()

        # Initialiser la liste des valeurs pour ce moment.
        values = []

        # Parcourir chaque mesure (capteur).
        for header in headers[1:]:  # Ignorer la première colonne 'time'.
            # Pour cet exemple, nous n'avons pas les détails exacts de chaque capteur, on les simplifie.
            value = row[header]
            values.append({
                "name": header,
                "unit": "unknown",  # L'unité est inconnue dans cet exemple
                "digital": 0,       # Supposons qu'il ne s'agit pas de valeurs numériques
                "sample_rate": "unknown",  # Le taux d'échantillonnage est inconnu
                "value": float(value) if not pd.isna(value) else None  # Gérer les valeurs NaN
            })

        # Ajouter cet instant temporel au JSON
        json_data.append({"time": time, "values": values})

    # Afficher un extrait du JSON pour vérification
    json_excerpt = json.dumps(json_data[:2], indent = 4)  # Afficher les 2 premiers enregistrements pour vérification
    print(json_excerpt)

# Amorce.
if __name__ == "__main__":
    # Considère la variable comme le chemin passé en argument pour ce script.
    path = "example.csv"
    print("Appel à la conversion du fichier CSV veuillez patienter...")
    convert(path)