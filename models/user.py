from app import db

class User:
    def __init__(self, username, password, token, is_admin=False):
        self.username = username
        self.password = password
        self.token = token
        self.is_admin = is_admin

    def save(self):
        db.users.insert_one({
            'username': self.username,
            'password': self.password,
            'token': self.token,
            'is_admin': self.is_admin
        })

    @staticmethod
    def find_by_username(username):
        return db.users.find_one({'username': username})

    # Vous pouvez ajouter d'autres méthodes pour gérer les utilisateurs (par exemple, trouver par token, mettre à jour, supprimer, etc.)
