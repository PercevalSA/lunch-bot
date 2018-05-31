#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import sqlite3
import franklin

# use absolute path for update cron
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
		cursor.execute("INSERT INTO users(tg_id, eurest_id, eurest_name) VALUES (?, ?, ?)",
			(TG_ID, EUREST_ID, eurest_name))
		cursor.execute("INSERT INTO balances(tg_id, balance) VALUES (?, ?)",
			(TG_ID, 0))
		db.commit()
		db.close()
		return 0

	else:
		print("wrong input : user does not exist\n")
		return -2


def get_user(tg_id, eurest=False):
	if(eurest):
		columns = "eurest_id, eurest_name"
	else:
		columns = "*"

	try:
		db = sqlite3.connect(DB_FILE)
		cursor = db.cursor()

		cursor.execute("SELECT " + columns + " FROM users WHERE tg_id=?", (tg_id,))

		user = cursor.fetchone()
	except Exception as e:
		print("Erreur : " + e)
	finally:
		db.close()

	return user


# get all users tg id
# if eurest = true give wole table 
def get_users(eurest=False):
	if(eurest):
		columns = "*"
	else:
		columns = "tg_id"

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
		cursor.execute("DELETE FROM balances WHERE tg_id=?", (tg_id,))

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

	if(get_user(tg_id)):
		cursor.execute("SELECT balance, last_update FROM balances WHERE tg_id=?", (tg_id,))
		balance = cursor.fetchone()
		db.close()
		return balance
	else:
		return -1,0


def update_balance(tg_id):
	f_id, f_name = get_user(tg_id, eurest=True)
	money, date = franklin.get_money(f_id, f_name)

	print(money)
	print(date)

	db = sqlite3.connect(DB_FILE)
	cursor = db.cursor()

	cursor.execute("UPDATE balances SET balance = ?, last_update = ? WHERE tg_id = ?",
		(money, date, tg_id))

	db.commit()
	db.close()


#
# Update all balances from all users
# called by crontab
def update_all_balances():
	users = get_users()
	for user in users:
		print(user)
		update_balance(user[0])


#
# Database creation
def db_init():
	try:
		db = sqlite3.connect(DB_FILE)
		cursor = db.cursor()

		# users table
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS users (
			tg_id INTEGER PRIMARY KEY UNIQUE,
			eurest_id INTEGER,
			eurest_name TEXT)
		""")

		# balances table
		# SQLite doesn't support foreign key by default
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS balances (
			tg_id INTEGER PRIMARY KEY UNIQUE,
			balance REAL,
			last_update TEXT)
		""")
		# last_update DATE)

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
