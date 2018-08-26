#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Balance and Menu Notifier

from lunchbot import TOKEN
import telegram, dbconnector, franklin

bot = telegram.Bot(token=TOKEN)

def notify_all_users():

	users = dbconnector.get_notifications()
	menu = franklin.get_menu()

	for u in users:
		try:
			user = u[0]
			notification = u[1]

			chat = bot.getChat(user)
			print(u, " ", chat.username, " ", chat.first_name, " ", chat.last_name)

			if(notification == 0):
				pass
			elif(notification == 1 or notification == 3):
				# menu
				bot.send_message(chat_id=chat.id, text=menu)

			elif(notification == 2 or notification == 3):
				# sold
				money, date = dbconnector.get_balance(user)
				
				if(money != None):
					message = "Solde disponible : " + str(money) + " €\n"\
					+ "Date de dernière mise à jour : " + str(date)
					bot.send_message(chat_id=chat.id, text=message)
			else:
				printf("notification combination impossibru")

		except(telegram.error.BadRequest):
			print("ERROR : ", u)
			continue

# Notify all users with balances and menu
# used for cron job
if __name__ == '__main__':
	notify_all_users()
