#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Database connector

import sqlite3
import franklin

# use absolute path for update timer
DB_FILE = "/home/tgbot/lunch-bot/users.db"

#
# USERS
def new_user(tg_id, eurest_id, eurest_name):

	# Convert inputs to integers
	try:
		TG_ID = int(tg_id)
		EUREST_ID = int(eurest_id)
	except ValueError:
		print("wrong input : all ID are not integers\n")
		return -1

	# Check user existence
	if franklin.check_user(EUREST_ID, eurest_name):

		# Insertion in database
		db = sqlite3.connect(DB_FILE)
		cursor = db.cursor()
		cursor.execute("INSERT INTO users(tg_id, eurest_id, eurest_name, balance)\
			VALUES (?, ?, ?, ?)", (TG_ID, EUREST_ID, eurest_name, 0))
		db.commit()
		db.close()
		return 0

	else:
		print("wrong input : user does not exist\n")
		return -2


def get_user(tg_id, eurest=False):

	# columns to return
	if(eurest):
		columns = "eurest_id, eurest_name"
	else:
		columns = "*"

	# database request
	user = None
	try:
		db = sqlite3.connect(DB_FILE)
		cursor = db.cursor()

		cursor.execute("SELECT " + columns + " FROM users WHERE tg_id=?", (tg_id,))

		user = cursor.fetchone()
	except Exception as e:
		print("Erreur : " + str(e)) # str() : quick fix
	finally:
		db.close()

	return user

# get all users
# return type (telegram) : 
#	true : telegram IDs only 
#	false : the whole table 
def get_users(telegram=True):
	if(telegram):
		columns = "tg_id"
	else:
		columns = "*"

	db = sqlite3.connect(DB_FILE)
	cursor = db.cursor()

	cursor.execute("SELECT " + columns + " FROM users")

	users = cursor.fetchall()
	db.close()

	return users

def delete_user(tg_id):
	success = True

	try:
		db = sqlite3.connect(DB_FILE)
		cursor = db.cursor()

		cursor.execute("DELETE FROM users WHERE tg_id=?", (tg_id,))

		db.commit()

	except Exception as e:
		db.rollback()
		success = False
	finally:
		db.close()

	return success

#
# BALANCES
def get_balance(tg_id):

	db = sqlite3.connect(DB_FILE)
	cursor = db.cursor()

	cursor.execute("SELECT balance, last_update FROM users WHERE tg_id=?", (tg_id,))

	balance = cursor.fetchone()
	db.close()

	# return a tuple of balance and last update date
	# return a tuple of None None if no result
	if(balance):
		return balance
	else:
		return None, None

def update_balance(tg_id):
	f_id, f_name = get_user(tg_id, eurest=True)
	money, date = franklin.get_money(f_id, f_name)

	db = sqlite3.connect(DB_FILE)
	cursor = db.cursor()

	cursor.execute("UPDATE users SET balance = ?, last_update = ? WHERE tg_id = ?",
		(money, date, tg_id))

	db.commit()
	db.close()

#
# Update all balances from all users
# called by crontab
def update_all_balances():
	users = get_users()
	for user in users:
		update_balance(user[0])

#
# NOTIFICATIONS
"""
Notification mode are stored as an integer but works as a boolean array 
Each boolean is associated with a notification type as following:
sold|menu|value
  0 |  0 |  0
  0 |  1 |  1
  1 |  0 |  2
  1 |  1 |  3
"""
def set_notification(tg_id, menu=False, sold=False):
	notification = 0
	if(sold == False and menu == False):
		notification = 0
	elif(sold == False and menu == True ):
		notification = 1
	elif(sold == True and menu == False):
		notification = 2
	elif(sold == True and menu == True):
		notification = 3
	else:
		printf("notification combination impossibru")

	# Insertion in database
	db = sqlite3.connect(DB_FILE)
	cursor = db.cursor()

	cursor.execute("UPDATE users SET notification = ? WHERE tg_id = ?",
		(notification, tg_id))

	db.commit()
	db.close()
	return 0

def get_notifications():
	db = sqlite3.connect(DB_FILE)
	cursor = db.cursor()

	cursor.execute("SELECT tg_id, notification FROM users")

	notification = cursor.fetchall()
	db.close()

	return notification

#
# Database creation
def db_init():
	try:
		db = sqlite3.connect(DB_FILE)
		cursor = db.cursor()

		# users table
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS users (
			tg_id INTEGER PRIMARY KEY UNIQUE, # Telegram ID
			eurest_id INTEGER,                # Eurest ID
			eurest_name TEXT,                 # Eurest name
			balance REAL,                     # current balance 
			last_update TEXT,                 # time of the balance's list update
			notification INTEGER)             # notification type 
		""")

		db.commit()

	except sqlite3.OperationalError:
		print('Erreur la table existe déjà')
	except Exception as e:
		print("Erreur : " + e)
		db.rollback()
	finally:
		db.close()


# Update all balances
# used for cron job
if __name__ == '__main__':
	update_all_balances()
