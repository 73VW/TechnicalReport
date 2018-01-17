`Français`
----------

Les fichiers présents dans ce dépôt permettent la création d'un rapport pdf en utilisant un fichier source rst ou md en utilisant pandoc et latex. Un template et un fichier de configuration disponibles dans le dossier tools_ sont utilisés.

⚠️**Testé uniquement sur windows!**

Le pdf_ créé à partir de ce readme se trouve dans le dépôt à titre d'exemple.

À faire
#######

1. Créer le fichier rest ou markdown contenant juste le contenu du rapport (comme ce readme).
2. Renseigner les champs nécessaires présents dans le fichier `tools/project_infos.yaml`.
3. Ouvrir un terminal au niveau du Makefile et lancer la commande `make`. L'aide s'affiche.
4. En utilisant `make all` sans paramètres, le script cherche les fichiers rst ou md et génère les pdf correspondants.

Essai d'utilisation d'image
###########################

.. figure:: img/samiral.png
    :width: 30%
    :height: 30%
    :alt: samiral-logo

    Voici le logo du S-Amiral crew!

    Ce logo ne représente pas grand chose si ce n'est le nom du crew.

Peu importe où se place la figure Fig. $\ref{img/samiral.png}$, elle sera référencée dans le lien.


`English`
---------

The files in this repository allow to create a pdf report using a `md` or `rst` source file using `pandoc` and `latex`. A template and a configuration file available in the tools_ directory are used to build the file correctly.

⚠️**Only tested on windows for the moment!**

The pdf_ file created from this readme can be found in the repository as an example

How to
#######

1. Create a rest or markdown file containing only the content of the report (just like the file you are reading right now).
2. Fill the fields in the file `tools/project_infos.yaml`.
3. Open a terminal at the makefile level and run `make`. The help should appear.
4. When using make all without parameters, the script will look for rest or markdown files and generate the corresponding pdf.

Image usage test
################

It doesn't matter where the figure Fig. $\ref{img/samiral.png}$ will go. It will always be linked.

.. _tools: ./tools
.. _pdf: https://github.com/73VW/TechnicalReport/blob/build/README.pdf
