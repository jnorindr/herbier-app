import requests
import shutil
import os
from ..app import app

# Full documentation for this API can be found on Gallica's site : http://api.bnf.fr/api-iiif-de-recuperation-des-images-de-gallica

class IIIF(object):
    """
    Une classe représentant les images récupérées via l'API IIIF de Gallica.

    Attributes
    ----------
    url : str
        L'URL de requête à l'API IIIF.
    filename : str
        Chemin de l'image enregistrée sous forme de chaîne de caractère.
    dirname : os.path.dirname
        Répertoire contenant l'image enregistrée. Crée un répertoire pour les images provenant d'un même document si celui-ci n'existe pas.
    response : 
        Réponse de la requête à l'API IIIF.

    Returns
    -------
    filename
        Chemin sous forme de chaîne de caractère vers l'image enregistrée.
    """
    @staticmethod
    def iiif(id, region, size, rotation, quality, format):
        # URL de base pour les requêtes à l'API IIIF de Gallica
        IIIF_BASEURL = app.config['IIIF_BASEURL']

        # Constitution de l'URL complète à partir d'une liste de variables définies dans la route
        url = "".join([IIIF_BASEURL, id, '/', region, '/', size, '/', rotation, '/', quality, '.', format])
        # Constitution de la chaîne qui correspondra au chemin vers le fichier qui sera enregistré suite à la requête
        filename = "".join([id, '.', format])
        # Définition du répertoire contenant le fichier enregistré par la requête à partir de la variable précédente
        dirname = os.path.dirname(filename)
        # Si le répertoire n'existe pas, le créer
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        # Requête à l'API et stockage de la réponse dans la variable response
        response = requests.get(url, stream=True)
        # Récupération du fichier
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
            del response
        # Ajout d'un return filename pour renvoyer le chemin du fichier créé en prévision de l'identification
        return filename