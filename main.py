'''
    Script pour transformer le fichier CSV en format compatible avec InfluxDB (JSON).
'''

import pandas as pd
from datetime import datetime
import json

def convert(file_path: str):
    # Charge le fichier csv et ignore les headers, on utilise le séparateur point virgule.
    csv_data = pd.read_csv(file_path, header = None, sep = ';')
    
     # Le nom des instruments.
    instruments = csv_data.iloc[1, 1:].values

    # Unités à parir de la ligne 3 (on compte à partir de zéro) et deuxième entrée (toujours à partir de zéro).
    units = csv_data.iloc[2, 1:].values
    
    # Données s'il s'agit d'un instrument digital ou analogue.
    digital_analog = csv_data.iloc[3, 1:].values  # Digital or Analog
   
    # Les fréquences.
    sample_rates = csv_data.iloc[4, 1:].values  # Sample rates

    # On initialise une liste vide.
    data = []

    # On procède chaque données du csv en commençant par la ligne 6.
    for i in range(5, len(csv_data)):
        row = csv_data.iloc[i, :].values
        
        # On sait que la première valeur est un timestamp (date heure) qu'on formatte.
        timestamp = datetime.strptime(row[0], " %H:%M:%S  %d/%m/%Y").isoformat()
        
        # Les mesures après la première valeur.
        measurements = row[1:]
        
        # On utilise la fonction d'énumération (après avoir cast en str on récupère la valeur numérique pour la périodicité (sample rate)).
        for j, instrument in enumerate(instruments):
            
            entry = {
                "name": instrument,
                "updated": timestamp,
                "unit": units[j] if not pd.isna(units[j]) else None,
                "digital": digital_analog[j] if not pd.isna(digital_analog[j]) else None,
                "rate": str(sample_rates[j]).split(' ')[0] if not pd.isna(sample_rates[j]) else None,
                "value": measurements[j] if not pd.isna(measurements[j]) else None
            }

            data.append(entry)

    return json.dumps(data, indent = 4)

def save(json_data, output_file_path):
    with open(output_file_path, 'w') as file:
        file.write(json_data)

# Amorce.
if __name__ == "__main__":
    # Considère la variable comme le chemin passé en argument pour ce script.
    path = "example.csv"
    print("Appel à la conversion du fichier CSV veuillez patienter...")
    
    # Procède à la conversion.
    data = convert(path)
    print(data)

    # Sauvegarde le fichier sur le disque.
    # save(data, "output.json")