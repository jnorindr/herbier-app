# herbier-app
Cette application permet de récupérer via l'API IIIF de Gallica les images du recueil de poèmes _[La Guirlande de Julie](https://gallica.bnf.fr/ark:/12148/btv1b8451620k)_. Appuyée sur l'[API Pl@ntNet](https://my.plantnet.org/), elle propose d'identifier les fleurs représentées dans les planches botaniques du recueil. Pour les poèmes du recueil, une transcription automatique réalisée avec [eScriptorium](https://traces6.paris.inria.fr/) est mise à disposition de l'utilisateur, qui peut également ajouter ses propres transcriptions et identifications, et exporter aux format PDF les images accompagnées de ses annotations.

Cette application a été réalisée avec Flask et SQLAlchemy par [Clara Hermant-Bertoni](https://github.com/ClaraHB98) et Jade Norindr dans le cadre du cours de Python du master Technologies numériques appliquées à l'histoire de l'École des chartes.

## Installation

Pour l'installation, vous aurez besoin de vous inscrire et de générer une clé d'API Pl@ntNet : https://my.plantnet.org/

- Cloner le dépôt : ```git clone https://github.com/jnorindr/herbier-app```
- Vérifier que la version de Python installée correspond à Python 3.X : ```python --version```. Sinon, l'installer avec la commande ```sudo apt-get install python3 python3-pip python3-virtualenv``` (vous aurez besoin des droits administrateur pour lancer cette commande).
- Se déplacer dans le dossier de l'application : ```cd herbier-app```
- Installer la base de données à la racine de l'application
- Créer un environnement virtuel : ```virtualenv env -p python3```
- À la racine de l'application, créer un fichier ```.env``` contenant les variables suivantes :
```
DEBUG = True
API_KEY = "[votre_clé_API]"
PROJECT = "weurope"
SQLALCHEMY_DATABASE_URI = sqlite:////[chemin]/appli.sqlite
WTF_CSRF_ENABLE = True
SECRET_KEY = [clé_secrète_personnelle]
PLANTE_PER_PAGE = 5
POEME_PER_PAGE = 10
```
- Activer l'environnement virtuel : ```source env/bin/activate```
- Installer les packages nécessaires au fonctionnement de l'application : ```pip install -r requirements.txt```
- Lancer l'application : ```python run.py```

- L'application dispose d'une interface d'administration graphique : pour y accéder, créer un compte avant pour nom d'utilisateur ```Administrateur``` et se rendre à l'URL ```/admin```
- Pour arrêter l'application : ```Ctrl + C```, puis désactivez l'environnement avec la commande ```deactivate```

## Lancement de l'application

Après la première installation, pour lancer l'application, il faut activer l'environnement ```source env/bin/activate``` et le lancer l'application ```python run.py```

## Fonctionnalités proposées par l'application 
Le Poète à la main verte permet de :
  - Découvrir via un sommaire herbier toutes les illustrations de plante recensées dans le manuscrit _[La Guirlande de Julie](https://gallica.bnf.fr/ark:/12148/btv1b8451620k)_.Celui-ci propose une miniature de chaque illustration, et le titre du poème qui lui est associé. 
  <picture>
  </picture>
