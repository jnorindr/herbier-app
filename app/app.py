from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

app = Flask(
    __name__, 
    template_folder='templates',
    static_folder='statics')
app.config.from_object(Config)

# Définition de la base de données dans la variable db
db = SQLAlchemy(app)

# Import des routes
from .routes import generales, insertions, users, erreurs