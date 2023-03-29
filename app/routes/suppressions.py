from ..app import app, db
from flask import render_template, request, flash
from flask_login import login_required
from ..models.database import Herbier, Poemes

@app.route("/suppression/poeme/<string:folio>", methods=["GET", "POST"])
@login_required
def suppression_poeme(folio):
    """
    Route permettant la suppression du commentaire et de la transcription sur une page de la table poemes

    Parameters
    ----------
    folio : str, required
        Numéro de la vue correspondant à la page

    Returns
    -------
    app.models.database.Poemes
        Met à jour une ligne de la table poemes si la suppression est un succès.
    template
        Retourne le template info_poeme.html qui comporte un bouton de suppression.
    """
    # Création d'une variable poeme correspondant au poème dont l'id est identique au folio
    donnees=Poemes.query.filter(Poemes.id == folio).first()

    try:
        # Supprimer la transcription et le commentaire
        Poemes.query.filter(Poemes.id == folio).\
                    update({"ocr": None, "commentaire": None})
        db.session.commit()

        # Retourner un message confirmant la suppression et le template du poème concerné
        flash(f"La transcription du poème {folio} a bien été supprimée.", "info")
        return render_template("/pages/info_poeme.html", donnees=donnees, folio=folio)

    # Sinon, renvoyer un message d'erreur et retourner le template
    except Exception as erreur:
        flash(f"Une erreur s'est produite lors de la suppression de la transcription {folio} ({str(erreur)}).", "warning")
    return render_template("/pages/info_poeme.html", donnees=donnees, folio=folio)


@app.route("/suppression/herbier/<string:folio>", methods=["GET", "POST"])
@login_required
def suppression_plante(folio):
    """
    Route permettant la suppression de l'identification de l'utilisateur sur une page de la table plante

    Parameters
    ----------
    folio : str, required
        Numéro de la vue correspondant à la page

    Returns
    -------
    app.models.database.Herbier
        Met à jour une ligne de la table herbier si la suppression est un succès.
    template
        Retourne le template info_plante.html qui comporte un bouton de suppression.
    """
    # Création d'une variable donnees correspondant à la planche dont l'id est identique au folio
    donnees=Herbier.query.filter(Herbier.id == folio).first()

    try:
        # Supprimer l'identification
        Herbier.query.filter(Herbier.id == folio).\
                    update({"famille2": None, "nom_commun4": None, 
                            "nom_latin4": None, "commentaire": None})
        db.session.commit()

        # Retourner un message confirmant la suppression et le template de la planche concernée
        flash(f"L'identification {folio} a bien été supprimée.", "info")
        return render_template("/pages/info_plante.html", donnees=donnees, folio=folio)

    # Sinon, renvoyer un message d'erreur et retourner le template
    except Exception as erreur:
        flash(f"Une erreur s'est produite lors de la suppression de l'identification {folio} ({str(erreur)}).", "warning")
    return render_template("/pages/info_plante.html", donnees=donnees, folio=folio)

