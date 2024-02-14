# app/routes/history.py
import os
import uuid
from pathlib import Path
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.utils.csv_to_json import convert
from app.utils.influx import transmute

reimport_bp = Blueprint('reimport', __name__, url_prefix = '/imports')

@reimport_bp.route('/force-reimport', methods = ['POST'])
@cross_origin()
def get_reimport():
    # Extraction du fichier.
    file = request.files['source']

    # Chemin ./app
    root = Path(__file__).parent.parent
    destination = root / f'uploads/{file.filename}'
    
    if file:
        # Création d'un identifiant unique pour le nom de fichier.
        unique_filename = uuid.uuid4()

        # Sauvegarde dans le répertoire storage (qui est surveillé par le watch dog).
        file.save(destination)

        # Converti le fichier nouvellement uploadé.
        data = convert(destination)

        # Envoi les données vers influx db.
        transmute(data, test = True)

        # Renvoie la réponse au client.
        return jsonify({'message': 'Le fichier a été tranféré avec succès.', 'uid': unique_filename}), 201
    
    return jsonify({'message': "Une erreur est survenue."}), 400