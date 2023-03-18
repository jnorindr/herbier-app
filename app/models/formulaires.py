from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import Email, InputRequired
from ..models.database import Herbier

class InsertionPlante(FlaskForm):
    famille2 = SelectField("famille2", choices=[('', ''), ('Acanthaceae', 'Acanthaceae'), ('Apocynaceae', 'Apocynaceae'), ('Asteraceae', 'Asteraceae'), ('Cyperaceae', 'Cyperaceae'),
                                                ('Euphorbiaceae', 'Euphorbiaceae'), ('Fabaceae', 'Fabaceae'), ('Lamiaceae', 'Lamiaceae'), ('Malvaceae', 'Malvaceae'),
                                                ('Melastomataceae', 'Melastomataceae'), ('Myrtaceae', 'Myrtaceae'), ('Orchidaceae', 'Orchidaceae'), ('Poaceae', 'Poaceae'),
                                                ('Rosaceae', 'Rosaceae'), ('Rubiaceae', 'Rubiaceae')])
    nom_commun4 = StringField("nom_commun4", validators=[]) 
    nom_latin4 = StringField("nom_latin4", validators=[]) 
    commentaire = TextAreaField("commentaire", validators=[])