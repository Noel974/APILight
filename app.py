import os
from flask import Flask, flash
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from routes.useroutes import users_bp # Importez le Blueprint depuis le sous-dossier routes

from flask_cors import CORS  # Importez Flask-CORS
from flask import Blueprint
from flask_jwt_extended import JWTManager  # Importez JWTManager
from flask_limiter.util import get_remote_address  # Importez get_remote_address

app = Flask(__name__)

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

mongo_uri = os.environ.get('MONGO_URI')

# Créez un nouveau client et connectez-vous au serveur
client = MongoClient(mongo_uri, server_api=ServerApi('1'))

# Envoyez un ping pour confirmer une connexion réussie
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# Activez CORS pour votre application Flask
CORS(app, origins=['http://localhost:3000', 'https://mondomaine.com'])  # Remplacez les domaines par ceux autorisés

# Enregistrez le Blueprint des utilisateurs dans l'application Flask

# Créez le Blueprint pour les routes des utilisateurs
app.register_blueprint(users_bp, url_prefix='/users')

# Initialisez le JWTManager
jwt = JWTManager(app)

# Initialisez le Limiter
limiter = Limiter(app, key_func=get_remote_address, default_limits=["5 per minute", "1 per second"])  # Exemple de taux limites