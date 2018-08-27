#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Used to manually notify users (especially for functionalities updates)

import telegram
from lunchbot import TOKEN
from dbconnector import get_users

def notify_users():
	NOTICE = """
	Bonjour %s J'ai été mis à jour.
	Quelques améliorations sur ma vitesse de réponse ont été effectuées.
	Tu m'en diras des nouvelles :)
	"""

	bot = telegram.Bot(token=TOKEN)
	users = get_users()

	for u in users:
		try:
			chat = bot.getChat(u[0])
			print(u, " ", chat.username, " ", chat.first_name, " ", chat.last_name)
			bot.send_message(chat_id=chat.id, text=NOTICE % chat.first_name)

		except(telegram.error.BadRequest):
			print("ERROR : ", u)
			continue

if __name__ == '__main__':
	notify_users()
