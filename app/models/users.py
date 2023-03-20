from ..app import app, db
from werkzeug.security import generate_password_hash

class Users(db.Model):
    """
    Une classe représentant la table users qui contient les informations des utilisateurs.

    Attributes
    ----------
    id : sqlalchemy.sql.schema.Column
        Identifiant de l'utilisateur. C'est la clé primaire. Cet attribut est une Column SQLALchemy.
    pseudo : sqlalchemy.sql.schema.Column
        Pseudonyme de l'utilisateur.
    password : sqlalchemy.sql.schema.Column
        Mot de passé hashé de l'utilisateur.

    Methods
    -------
    create_user(pseudo, password)
        Permet l'insertion d'un utilisateur dans la table avec un pseudonyme et un mot de passe hashé choisis par l'utilisateur.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    pseudo = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    @staticmethod
    def create_user(pseudo, password):
        # Création d'une variable erreurs correspondant à une liste vide
        erreurs = []
        # L'utilisateur doit obligatoirement saisir un pseudo et un mot de passe de plus de 6 caractères, sinon un message d'erreur est ajouter à la liste erreurs
        if not pseudo:
            erreurs.append("Le pseudo est vide")
        if not password or len(password) < 6:
            erreurs.append("Le mot de passe doit obligatoirement comporter plus de 6 caractères")
        
        # Requête à la table users pour compter le nombre d'occurences du pseudo et vérifier son unicité, sinon ajout du message d'erreur à la liste erreurs
        unique = Users.query.filter(
            db.or_(Users.pseudo == pseudo)).count()
        if unique:
            erreurs.append("Le pseudo est déjà utilisé")
        
        # S'il y a plus de 0 erreurs, retourner les erreurs et ne pas insérer l'utilisateur dans la table
        if len(erreurs) > 0:
            return False, erreurs
        
        # Création d'une instance de la classe Users ayant pour pseudo le pseudo et pour mot de passe le mot de passe hashé
        utilisateur = Users(pseudo=pseudo, password=generate_password_hash(password))

        # Insertion dans la table de utilisateur
        try:
            db.session.add(utilisateur)
            db.session.commit()
            return True, utilisateur
        # Si l'insertion échoue, retourner les erreurs
        except Exception as erreur:
            return False, [str(erreur)]