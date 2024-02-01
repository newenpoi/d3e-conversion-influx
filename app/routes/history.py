# app/routes/history.py
from flask import Blueprint, jsonify
from app.services.import_service import find_history_imports

history_bp = Blueprint('history', __name__, url_prefix = '/history')

@history_bp.route('/', methods = ['GET'])
def get_history_data():
    # Appelle le service pour renvoyer la liste des imports.
    data = find_history_imports()

    # Renvoie un code 204 en cas d'absence de données.
    if not data: return '', 204

    return jsonify(data), 200