from ..app import app, db
from flask import render_template, request, flash
from flask_login import login_required
from ..models.database import Herbier, Poemes
from ..models.formulaires import InsertionPlante, InsertionPoeme

@app.route("/insertion/poeme/<string:folio>", methods=['GET', 'POST'])
@login_required
def insertion_poeme(folio):
    """
    Route permettant l'insertion d'un commentaire sur une page de la table poemes

    Parameters
    ----------
    folio : str, required
        Numéro de la vue correspondant à la page

    Returns
    -------
    app.models.database.Poemes
        Met à jour une ligne de la table poemes si l'insertion est un succès.
    template
        Retourne le template insertion_poeme.html
    """
    form = InsertionPoeme()
    donnees=Poemes.query.filter(Poemes.id == folio).first()

    try:
        # Si le formulaire est rempli et soumi, récupérer les informations
        if form.validate_on_submit():
            ocr = request.form.get("ocr", None)
            commentaire = request.form.get("commentaire", None)

            # Mettre à jour la ligne de la table poemes donc la valeur de l'id est égale à la valeur de la variable folio pour y insérer les données du formulaire
            Poemes.query.filter(Poemes.id == folio).\
                    update({"commentaire": commentaire, "ocr": ocr})
            db.session.commit()
            
            # Afficher un message confirmant la réussite de la mise à jour des informations et retourner la page du poème
            flash("La transcription a bien été modifiée", "info")
            return render_template("/pages/info_poeme.html", donnees=donnees, folio=folio)

    # En cas d'exception, afficher un message d'erreur
    except Exception as erreur:
        flash("Une erreur s'est produite : " + str(erreur), "error")
    
    # Retourner le template correspondant à la page d'insertion
    return render_template("/pages/insertion_poeme.html", donnees=donnees, form=form, folio=folio)

@app.route("/insertion/plante/<string:folio>", methods=['GET', 'POST'])
@login_required
def insertion_plante(folio):
    """
    Route permettant l'insertion de l'identification et d'un commentaire sur une planche dans la table herbier

    Parameters
    ----------
    folio : str, required
        Numéro de la vue correspondant à la planche

    Returns
    -------
    app.models.database.Herbier
        Met à jour une ligne de la table herbier si l'insertion est un succès.
    template
        Retourne le template insertion_plante.html
    """
    form = InsertionPlante()

    try:
        # Si le formulaire est rempli et soumi, récupérer les informations
        if form.validate_on_submit():
            famille2 = request.form.get("famille2", None)
            nom_commun4 = request.form.get("nom_commun4", None)
            nom_latin4 = request.form.get("nom_latin4", None)
            commentaire = request.form.get("commentaire", None)

            # Mettre à jour la ligne de la table herbier donc la valeur de l'id est égale à la valeur de la variable folio pour y insérer les données du formulaire
            Herbier.query.filter(Herbier.id == folio).\
                    update({"famille2": famille2, "nom_commun4": nom_commun4, 
                            "nom_latin4": nom_latin4, "commentaire": commentaire})
            db.session.commit()
            
            # Afficher un message confirmant la réussite de la mise à jour des informations et retourner la page de la planche
            flash("L'identification " + nom_latin4 + " a bien été ajoutée", "info")
            return render_template("/pages/info_plante.html", donnees=Herbier.query.filter(Herbier.id == folio).first(), folio=folio)

    # En cas d'exception, afficher un message d'erreur
    except Exception as erreur:
        flash("Une erreur s'est produite lors de l'insertion de l'identification " + nom_latin4 + " : " + str(erreur), "error")
    
    # Retourner le template correspondant à la page d'insertion
    return render_template("/pages/insertion_plante.html", form=form, folio=folio)