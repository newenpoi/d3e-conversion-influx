# app/routes/history.py
import hashlib
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.services.device_service import recuperer_appareils, ajouter_appareil

'''
    Ce fichier représente une route serveur.
    TODO : Gestion des exceptions.
'''

devices_bp = Blueprint('devices', __name__, url_prefix = '/devices')

@devices_bp.route('/', methods = ['GET'])
@cross_origin()
def get_devices():
    # Appelle le service pour renvoyer les appareils.
    data = recuperer_appareils()

    # Renvoie un code 204 en cas d'absence de données.
    if not data: return '', 204

    return jsonify(data), 200

@devices_bp.route('/add', methods = ['POST'])
@cross_origin()
def ajouter_device():
    capteur = request.get_json()

    # On doit s'assurer qu'il y a bien quelque chose dans le corps de la requête (comme le nom).
    if not capteur or 'name' not in capteur: return jsonify(capteur), 400

    # On créé le hash, c'est obligatoire dans notre schéma (on join le lieu et le nom séparé par un espace avant d'encoder et de hasher).
    capteur['hash'] = hashlib.sha256(' '.join([capteur['location'], capteur['name']]).encode()).hexdigest()

    # Appelle le service pour ajouter le capteur (data correspond au modèle device).
    ajouter_appareil(capteur)

    # Renvoie un statut code (créé) et le capteur ajouté (il faudrait avoir un callback côté service car là on reprend ce qui a été envoyé).
    return jsonify(capteur), 201

# TODO : Route pour uploader le fichier.