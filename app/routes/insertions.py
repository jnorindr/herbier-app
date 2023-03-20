from ..app import app, db
from flask import render_template, request, flash
from ..models.database import Herbier
from ..models.formulaires import InsertionPlante

@app.route("/insertion/plante/<string:folio>", methods=['GET', 'POST'])
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
            
            # Afficher un message confirmant la réussite de la mise à jour des informations
            flash("L'identification " + nom_latin4 + " a bien été ajoutée", "info")

    # En cas d'exception, afficher un message d'erreur
    except Exception as erreur:
        flash("Une erreur s'est produite lors de l'insertion de l'identification " + nom_latin4 + " : " + str(erreur), "error")
    
    # Retourner le template correspondant au formulaire d'insertion d'une identification
    return render_template("pages/insertion_plante.html", form=form, folio=folio)