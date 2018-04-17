# Lunchbot

Lunchbot est un bot telegram qui permet de consulter le solde restant sur sa 
carte ainsi que le menu du restaurant de la tour Franklin à la défense :
[Eurest Franklin](http://www.tourfranklin.eurest.fr/home.aspx)

*Lunchbot nécessite python3*

## Quick start

* Clonez le dépôt : `git clone https://github.com/PercevalSA/lunch-bot.git`
* Installez les dépendances : `pip3 install --upgrade requests bs4 python-telegram-bot`
* Modifiez le fichier `lunchbot.py` pour y jouter le
[jeton](https://core.telegram.org/bots/api#authorizing-your-bot)
de votre bot dans la variable `TOKEN`. Vous pouvez en demander un auprès du
[botfather](http://telegram.me/botfather).
* Démarrez le bot : `python3 lunchbot.py`
* Enjoy !

## Commandes

* `/money` : consulter son solde
* `/menu` : afficher le menu du jour
* `/addme BadgeID NOM Prénom` s'enregistrer auprès du bot pour consulter
son solde (le BadgeID se trouve sur les tickets de caisse)
* `/forgetme` : supprimer ses identifiants de la base
* `/bonjour` : bonjour, une fois!

## TO DO

* Ajouter la consultation quotidienne unique et l'enregistrement du solde
(~7h30) [performances]
* Migrer de Shelve vers SQLite ?
* Gestion des statistiques de consommation
* Gestion du menu des autres jours de la semaine