from models.user import User
from dotenv import load_dotenv
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_limiter.util import get_remote_address

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Configuration de la clé secrète pour signer les tokens
SECRET_KEY = os.environ.get('Token')  # Remplacez par une clé secrète sécurisée dans un environnement réel

class UserController:
    def __init__(self):
        # Vous pouvez utiliser une liste (ou une autre structure de données) pour stocker les utilisateurs
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def delete_user(self, current_user, username_to_delete):
        # Vérifiez d'abord si l'utilisateur actuel a le droit de supprimer un autre utilisateur
        if current_user.admin:
            # Recherchez l'utilisateur à supprimer dans la liste
            user_to_delete = None
            for user in self.users:
                if user.username == username_to_delete:
                    user_to_delete = user
                    break

            if user_to_delete:
                # Supprimez l'utilisateur de la liste
                self.users.remove(user_to_delete)
                print(f"L'utilisateur {username_to_delete} a été supprimé.")
            else:
                print(f"L'utilisateur {username_to_delete} n'a pas été trouvé.")
        else:
            print("Vous n'êtes pas autorisé à supprimer un autre utilisateur.")

    def update_admin_status(self, current_user, username_to_update, is_admin):
        # Vérifiez si l'utilisateur actuel a le droit de mettre à jour le statut d'administrateur
        if current_user.admin:
            # Recherchez l'utilisateur dont le statut d'administrateur doit être mis à jour
            user_to_update = None
            for user in self.users:
                if user.username == username_to_update:
                    user_to_update = user
                    break

            if user_to_update:
                user_to_update.admin = is_admin
                print(f"Le statut administrateur de l'utilisateur {username_to_update} a été mis à jour.")
            else:
                print(f"L'utilisateur {username_to_update} n'a pas été trouvé.")
        else:
            print("Vous n'êtes pas autorisé à mettre à jour le statut d'administrateur.")

    def login(self, username, password):
        # Vérifiez les informations d'identification de l'utilisateur
        # Si l'utilisateur est valide, générez un token d'accès
        access_token = create_access_token(identity=username)
        return access_token

    @jwt_required()  # Protégez cette route avec l'authentification JWT
    @limiter.limit("2 per minute")  # Exemple de taux limites pour cette route
    def protected_route(self):
        current_user = get_jwt_identity()
        return f"Route protégée, utilisateur actuel : {current_user}"

# Créez une instance du contrôleur UserController
controller = UserController()

# Exemple d'utilisation du contrôleur User
user1 = User(username='john_doe', email='john@example.com', password='my_password', admin=False)
user2 = User(username='admin_user', email='admin@example.com', password='admin_password', admin=True)

controller.add_user(user1)
controller.add_user(user2)

# Exemple de suppression d'un utilisateur par l'administrateur
current_user = user2  # L'utilisateur actuel qui est administrateur (user2)
username_to_delete = 'john_doe'
controller.delete_user(current_user, username_to_delete)

# Exemple de mise à jour du statut administrateur par l'administrateur
username_to_update = 'john_doe'
is_admin = True
controller.update_admin_status(current_user, username_to_update, is_admin)
