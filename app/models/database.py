from ..app import db

class Herbier(db.Model):
    """
    Une classe représentant les planches botaniques de l'ouvrage

    Attributes
    ----------
    id : sqlalchemy.sql.schema.Column
        Identifiant de la planche correspondant au numéro de la vue dans Gallica. C'est la clé primaire. Cet attribut est une Column SQLALchemy.
    famille : sqlalchemy.sql.schema.Column
        Famille de la plante identifiée. Deux colonnes pour permettre plusieurs identifications.
    nom_commun : sqlalchemy.sql.schema.Column
        Noms communs des plantes identifiées. Quatre colonnes pour permettre plusieurs identifications.
    nom_latin : sqlalchemy.sql.schema.Column
        Noms latins des plantes identifiées. Quatre colonnes pour permettre plusieurs identifications.
    commentaire : sqlalchemy.sql.schema.Column
        Commentaire ajouté par l'utilisateur à la planche.
    """
    __tablename__ = "herbier"

    id = db.Column(db.String(5), primary_key=True) # Clé primaire
    famille = db.Column(db.String(20))
    famille2 = db.Column(db.String(20))
    nom_commun1 = db.Column(db.String(50))
    nom_latin1 = db.Column(db.String(50))
    nom_commun2 = db.Column(db.String(50))
    nom_latin2 = db.Column(db.String(50))
    nom_commun3 = db.Column(db.String(50))
    nom_latin3 = db.Column(db.String(50))
    nom_commun4 = db.Column(db.String(50))
    nom_latin4 = db.Column(db.String(50))
    commentaire = db.Column(db.Text)

    # Propriétés de relation avec la table des poèmes
    poems = db.relationship('Poemes',  backref='poemes',  cascade="all, delete", lazy=True)

class Poemes(db.Model):
    """
    Une classe représentant les pages de poèmes de l'ouvrage

    Attributes
    ----------
    id : sqlalchemy.sql.schema.Column
        Identifiant de la page correspondant au numéro de la vue dans Gallica. C'est la clé primaire. Cet attribut est une Column SQLALchemy.
    ocr : sqlalchemy.sql.schema.Column
        Texte du poème transcrit avec eScriptorium.
    commentaire : sqlalchemy.sql.schema.Column
        Commentaire ajouté par l'utilisateur à la planche.
    id_plante : sqlalchemy.sql.schema.Column
        Identifiant de la planche botanique associée à la page de poème. Il s'agit d'une clé secondaire.
    titre : sqlalchemy.sql.schema.Column
        Titre du poème dont la page fait partie.
    """
    __tablename__ = "poemes"

    id = db.Column(db.String(5), primary_key=True) # Clé primaire
    ocr = db.Column(db.Text)
    commentaire = db.Column(db.Text)
    id_plante = db.Column(db.String(5), db.ForeignKey('herbier.id')) # Clé étrangère : id issus de la table herbier
    titre = db.Column(db.String(50))
