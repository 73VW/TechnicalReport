`Work log generator`
--------------------

📝 C'est quoi?
===============

Ce simple script python permet de générer un journal de travail au format rst à partir des commits de l'un de vos dépôts.

🔘 Comment l'utiliser?
=======================

Il est nécessaire de commencer par générer un jeton d'accès et de l'écrire dans le fichier tokens.py.

Pour le générer, rendez-vous `ici`_ dans la section "Personal access tokens".

À présent, vous pouvez appeler le script avec le dépôt désiré comme paramètre.

À titre d'example, si nous désirions générer un journal de travail basé sur ce dépôt, il nous suffirait de lancer `python get_commits_and_write.py TechnicalReportGenerator`.

Le nom du fichier généré est "workLog.rst".

Il est maintenant possible de le convertir en utilisant pandoc ou n'importe quelle autre convertisseur que vous préférez.

Enjoy!


📝 What is this?
================

This simple python script allows you to generate a worklog in rst format based on your repo commits.

🔘 How to use it?
=================

Simply generate a personnal access token and put it in the file tokens.py.

In order to generate this token, go `here`_ under "Personal access tokens".

Then, you can call the script with the repo you want to use as parameter.

As an example, if we wanted to generate a worklog based on this repository, we would just run `python get_commits_and_write.py TechnicalReportGenerator`.

The output file's name is "workLog.rst".

You can then convert it using pandoc or any other converter you prefer.

Enjoy!

.. _`ici`: https://github.com/settings/tokens
.. _`here`: https://github.com/settings/tokens
