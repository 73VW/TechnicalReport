Français
--------

Les fichiers présents dans ce dépôt permettent la création d'un rapport pdf en utilisant un fichier source rst ou md en utilisant pandoc et latex. Un template et un fichier de configuration disponibles dans le dossier templates sont utilisés.

**Testé uniquement sur windows!**

Le pdf créé à partir de ce readme se trouve dans le dépôt à titre d'exemple.

À faire
#######

1. Créer le fichier rest ou markdown contenant juste le contenu du rapport (comme ce readme)
2. Renseigner les champs nécessaires présents dans le fichier templates/header.yaml
3. Ouvrir un terminal au niveau du Makefile et lancer la commande `make`. L'aide s'affiche.
4. En utilisant `make all` sans paramètres, le script cherche les fichiers rst ou md et génère les pdf correspondants.
