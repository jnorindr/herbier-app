from ..app import db

# Création de la classe associée à la table des illustrations "herbier"
class Herbier(db.Model):
    __tablename__ = "herbier"

    id = db.Column(db.String(5), primary_key=True)
    famille = db.Column(db.String(20))
    nom_commun1 = db.Column(db.String(50))
    nom_latin1 = db.Column(db.String(50))
    nom_commun2 = db.Column(db.String(50))
    nom_latin2 = db.Column(db.String(50))
    nom_commun3 = db.Column(db.String(50))
    nom_latin3 = db.Column(db.String(50))
    nom_commun4 = db.Column(db.String(50))
    nom_latin4 = db.Column(db.String(50))
    commentaire = db.Column(db.Text)
    id_poeme = db.Column(db.String(50))



# Création de la classe associée à la table poèmes
class Poemes(db.Model):
    __tablename__ = "poemes"


    id = db.Column(db.Text, primary_key=True)
    OCR = db.Column(db.Text)
    commentaire = db.Column(db.Text)
    id_plante = db.Column(db.String(50))
    titre = db.Column(db.String(20))



