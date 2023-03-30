import dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.load_dotenv(os.path.join(BASE_DIR, '.env'))

# Configuration des variables d'environnement à partir du .env
class Config():
    DEBUG = os.environ.get("DEBUG")
    API_KEY = os.environ.get("API_KEY")
    PROJECT = os.environ.get("PROJECT")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    WTF_CSRF_ENABLE = os.environ.get("WTF_CSRF_ENABLE ")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    PLANTE_PER_PAGE = int(os.environ.get("PLANTE_PER_PAGE"))
    POEME_PER_PAGE = int(os.environ.get("POEME_PER_PAGE"))
    FLASK_ADMIN_SWATCH = 'yeti'