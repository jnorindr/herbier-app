from ..app import app, db
from flask import render_template

# Route en cas d'erreur 403 avec affichage d'un template
@app.errorhandler(403)
def page_not_found(erreur):
    """
        Route permettant l'affichage d'une page d'erreur personnalisée en cas d'accès non autorisé

        Parameters
        ----------
        erreur : required
            L'erreur retournée en cas d'exception sur la route

        Returns
        -------
        template
            Retourne le template error403.html
    """
    return render_template('pages/erreurs/error403.html'), 403

# Route en cas d'erreur 404 avec affichage d'un template
@app.errorhandler(404)
def page_not_found(erreur):
    """
        Route permettant l'affichage d'une page d'erreur personnalisée en cas de ressource non trouvée

        Parameters
        ----------
        erreur : required
            L'erreur retournée en cas d'exception sur la route

        Returns
        -------
        template
            Retourne le template error404.html
    """
    return render_template('pages/erreurs/error404.html'), 404

# Route en cas d'erreur 500 ou 503 avec affichage d'un template
@app.errorhandler(500)
@app.errorhandler(503)
def internal_error(erreur):
    """
        Route permettant l'affichage d'une page d'erreur personnalisée en cas de problème inattendu du serveur

        Parameters
        ----------
        erreur : required
            L'erreur retournée en cas d'exception sur la route

        Returns
        -------
        template
            Retourne le template error500.html
    """
    db.session.rollback()
    return render_template('pages/erreurs/error500.html'), 500