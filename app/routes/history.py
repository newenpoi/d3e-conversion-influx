# app/routes/history.py
from flask import Blueprint, jsonify
from app.services.imports_service import recuperer_historique_fichiers

'''
    Ce fichier représente une route serveur.
'''

history_bp = Blueprint('history', __name__, url_prefix = '/history')

@history_bp.route('/', methods = ['GET'])
def get_history_data():
    # Appelle le service pour renvoyer l'historique des imports.
    data = recuperer_historique_fichiers()

    # Renvoie un code 204 en cas d'absence de données.
    if not data: return '', 204

    return jsonify(data), 200