# app/__init__.py
import os
from flask import Flask
from config import DevelopmentConfig, ProductionConfig

def create_app():
    app = Flask(__name__)

    if os.getenv('FLASK_ENV') == 'production': app.config.from_object(ProductionConfig)
    else: app.config.from_object(DevelopmentConfig)
    
    # Importation des routes.
    from .routes.history import history_bp
    from .routes.force_reimport import reimport_bp
    from .routes.devices import devices_bp
    
    # Enregistre les routes spécifiques au serveur.
    app.register_blueprint(history_bp)
    app.register_blueprint(reimport_bp)
    app.register_blueprint(devices_bp)
    
    return app