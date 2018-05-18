#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import telegram
from lunchbot import TOKEN

USERS = {}

NOTICE = """
Bonjour %s, J'ai été mis à jour ! 🔄🎇🆙🎆🆕🎈🎊🎉
Cette mise à jour augmente ma stabilité et mes performances. 

Pour permettre cette progression, le format et le stockage des données ont été améliorés. \
Cependant, la migration des comptes n'a pas pu être effectuée et j'en suis navré. 😱😢😭

Pour continuer à utiliser Franklin Bot, il est nécessaire de te réinscrire avec la commande suivante : 
/register BadgeID Nom Prénom

Désolé pour la gêne occasionnée. 🙃🙃🙃
Bon Appétit 🍽☕️

@paris_lunch_bot

PS :  Si tu trouves des bugs, n'hésites pas à les remonter sur github :
https://github.com/percevalsa/lunch-bot/issues/
"""

print("\n\tSending update notice tu users...\n")
bot = telegram.Bot(token=TOKEN)

for u in USERS:
	try:
		chat = bot.getChat(u)
		print(u, " ", chat.username, " ", chat.first_name, " ", chat.last_name)
		bot.send_message(chat_id=chat.id, text=NOTICE % chat.first_name)

	except(telegram.error.BadRequest):
		print("ERROR : ", u)
		continue

print("\n\tUpdate notice send.\n")
