from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from .config import Config

app = Flask(
    __name__, 
    template_folder='templates',
    static_folder='statics')
app.config.from_object(Config)

# Création d'une instance de la classe SQLAlchemy à partir de l'application
db = SQLAlchemy(app)

# Création d'une instance de la classe LoginManager à partir de l'application
login = LoginManager(app)

# Import des modèles nécessaires à la création d'une interface administrateur
from .models.admin import MyModelView
from .models.users import Users
from .models.database import Herbier, Poemes

# Ajout de nos modèles dans l'interface pour une gestion graphique
admin = Admin(app, name='Le poète à la main verte', template_mode='bootstrap3', endpoint="admin")
admin.add_view(MyModelView(Users, db.session))
admin.add_view(MyModelView(Herbier, db.session))
admin.add_view(MyModelView(Poemes, db.session))

# Import des routes
from .routes import generales, insertions, suppressions, users, erreurs