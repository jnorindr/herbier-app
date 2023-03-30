from flask_admin.contrib.sqla import ModelView
from flask import abort
from flask_login import current_user

class MyModelView(ModelView):
    """
    Une classe représentant les pages des modèles dans l'interface graphique d'administration.

    Methods
    -------
    is_accessible(self)
        Permet de vérifier que l'utilisateur est connecté et que son pseudo est "Administrateur".
    """
    def is_accessible(self):
        """
        Permet la vérification de certains critères à remplir par l'utilisateur pour avoir accès aux pages de l'interface graphique d'administration.

        Parameters
        ----------
        self
            Une instance de la classe MyModelView

        Returns
        -------
        Booléen
            True si l'utilisateur a pour pseudo "Administrateur", sinon False.
        """
        try:
            return current_user.pseudo == "Administrateur"
        except Exception as erreur:
            abort(403)
