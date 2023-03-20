from ..app import app, db
from flask import url_for, render_template, request, redirect, flash
from ..models.users import Users
from ..models.formulaires import CreationUtilisateur

@app.route("/utilisateurs/creation", methods=["GET", "POST"])
def creation_utilisateur():
    """
    Route permettant l'insertion d'un utilisateur dans la table users.

    Returns
    -------
    app.models.users.Users
        Insère une ligne dans la table users et crée une instance de la classe Users si l'insertion est un succès.
    template
        Retourne le template insertion_plante.html
    """
    form = CreationUtilisateur()

    # Si le formulaire est rempli et soumis, créer une instance de la classe Users
    if form.validate_on_submit():
        statut, donnees = Users.create_user(
            pseudo = request.form.get("pseudo", None),
            password = request.form.get("password", None)
        )
        # Si statut n'est pas nul, renvoyer un message confirmant la création de l'utilisateur et retourner la page d'accueil
        if statut:
            flash("Votre compte a bien été créé", "success")
            return redirect(url_for("herbier"))
        # MODIFIER RETOUR POUR PAGE D'ACCUEIL QUAND CRÉÉE

        # Sinon, renvoyer les erreurs et retourner la page d'inscription
        else:
            flash(",".join(donnees), "error")
            return render_template("pages/creation_utilisateur.html", form=form)
    
    # Sinon, retourner la page d'inscription
    else:
        return render_template("pages/creation_utilisateur.html", form=form)
