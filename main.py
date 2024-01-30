'''
    Script pour transformer le fichier csv en format compatible avec InfluxDB (JSON).
    Plutôt que de s'enquiquiner à recréer un csv on peut produire du json et ainsi augmenter la portabilité des données.
    Le script ci-dessous va lire le csv et en extraire les informations nécessaires pour les formater correctement.
    En sortie on obtient un fichier json (output.json).

    Remarque :
    Tester avec le fichier csv au complet et observer les valeurs `missing`.
'''

import colorama
import pandas as pd
from zoneinfo import ZoneInfo
from datetime import datetime
from colorama import Fore
import json
import re
import hashlib

# Initialize colorama.
colorama.init(autoreset = True)

def convert(file_path: str):
    # Affiche un petit message d'information.
    print(Fore.YELLOW + "Conversion vers le format JSON en cours veuillez patienter...")

    # La fusée horaire (le fuseau pardon).
    paris_timezone = ZoneInfo("Europe/Paris")
    
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
        
        # On sait que la première valeur est notre timestamp qu'on met au propre puis on formate.
        local_time_str = re.sub(' +', ' ', row[0]).strip()
        local_datetime = datetime.strptime(local_time_str, "%H:%M:%S %d/%m/%Y")

        local_datetime = local_datetime.replace(tzinfo = paris_timezone)
        
        # Les mesures après la première valeur.
        measurements = row[1:]
        
        # On utilise la fonction d'énumération (après avoir cast en str on récupère la valeur numérique pour la périodicité (sample rate)).
        for j, instrument in enumerate(instruments):

            # Le nom a des espaces blancs en trop on va arranger ça proprement.
            instrument = re.sub(' +', ' ', instrument).upper()

            # /!\ Une conversion est nécessaire pour les valeurs numériques afin d'éviter l'erreur `unsupported input type for mean aggregate: string`.
            # En Python, None = Null.
            # Le hash est sur le lieu et le nom de l'équipement, ce qui nous donne un identifiant unique dont on retrouve des valeurs chaque minutes.
            entry = {
                "equipmentId": hashlib.sha256(instrument.encode()).hexdigest(),
                "location": re.split(":", instrument)[0],
                "device": re.split(":", instrument)[1][1:], # On enlève l'espace de trop en bougeant le curseur.
                "updated": local_datetime.astimezone(ZoneInfo("UTC")).isoformat().replace('+00:00', 'Z'),
                "unit": units[j] if not pd.isna(units[j]) else None,
                "digital": float(digital_analog[j]) if not pd.isna(digital_analog[j]) else None,
                "rate": float(str(sample_rates[j]).split(' ')[0]) if not pd.isna(sample_rates[j]) else None,
                "value": float(measurements[j]) if not pd.isna(measurements[j]) else None
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
    
    # Procède à la conversion.
    data = convert(path)

    # Sauvegarde le fichier sur le disque.
    save(data, "output.json")

    print(Fore.GREEN + "Conversion terminée.")