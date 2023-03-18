import dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config():
    DEBUG = os.environ.get("DEBUG")
    API_KEY = os.environ.get("API_KEY")
    PROJECT = os.environ.get("PROJECT")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    ILLU_PER_PAGE = int(os.environ.get("ILLU_PER_PAGE"))
    WTF_CSRF_ENABLE = os.environ.get("WTF_CSRF_ENABLE ")
    SECRET_KEY = os.environ.get("SECRET_KEY")