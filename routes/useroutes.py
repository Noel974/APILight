from flask import Blueprint, request
from models.user import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/create_user', methods=['POST'])
def create_user():
    # Récupérer les informations de l'utilisateur à partir d'une requête POST
    username = request.form['username']
    password = request.form['password']
    token = generate_token()  # Assurez-vous de créer une fonction pour générer le token

    # Créer un nouvel objet User
    new_user = User(username=username, password=password, token=token)

    # Enregistrer l'utilisateur dans la base de données MongoDB
    new_user.save()

    return "Utilisateur créé avec succès !"
from flask import Blueprint, request
from models.user import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os

users_bp = Blueprint('users', __name__)

# Configuration de la clé secrète pour signer les tokens
SECRET_KEY = os.environ.get('Token')  # Remplacez par une clé secrète sécurisée dans un environnement réel

# Créez une fonction pour générer un token pour un utilisateur donné
def generate_token(user_id):
    s = Serializer(SECRET_KEY, expires_in=3600)  # Le token expirera après 1 heure (3600 secondes)
    token = s.dumps({'user_id': user_id}).decode('utf-8')
    return token

@users_bp.route('/create_user', methods=['POST'])
def create_user():
    # Récupérer les informations de l'utilisateur à partir d'une requête POST
    username = request.form['username']
    password = request.form['password']
    token = generate_token(user_id)  # Assurez-vous d'avoir l'ID de l'utilisateur pour générer le token

    # Créer un nouvel objet User
    new_user = User(username=username, password=password, token=token)

    # Enregistrer l'utilisateur dans la base de données MongoDB
    new_user.save()

    return "Utilisateur créé avec succès !"
