#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Used to manually notify users (especially for functionalities updates)

import telegram
from lunchbot import TOKEN
import dbconnector

NOTICE = """
Bonjour %s ...
"""
print("\n\tSending update notice to users...\n")

bot = telegram.Bot(token=TOKEN)
users = dbconnector.get_users()

for u in users:
	try:
		chat = bot.getChat(u[0])
		print(u, " ", chat.username, " ", chat.first_name, " ", chat.last_name)
		bot.send_message(chat_id=chat.id, text=NOTICE % chat.first_name)

	except(telegram.error.BadRequest):
		print("ERROR : ", u)
		continue

print("\n\tUpdate notice send.\n")
