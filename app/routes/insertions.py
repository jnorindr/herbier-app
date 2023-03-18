from ..app import app, db
from flask import render_template, request, flash
from ..models.database import Herbier
from ..models.formulaires import InsertionPlante

@app.route("/insertion/plante/<string:folio>", methods=['GET', 'POST'])
def insertion_plante(folio):
    form = InsertionPlante()

    try:
        if form.validate_on_submit():
            famille2 = request.form.get("famille2", None)
            nom_commun4 = request.form.get("nom_commun4", None)
            nom_latin4 = request.form.get("nom_latin4", None)
            commentaire = request.form.get("commentaire", None)

            Herbier.query.filter(Herbier.id == folio).\
                    update({"famille2": famille2, "nom_commun4": nom_commun4, 
                            "nom_latin4": nom_latin4, "commentaire": commentaire})
            db.session.commit()
            flash("L'identification " + nom_latin4 + " a bien été ajoutée", "info")

    except Exception as erreur:
        flash("Une erreur s'est produite lors de l'insertion de l'identification " + nom_latin4 + " : " + str(erreur), "error")

    return render_template("pages/insertion_plante.html", form=form, folio=folio)