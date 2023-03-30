# Le poète à la main verte
Cette application permet de récupérer via l'API IIIF de Gallica les images du recueil de poèmes _[La Guirlande de Julie](https://gallica.bnf.fr/ark:/12148/btv1b8451620k)_. Appuyée sur l'[API Pl@ntNet](https://my.plantnet.org/), elle propose d'identifier les fleurs représentées dans les planches botaniques du recueil. Pour les poèmes du recueil, une transcription automatique réalisée avec [eScriptorium](https://traces6.paris.inria.fr/) est mise à disposition de l'utilisateur, qui peut également ajouter ses propres transcriptions et identifications, et exporter aux format PDF les images accompagnées de ses annotations.

Cette application a été réalisée avec Flask et SQLAlchemy par [Clara Hermant-Bertoni](https://github.com/ClaraHB98) et Jade Norindr dans le cadre du cours de Python du master Technologies numériques appliquées à l'histoire de l'École des chartes.

## Installation

Pour l'installation, vous aurez besoin de vous inscrire et de générer une clé d'API Pl@ntNet : https://my.plantnet.org/

- Cloner le dépôt : ```git clone https://github.com/jnorindr/herbier-app```
- Vérifier que la version de Python installée correspond à Python 3.X : ```python3 --version```. Sinon, l'installer avec la commande ```sudo apt-get install python3 python3-pip python3-virtualenv``` (vous aurez besoin des droits administrateur pour lancer cette commande).
- Se déplacer dans le dossier de l'application : ```cd herbier-app```
- Installer la base de données à la racine de l'application
- Créer un environnement virtuel : ```virtualenv env -p python3```
- À la racine de l'application, créer un fichier ```.env``` contenant les variables suivantes :
```
DEBUG = True
IIIF_BASEURL = 'https://gallica.bnf.fr/iiif/ark%'
API_KEY = "[votre_clé_API]"
PROJECT = "weurope"
SQLALCHEMY_DATABASE_URI = sqlite:////[chemin du répertoire home jusqu'au dépôt cloné]/herbier-app/appli.sqlite
WTF_CSRF_ENABLE = True
SECRET_KEY = [clé_secrète_personnelle]
PLANTE_PER_PAGE = 5
POEME_PER_PAGE = 10
```
- Activer l'environnement virtuel : ```source env/bin/activate```
- Installer les packages nécessaires au fonctionnement de l'application : ```pip install -r requirements.txt```
- Lancer l'application : ```python run.py```

- Pour arrêter l'application : ```Ctrl + C```, puis désactivez l'environnement avec la commande ```deactivate```

## Lancement de l'application

Pour lancer l'application après la première installation :
- Se déplacer dans le dossier de l'application
- Activer l'environnement : ```source env/bin/activate```
- Lancer l'application : ```python run.py```

## Fonctionnalités proposées par l'application 

Le Poète à la main verte a été construit autour de deux principaux axes : le coin herbier et le coin poèmes. 
Dans le premier cas, il est proposé à l'utilisateur de : 
  - Découvrir via le sommaire de l'herbier toutes les illustrations de plantes recensées dans le manuscrit _[La Guirlande de Julie](https://gallica.bnf.fr/ark:/12148/btv1b8451620k)_. Celui-ci propose une miniature de chaque illustration, et le titre du poème qui lui est associé. 

Une fois la plante séléctionnée, une page individuelle s'affiche à l'utilisateur. Celle-ci propose une vue individuelle de la planche botanique choisie, les métadonnées apportées par l'API Pl@ntNet sur celle-ci, et la possibilité pour l'utilisateur d'ajouter sa propre identification qui sera rendue visible à la prochaine consultation de cette même planche botanique.
Enfin, une route conduisant au poème associé a été créée pour que l'utilisateur puisse naviguer entre les illustrations et les poèmes du manuscrit.


![vue_info_plante](https://user-images.githubusercontent.com/119687553/228597504-eac9a30c-0710-488f-bc39-d99e1590b019.png)
  
  
  - Le coin poèmes du site a été pensé de la même façon que le coin herbier. Un sommaire propose à l'utilisateur une liste des poèmes du recueil de référence appelés par leur titre et les numéros de folio correspondant.

Sur les pages indivuelles des poèmes, une vue du poème et une version texte de la transcription automatique de celui-ci fournie par eScriptorium. L'utilisateur peut découvrir la plante associée au poème, et exporter la version texte en format PDF. Enfin, il peut choisir de corriger la transcription de celui-ci. Pour cela, il doit se connecter à son compte ou s'enregistrer, et pourra laisser un commentaire pour apporter des précisions sur ses modifications. Une fois le travail soumis, la nouvelle transcription apparaitra à la prochaine consultation du poème. 


![vue_info_poeme](https://user-images.githubusercontent.com/119687553/228839644-06eac33e-93e1-47b7-8490-42a552f1e0a6.png)

Ces fonctionnalités d'intégration ou de modification proposées à l'utilisateur s'ajoutent à la base de données en SQLite reliée à l'application, dont nous proposons ici le modèle physique : 

![modele_donnees_herbier](https://user-images.githubusercontent.com/106514875/228983692-5db417f0-ffac-4cef-b354-e48adb1cb40d.png)
