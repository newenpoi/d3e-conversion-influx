'''
    Modèle brut pour un équipement.
    models/aksm/device.py
'''

from colorama import Fore

class Device():

    print(Fore.LIGHTCYAN_EX + f'Trouvé le modèle suivant : AKSM/{__name__}.')
    
    model = '''
        CREATE TABLE IF NOT EXISTS `Devices` (
        `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
        `hash` varchar(511) NOT NULL COMMENT "Identifiant unique de l'équipement.",
        `full_name` varchar(255) DEFAULT NULL COMMENT "Nom complet de l'équipement.",
        `name` varchar(255) NOT NULL DEFAULT "Inconnu" COMMENT "Nom court de l'équipement.",
        `location` varchar(255) NOT NULL DEFAULT "On ne sait pas où se trouve cet équipement, et on ne veut pas savoir." COMMENT "Lieu où se trouve l'équipement.",
        `unit` varchar(32) DEFAULT NULL COMMENT "Unité dans laquelle sera prise la mesure.",
        `digital` tinyint NOT NULL DEFAULT '0' COMMENT "Si c'est un appareil digital ou analogue.",
        `rate` tinyint NOT NULL DEFAULT '1' COMMENT "La fréquence des mesures.",
        `category` varchar(32) DEFAULT NULL COMMENT "La catégorie de l'équipement.",
        `threshold` float DEFAULT NULL COMMENT "Le seuil a ne pas dépasser pour cet équipement.",
        `comment` varchar(511) DEFAULT NULL COMMENT "Commentaire sur l'équipement.",
        `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT "Date à laquelle cet équipement a été enregistré.",

        UNIQUE KEY `Hash` (`hash`),
        PRIMARY KEY (`id`)
        ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
    '''

    def __init__(self):
        print("Merci de ne pas instancier cette classe.")