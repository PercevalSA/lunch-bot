# Lunchbot

Lunchbot est un bot telegram qui permet de servir le menu du restaurant de la ville de Paris : [ASPP Jean Rey](http://www.aspp.fr/restaurants/28). Lunchbot nécessite python3 pour tourner.

## Quick start

* Clonez le dépôt : `git clone https://github.com/PercevalSA/lunch-bot.git`
* Installez les dépdances : `pip3 install --upgrade requests python-telegram-bot`
* Modifiez le fichier `settings.py` pour y jouter le [jeton](https://core.telegram.org/bots/api#authorizing-your-bot) de votre bot dans la variable `TOKEN`. Vous pouvez en demander un auprès du [botfather](http://telegram.me/botfather).
* Déplacer vous dans le dossier du bot : `cd lunch-bot`
* Permettez l'execution du bot : `chmod u+x lunchbot.py`
* Démarrez le : `./lunchbot.py`
* Enjoy !

## TO DO

* Gestion des soldes
* Gestion des statistiques de consommation
* Gestion des autres jours de la semaine
