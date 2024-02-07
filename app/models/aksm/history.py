'''
    Modèle brut pour un historique.
    models/aksm/history.py
'''
from colorama import Fore

class History():

    print(Fore.LIGHTCYAN_EX +  f'Trouvé le modèle suivant : AKSM/{__name__}.')
    
    model = '''
        CREATE TABLE IF NOT EXISTS `History` (
        `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
        `date_imported` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT "Date d'importation.",
        `reading_start` datetime COMMENT "Début des mesures.",
        `reading_end` datetime COMMENT "Fin des mesures.",
        `nb_missing` int NOT NULL DEFAULT '0' COMMENT "Nombre de valeurs manquantes.",
        `status` int NOT NULL DEFAULT '0' COMMENT "Etat dans lequel se trouve l'importation ?",

        PRIMARY KEY (`id`)
        ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
    '''

    def __init__(self):
        print("Merci de ne pas instancier cette classe.")