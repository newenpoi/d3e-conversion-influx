'''
    Permet de structure les données de sorte à obtenir 18 000 lignes par an et non 30 000 000.
    Et ce pour 50 appareils environ.

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
    
    # Données qui déterminent si le capteur est digital ou analogue.
    digital_analog = csv_data.iloc[3, 1:].values
    
    # Fréquence des mesures.
    sample_rates = csv_data.iloc[4, 1:].values

    data = {}
    
    for i in range(5, len(csv_data)):
        
        row = csv_data.iloc[i, :].values
        
        # On sait que la première valeur est notre timestamp qu'on met au propre en le formattant et le transformant en ts conscient de son fuseau.
        local_time_str = re.sub(' +', ' ', row[0]).strip()
        local_datetime = datetime.strptime(local_time_str, "%H:%M:%S %d/%m/%Y").replace(tzinfo = paris_timezone)
        
        # Les mesures après la première valeur.
        measurements = row[1:]

        for j, instrument in enumerate(instruments):
            # Le nom a des espaces blancs en trop on va arranger ça proprement.
            instrument = re.sub(' +', ' ', instrument).upper()
            
            # Le hash est sur le lieu et le nom de l'équipement, ce qui nous donne un identifiant unique utile pour notre dictionnaire.
            id = hashlib.sha256(instrument.encode()).hexdigest()
            
            # On sépare le lieu et l'appareil en enlevant également l'espace de trop du nom (device) en bougeant le curseur.
            location, device = re.split(":", instrument)[0], re.split(":", instrument)[1][1:]
            
            # Servira pour notre champ date « parent » désormais séparé des heures.
            date_str = local_datetime.strftime("%Y-%m-%d")

            # Ajoute cette entrée au dictionnaire si elle n'existe pas encore.
            if id not in data:
                data[id] = {
                    "equipmentId": id,
                    "location": location,
                    "device": device,
                    "date": date_str,
                    "measurements": [],
                    "unit": units[j] if not pd.isna(units[j]) else None,
                    "digital": float(digital_analog[j]) if not pd.isna(digital_analog[j]) else None,
                    "rate": float(str(sample_rates[j]).split(' ')[0]) if not pd.isna(sample_rates[j]) else None
                }
            
            # Nouvelle entrée (les données sont filtrées si elles n'existent pas dans le csv).
            measurement_entry = {
                "time": local_datetime.astimezone(ZoneInfo("UTC")).isoformat().replace('+00:00', 'Z'),
                "value": float(measurements[j]) if not pd.isna(measurements[j]) else None
            }

            data[id]["measurements"].append(measurement_entry)

    # Transforme les valeurs sous forme de liste.
    output = list(data.values())
    
    # Sérialisation vers un objet json formatté.
    return json.dumps(output, indent = 4)

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