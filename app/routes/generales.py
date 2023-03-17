from ..app import app, db
from flask import Flask, render_template
from ..models.iiif_api import IIIF
from ..models.database import Herbier
import json, requests

# Route pour les pages individuelles des illustations de  plantes
@app.route("/herbier/<string:folio>", methods=["POST", "GET"])

# Définition de la fonction permettant d'identifier la plante et d'ajouter ces données à la base
def identification(folio):
    # Import depuis le fichier config.py de la clé d'API et du continent de travail
    API_KEY = app.config['API_KEY']
    PROJECT = app.config['PROJECT']

    # Création de l'URL pour la requête à l'API
    api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

    # Utilisation du wrapper PyGallica pour récupérer l'image, l'enregistrer et récupérer son chemin
    # Utilisation de la variable folio pour construire l'URL pour chaque illustration
    image = IIIF.iiif('3A%2F12148%2Fbtv1b8451620k/'+folio, 'full', 'full', '0', 'native', 'jpg')

    # Lecture en binaire de l'image enregistrée précédemment
    image_data = open(image, 'rb')

    # Création du dictionnaire des organes des plante sur les images (systématiquement des fleurs dans notre cas)
    data = {
        'organs': ['flower']
    }

    # Création d'une liste de tuples correspondants à l'image et son chemin pour la requête
    files = [
        ('images', (image, image_data))
    ]

    # Requête à l'API PlantNet pour l'identification à partir des fichiers image, du dictionnaire d'organes et de l'URL définis précédemment
    req = requests.Request('POST', url=api_endpoint, files=files, data=data)

    # Mise en forme de la réponse de l'API au format JSON
    prepared = req.prepare()
    s = requests.Session()
    response = s.send(prepared)
    ident = json.loads(response.text)

    # AJOUTER CONDITION : SI PREMIÈRE FOIS
    # Import des valeurs qui nous intéressent dans la base de données herbier à partir de la réponse en JSON de l'API
    Herbier.query.filter(Herbier.id == folio).\
        update({"famille": ident['results'][0]['species']['family']['scientificNameWithoutAuthor'],
                "nom_commun1": ', '.join(ident['results'][0]['species']['commonNames']),
                "nom_latin1": ident['results'][0]['species']['scientificNameWithoutAuthor'],
                "nom_latin2": ident['results'][1]['species']['scientificNameWithoutAuthor'],
                "nom_commun2": ', '.join(ident['results'][1]['species']['commonNames']),
                "nom_commun3": ', '.join(ident['results'][2]['species']['commonNames']),
                "nom_latin3": ident['results'][2]['species']['scientificNameWithoutAuthor']})
    db.session.commit()

    # Requête pour les données de l'illustration dont l'identifiant dans la base est équivalent au folio
    donnees = Herbier.query.filter(Herbier.id == folio).first()

    return render_template("/pages/info_plante.html", donnees=donnees, folio=folio)