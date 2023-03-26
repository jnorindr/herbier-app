from ..app import app, db, login
from flask import url_for, render_template, request, redirect, flash
from flask_login import login_user, logout_user, current_user
from ..models.users import Users
from ..models.formulaires import CreationUtilisateur, Connexion

@app.route("/utilisateurs/creation", methods=["GET", "POST"])
def creation_utilisateur():
    """
    Route permettant l'insertion d'un utilisateur dans la table users.

    Returns
    -------
    app.models.users.Users
        Insère une ligne dans la table users et crée une instance de la classe Users si l'insertion est un succès.
    template
        Retourne le template creation_utilisateur.html
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
            return redirect(url_for("accueil"))

        # Sinon, renvoyer les erreurs et retourner la page d'inscription
        else:
            flash(",".join(donnees), "error")
            return render_template("partials/formulaires/creation_utilisateur.html", form=form)
    
    # Sinon, retourner la page d'inscription
    else:
        return render_template("partials/formulaires/creation_utilisateur.html", form=form)

@app.route("/utilisateurs/connexion", methods=["GET", "POST"])
def connexion():
    """
    Route permettant la connexion de l'utilisateur.

    Returns
    -------
    template
        Retourne le template connexion.html si l'utilisateur n'existe pas. Retourne la page d'accueil si l'utilisateur existe.
    """
    form = Connexion()

    # Vérification que l'utilisateur n'est pas déjà connecté : si l'utilisateur est connecté, retour à la page d'accueil
    if current_user.is_authenticated:
        flash("Vous êtes déjà connecté", "info")
        return redirect(url_for("accueil"))
    
    # Si le formulaire est rempli et soumi, vérification de l'existence de l'utilisateur dans la base
    if form.validate_on_submit():
        utilisateur = Users.identification(
            pseudo=request.form.get("pseudo", None),
            password=request.form.get("password", None)
        )
        # Si l'utilisateur existe, le connecter
        if utilisateur:
            flash("Vous êtes connecté", "success")
            login_user(utilisateur)
            return redirect(url_for("accueil"))
        # Sinon, retourner la page de connexion
        else:
            flash("L'identifiant ou le mot de passe est incorrect", "error")
            return render_template("partials/formulaires/connexion.html", form=form)
        
    # Sinon, retourner la page de connexion
    else:
        return render_template("partials/formulaires/connexion.html", form=form)

# Définition de la page retournée automatiquement quand l'utilisateur non-connecté essaye d'accéder aux pages avec restriction
login.login_view = "connexion"

@app.route("/utilisateurs/deconnexion", methods=["POST", "GET"])
def deconnexion():
    """
    Route permettant la déconnexion de l'utilisateur.

    Returns
    -------
    template
        Retourne le template accueil.html.
    """
    # Vérification que l'utilisateur est connecté : si oui, le déconnecter et retourner la page d'accueil
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté", "info")
    return redirect(url_for("accueil"))