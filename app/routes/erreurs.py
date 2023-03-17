from ..app import app, db
from flask import render_template

# Route en cas d'erreur 404 avec affichage d'un template
@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/erreurs/error404.html'), 404

# Route en cas d'erreur 500 ou 503 avec affichage d'un template
@app.errorhandler(500)
@app.errorhandler(503)
def internal_error(e):
    db.session.rollback()
    return render_template('pages/erreurs/error500.html'), 500