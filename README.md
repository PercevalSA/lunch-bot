# Lunchbot

Lunchbot est un bot telegram qui permet de consulter le solde restant sur sa 
carte ainsi que le menu du restaurant de la tour Franklin à la défense :
[Eurest Franklin](http://www.tourfranklin.eurest.fr/home.aspx)

*Lunchbot nécessite python3*

## Quick start

* Clonez le dépôt : `git clone --recurse-submodules https://github.com/PercevalSA/lunch-bot.git`
* Installez les dépendances : `pip3 install --upgrade bitarray bs4 json python-telegram-bot requests`
* Modifiez le fichier `lunchbot.py` pour y jouter le
[jeton](https://core.telegram.org/bots/api#authorizing-your-bot)
de votre bot dans la variable `TOKEN`. Vous pouvez en demander un auprès du
[botfather](http://telegram.me/botfather).
* Démarrez le bot : `python3 lunchbot.py`
* Enjoy !

## Installation complète

* Créez un nouvel utilisateur :
```bash
sudo adduser tgbot # créer un utilisateur pour le bot
```

* Installez lunchbot :
```bash
sudo -s tgbot && cd /home/tgbot
git clone --recurse-submodules https://github.com/PercevalSA/lunch-bot.git # clone le dépôt
pip3 install --upgrade bitarray bs4 json python-telegram-bot requests # installe les dépendances
```

* Modifiez le fichier `lunchbot.py` pour y jouter le
[jeton](https://core.telegram.org/bots/api#authorizing-your-bot)
de votre bot dans la variable `TOKEN`. Vous pouvez en demander un auprès du
[botfather](http://telegram.me/botfather).

* Ajoutez les service du bot au système pour la mise à jour des soldes avec
`sudo cp service/* /etc/systemd/system/`

* Activez les services
```bash
sudo systemctl enable lunchbot lunchbot-db-update lunchbot-backup lunchbot-notify
sudo systemctl start lunchbot lunchbot-db-update lunchbot-backup lunchbot-notify
```

* Enjoy !

En production, vous pouvez utiliser un webhook au lieu de la fonction poll :
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks

## Commandes

* `/money` consulter son solde
* `/menu` afficher le menu du jour
* `/register BadgeID NOM Prénom` s'enregistrer auprès du bot pour consulter
son solde (le BadgeID se trouve sur les tickets de caisse)
* `/forgetme` supprimer ses identifiants de la base
* `/notification` recevoir le menu et son solde tous les jours à 11h45
* `/bonjour` Habile !
* `/cepafo` C'est pas faux !
* `/ouiches` Georges Abitbol

## Extra

`migrate.py` permet d'envoyer un message directement à tous les utilisateurs du bot.
Utile notemment pour annoncer les mises à jours ou maintenances aux utilisateurs.

## TO DO

* Gestion des statistiques de consommation
* Gestion du menu des autres jours de la semaine
* Ajout d'alertes sur le solde à partir d'un certain seuil
