# app/routes/history.py
import uuid
from pathlib import Path
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.services import historique_service, device_service
from app.utils.csv_to_json import convert
from app.utils.influx import transmute

reimport_bp = Blueprint('reimport', __name__, url_prefix = '/imports')

@reimport_bp.route('/force-reimport', methods = ['POST'])
@cross_origin()
def get_reimport():
    # Extraction du fichier.
    file = request.files['source']
    comment = request.form['comment']

    # Chemin ./app
    root = Path(__file__).parent.parent
    destination = root / f'uploads/{file.filename}'

    # TODO : Vérifier extension server-side.
    
    if file:
        # Création d'un identifiant unique pour le nom de fichier.
        unique_filename = uuid.uuid4()

        # Sauvegarde dans le répertoire uploads (et non dans celui surveillé par le watch dog).
        file.save(destination)

        # Converti le fichier nouvellement uploadé en dictionnaire.
        # TODO : Extraire début, fin des relevés, nombre missing.
        data = convert(destination)

        # Envoi les données vers influx db (peut prendre un certain temps).
        transmute(data)

        # Si tout se passe bien, on appelle le service pour ajouter une trace de cet import en base de données.
        historique_service.ajouter_trace(file.filename, comment = comment)

        # Et on ajoute les nouveaux capteurs en base de données sql aussi, les doublons auront certains champs mis à jour.
        device_service.ajouter_appareils(data)

        # Renvoie la réponse au client.
        return jsonify({'message': 'Le fichier a été tranféré avec succès.', 'uid': unique_filename}), 201
    
    # Dans le cas où on a pas de fichier propre.
    return jsonify({'message': "Une erreur est survenue."}), 400