#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import telegram

TOKEN= ""
USERS = []

bot = telegram.Bot(token=TOKEN)
print(bot.get_me())

for u in USERS:
	chat = bot.getChat(u)
	print("User : ", chat.username)
	print("User Name : ", chat.first_name, " ", chat.last_name)
