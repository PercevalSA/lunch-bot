#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Used to manually notify users (especially for functionalities updates)

import telegram, sqlite3
from lunchbot import TOKEN
from dbconnector import DB_FILE, get_users

def notify_users():
	NOTICE = """
	Bonjour %s J'ai été mis à jour.
	Je peux désormais t'indiquer automatiquement ton solde et/ou le menu du jour \
	à 11h50 :) Pour cela envoie la commande /notification
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

def db_migrate():
	try:
		db = sqlite3.connect(DB_FILE)
		cursor = db.cursor()

		# check data before
		cursor.execute("""
			select users.tg_id, eurest_id, eurest_name, balance, last_update
			from users, balances
			where users.tg_id == balances.tg_id
		""")
		print(cursor.fetchall())

		# migrate database into users table
		cursor.executescript("""
			alter table users add balance REAL;
			alter table users add last_update TEXT;
			alter table users add notification INTEGER;
			update users set balance = (select balance from balances where users.tg_id = balances.tg_id);
			update users set last_update = (select last_update from balances where users.tg_id = balances.tg_id);
			drop table balances;
		""")

		# check data after
		cursor.execute("""select * from users""")
		print(cursor.fetchall())
	
	except sqlite3.OperationalError:
		print('Erreur la table existe déjà')
	except Exception as e:
		print("Erreur : " + e)
		db.rollback()
	finally:
		db.close()

if __name__ == '__main__':
	db_migrate()
	print("Reboot Franklin!")
	notify_users()
