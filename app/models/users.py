from ..app import app, db
from werkzeug.security import generate_password_hash

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    pseudo = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    @staticmethod
    def create_user(pseudo, password):
        erreurs = []
        if not pseudo:
            erreurs.append("Le pseudo est vide")
        if not password or len(password) < 6:
            erreurs.append("Le mot de passe doit obligatoirement comporter plus de 6 caractères")
        
        unique = Users.query.filter(
            db.or_(Users.pseudo == pseudo)).count()
        if unique:
            erreurs.append("Le pseudo est déjà utilisé")
        
        if len(erreurs) > 0:
            return False, erreurs
        
        utilisateur = Users(pseudo=pseudo, password=generate_password_hash(password))

        try:
            db.session.add(utilisateur)
            db.session.commit()
            return True, utilisateur
        except Exception as erreur:
            return False, [str(erreur)]