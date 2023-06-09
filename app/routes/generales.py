from ..app import app, db
from flask import render_template, abort, request
from sqlalchemy import or_
from flask_weasyprint import HTML, render_pdf
from ..models.iiif_api import IIIF
from ..models.database import Herbier, Poemes
import json, requests

@app.route("/")
@app.route("/accueil")
def accueil():
    """
    Route permettant l'affichage de la page d'accueil

    Returns
    -------
    template
        Retourne le template accueil.html
    """
    # Récupération des métadonnées de l'ouvrage via l'API Présentation de Gallica
    IIIF_BASEURL = app.config['IIIF_BASEURL']
    req = requests.get(IIIF_BASEURL+"3A%2F12148%2Fbtv1b8451620k/manifest.json")

    # Conversion du résultat de la requête précédente au format JSON
    biblio = req.json()
    
    return render_template("pages/accueil.html", sous_titre="Accueil", biblio=biblio)

@app.route("/poemes")
@app.route("/poemes/<int:page>")
def poemes(page=1):
    """
    Route permettant l'affichage de la liste des poèmes.

    Parameters
    ----------
    page : int, optional
        Numéro de page

    Returns
    -------
    template
        Retourne le template sommaire_poemes.html
    """
    return render_template("pages/sommaire_poemes.html", 
        sous_titre="Sommaire des poèmes", donnees= Poemes.query.order_by(Poemes.titre).paginate(page=page, per_page=app.config["POEME_PER_PAGE"]))

@app.route("/poemes/<string:folio>", methods=["POST", "GET"])
def info_poeme(folio):
    """
    Route permettant l'affichage d'une page de poème et de ses informations.

    Parameters
    ----------
    folio : str, required
        Numéro de la vue correspondant à la page

    Returns
    -------
    template
        Retourne le template info_poeme.html
    """
    try:
        # Test de l'existence du poème dans la table
        if Poemes.query.filter(Poemes.id==folio).first():
            # Création d'une variable associée aux données requêtées dans la base
            donnees=Poemes.query.filter(Poemes.id == folio).first()
            return render_template("/pages/info_poeme.html", url=app.config['IIIF_BASEURL'], sous_titre=donnees.titre+' '+donnees.id, 
                                   donnees=donnees, folio=folio)

        # Une erreur 404 est renvoyée si la page n'existe pas
        else:
            abort(404)
        # Erreur 404 en cas d'erreur
    except Exception as erreur:
        abort(404)


@app.route('/poemes/<string:name>.pdf')
def print_pdf(name):
    """
    Route permettant la transformation des pages des poèmes en PDF.

    Parameters
    ----------
    name : str, required
        Numéro de la vue correspondant à la page transformée

    Returns
    -------
    pdf
        Retourne le document PDF issu du template info_poeme.html
    """
    # Données à présenter dans le document
    donnees = Poemes.query.filter(Poemes.id==name).first()

    # Page HTML à transformer
    html = render_template('pages/info_poeme.html', name=name, donnees=donnees)
    return render_pdf(HTML(string=html))

@app.route("/herbier")
@app.route("/herbier/<int:page>")
def herbier(page=1):
    """
    Route permettant l'affichage de la liste des planches botaniques.

    Parameters
    ----------
    page : int, optional
        Numéro de page

    Returns
    -------
    template
        Retourne le template sommaire_herbier.html
    """
    return render_template("pages/sommaire_herbier.html", url=app.config['IIIF_BASEURL'], 
        sous_titre="Sommaire de l'herbier", donnees=Herbier.query.paginate(page=page, per_page=app.config["PLANTE_PER_PAGE"]))

@app.route("/herbier/<string:folio>", methods=["POST", "GET"])
def info_plante(folio):
    """
    Route permettant l'affichage d'une planche botanique et de ses informations.

    Parameters
    ----------
    folio : str, required
        Numéro de la vue correspondant à la planche

    Returns
    -------
    template
        Retourne le template info_plante.html
    """
    try:
        # Test de l'existence de l'illustration dans la table
        if Herbier.query.filter(Herbier.id==folio).first():
            # Création d'une variable avec les données de la requête
            donnees = Herbier.query.filter(Herbier.id==folio).first()

            # Vérifier que les données n'ont pas déjà été importées pour éviter d'appeler l'API à chaque chargement de la page
            if not donnees.famille:
                # Import depuis le fichier config.py de l'URL de l'API IIIF, de la clé d'API et de la zone géographique
                API_KEY = app.config['API_KEY']
                PROJECT = app.config['PROJECT']

                # Création de l'URL pour la requête à l'API
                api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

                # Utilisation du wrapper PyGallica pour récupérer l'image, l'enregistrer et récupérer son chemin : utilisation de la méthode iiif de la classe IIIF
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

                # Mise en forme de la requête sous forme de dictionnaire
                prepared = req.prepare()

                # Création d'une session pour conserver les paramètres au fil des différentes requêtes
                s = requests.Session()

                # Envoi de la requête préparée et récupération de la réponse
                response = s.send(prepared)

                # Transformation de la réponse au format JSON vers un dictionnaire Python
                ident = json.loads(response.text)

                # Vérification de l'existence des résultats dans le dictionnaire pour éviter erreur fatale en cas d'échec de l'identification
                if 'results' in ident.keys():
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
            
                # Sinon signaler que l'identification est impossible
                else:
                    Herbier.query.filter(Herbier.id == folio).\
                    update({"famille": 'Espèce inconnue'})

                # Enfin, renvoyer le template info_plante.html qui utilisera comme données la requête ci-dessous
                return render_template("/pages/info_plante.html", url=app.config['IIIF_BASEURL'], sous_titre=donnees.poems[0].titre, 
                                       donnees=donnees, folio=folio)
            
            # Sinon, si l'identification est déjà faite, retourner directement le template avec les données
            else:
                # Cette route renvoie le template info_plante.html qui utilisera comme données la requête ci-dessous
                return render_template("/pages/info_plante.html", url=app.config['IIIF_BASEURL'], sous_titre=donnees.poems[0].titre, 
                                       donnees=donnees, folio=folio)
            
        # Une erreur 404 est renvoyée si l'illustration n'existe pas
        else:
            abort(404)
        # Erreur 404 en cas d'erreur
    except Exception as erreur:
        abort(404)

@app.route("/recherche_rapide")
@app.route("/recherche_rapide/<int:page>")
def recherche_rapide(page=1):
    """
    Route permettant à l'utilisateur de faire une recherche rapide via la navbar.

    Parameters
    ----------
    page : int, optional
        Numéro de page

    Returns
    -------
    template
        Retourne le template resultats_recherche.html
    """
    # Récupération de la chaîne dans le formulaire
    chaine = request.args.get("chaine", None)
    # Si la requête existe
    if chaine:
        # Les requêtes retournent une liste des pages des poèmes et plantes dont les données contient la chaîne.
        resultats_poemes = Poemes.query.join(Herbier, Poemes.id_plante == Herbier.id).\
            filter(or_(Poemes.titre.ilike(f"%{chaine}%"),
                        Poemes.ocr.ilike(f"%{chaine}%"),
                        Poemes.commentaire.ilike(f"%{chaine}%"))
            ).distinct(Poemes.titre).order_by(Poemes.titre).paginate(page=page)
        
        resultats_plantes = Herbier.query.join(Poemes, Poemes.id_plante == Herbier.id).\
            filter(or_(Poemes.titre.ilike(f"%{chaine}%"),
                       Herbier.commentaire.ilike(f"%{chaine}%"),
                       Herbier.famille.ilike(f"%{chaine}%"),
                       Herbier.famille2.ilike(f"%{chaine}%"),
                       Herbier.nom_latin1.ilike(f"%{chaine}%"),
                       Herbier.nom_latin2.ilike(f"%{chaine}%"),
                       Herbier.nom_latin3.ilike(f"%{chaine}%"),
                       Herbier.nom_latin4.ilike(f"%{chaine}%"),
                       Herbier.nom_commun1.ilike(f"%{chaine}%"),
                       Herbier.nom_commun2.ilike(f"%{chaine}%"),
                       Herbier.nom_commun3.ilike(f"%{chaine}%"),
                       Herbier.nom_commun4.ilike(f"%{chaine}%"))
            ).distinct(Poemes.titre).order_by(Poemes.titre).paginate(page=page)
    # En l'absence de résultats, retourner le template vide
    else:
        resultats_poemes=None
        resultats_plantes=None
    return render_template("pages/resultats_recherche.html", url=app.config['IIIF_BASEURL'], sous_titre=f"Recherche | {chaine}", 
                           donnees=resultats_poemes, donnees2=resultats_plantes, requete=chaine)