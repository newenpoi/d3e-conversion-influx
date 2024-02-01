# app/routes/history.py
from flask import Blueprint, jsonify

reimport_bp = Blueprint('force_reimport', __name__, url_prefix = '/force-reimport')

@reimport_bp.route('/<string:csv_name>', methods = ['GET'])
def get_force_reimport(csv_name):
    # Données de test pour indiquer que la route fonctionne.
    data = {"message": f"Importation du fichier {csv_name} réalisée avec succès."}
    return jsonify(data), 200