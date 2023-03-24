from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField
from wtforms.validators import InputRequired

class InsertionPoeme(FlaskForm):
    """
    Une classe représentant le formulaire pour insérer une identification un commentaire sur un poème.

    Attributes
    ----------
    commentaire : wtforms.TextAreaField
        Champs de texte libre permettant à l'utilisateur d'ajouter un commentaire dans la table.
    """
    commentaire = TextAreaField("commentaire", validators=[])
     
class InsertionPlante(FlaskForm):
    """
    Une classe représentant le formulaire pour insérer une identification de plante et un commentaire dans la table herbier.

    Attributes
    ----------
    famille2 : wtforms.SelectField
        Champs permettant à l'utilisateur de sélectionner la famille botanique dans une liste prédéfinie.
    nom_commun4 : wtforms.fields.StringField
        Champs de texte libre correspondant à la quatrième colonne de noms communs de la planche botanique.
    nom_latin4 : wtforms.fields.StringField
        Champs de texte libre correspondant à la quatrième colonne de noms latins de la planche botanique.
    commentaire : wtforms.TextAreaField
        Champs de texte libre permettant à l'utilisateur d'ajouter un commentaire dans la table.
    """
    famille2 = SelectField("famille2", choices=[('', ''), ('Acanthaceae', 'Acanthaceae'), ('Apocynaceae', 'Apocynaceae'), ('Asteraceae', 'Asteraceae'), ('Cyperaceae', 'Cyperaceae'),
                                                ('Euphorbiaceae', 'Euphorbiaceae'), ('Fabaceae', 'Fabaceae'), ('Lamiaceae', 'Lamiaceae'), ('Malvaceae', 'Malvaceae'),
                                                ('Melastomataceae', 'Melastomataceae'), ('Myrtaceae', 'Myrtaceae'), ('Orchidaceae', 'Orchidaceae'), ('Poaceae', 'Poaceae'),
                                                ('Rosaceae', 'Rosaceae'), ('Rubiaceae', 'Rubiaceae')])
    nom_commun4 = StringField("nom_commun4", validators=[]) 
    nom_latin4 = StringField("nom_latin4", validators=[]) 
    commentaire = TextAreaField("commentaire", validators=[])

class CreationUtilisateur(FlaskForm):
    """
    Une classe représentant le formulaire pour insérer un utilisateur dans la table users.

    Attributes
    ----------
    pseudo : wtforms.fields.StringField
        Champs de texte libre correspondant au pseudonyme de l'utilisateur à insérer.
    password : wtforms.PasswordField
        Champs au texte masqué correspondant au mot de passe de l'utilisateur à insérer.
    """
    pseudo = StringField("prenom", validators=[])
    password = PasswordField("password", validators=[])

class Connexion(FlaskForm):
    """
    Une classe représentant le formulaire pour permettre à l'utilisateur de se connecter

    Attributes
    ----------
    pseudo : wtforms.fields.StringField
        Champs de texte libre correspondant au pseudonyme de l'utilisateur.
    password : wtforms.PasswordField
        Champs au texte masqué correspondant au mot de passe de l'utilisateur.
    """
    pseudo = StringField("pseudo", validators=[])
    password = PasswordField("password", validators=[])