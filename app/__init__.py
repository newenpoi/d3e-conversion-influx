# app/__init__.py
import os
from flask import Flask
from app.models import setup
from config import DevelopmentConfig, ProductionConfig

def create_app():
    app = Flask(__name__)

    # Récupère la configuration de développement ou de production selon l'environnement (FLASK_ENV) spécifié.
    if os.getenv('FLASK_ENV') == 'production': app.config.from_object(ProductionConfig)
    else: app.config.from_object(DevelopmentConfig)

    # Création des schéma sql.
    setup()
    
    # Importation des routes.
    from .routes.history import history_bp
    from .routes.force_reimport import reimport_bp
    
    # Enregistre les routes spécifiques au serveur.
    app.register_blueprint(history_bp)
    app.register_blueprint(reimport_bp)
    
    return app