# app/routes/devices.py
from flask import Blueprint, jsonify

devices_bp = Blueprint('devices', __name__, url_prefix = '/last-import')

@devices_bp.route('/', methods = ['GET'])
def get_devices(company: None):
    '''
        Récupère la liste des derniers capteurs importés.
    '''
    # Données de test pour indiquer que la route fonctionne.
    data = {"message": f"Renvoie des derniers capteurs importés pour la société {company}."}

    # Renvoie un code 204 en cas d'absence de données.
    if not data: return '', 204

    return jsonify(data), 200