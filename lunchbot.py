#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

# TODO : migrate from shelve to SQLite3
import logging, shelve
import menu, money
from random import choice
from dikkenek import citations
from collections import defaultdict
from telegram.ext import Updater, CommandHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)

logger = logging.getLogger(__name__)

# Needed constants
# Telegram bot token
TOKEN= ""

# file to store users data, created with shelve : dict of users
# keys : telegram ID
# values : ['ID', 'Name Surname']
FILE = "users.dat"

# text for start commmand
welcome_message = """Bonjour, je m'appelle Franklin, je peux t'afficher ton \
solde restant auprès du restaurant de la tour Franklin.\n
Pour t'enregistrer et consulter ton solde tu dois m'envoyer:
/addme BadgeID Nom Prénom
Tu trouveras ton ID de badge, ton nom et ton prénom, en haut d'un ticket de \
caisse du restaurant, à coté de la mention 'Badge'.
Tu pourras alors me demander ton solde restant avec /money\nBon Appétit!\n
PS: Si tu veux supprimer tes données personnelles, tu peux le faire avec
/forgetme. Mais attention je ne pourrais plus t'indiquer ton solde!"""

# Bot command handlers

def welcome(bot, update):
	update.message.reply_text(welcome_message, quote=False)

def hello(bot, update):
	update.message.reply_text(text=choice(citations), quote=False)

def display_menu(bot, update):
	message = ""
	response = menu.getMenu()

	if (response):
		output = menu.parseMenu(response)
		if(output != ""):
			message = "Le Menu du jour est : \n" + output
		else:
			message = "Il n'y a pas de menu pour aujourd'hui :'( \n"

	update.message.reply_text(message, quote=False)

def display_sold(bot, update):
	message = ""

	with shelve.open(FILE) as users:
		if(str(update.message.from_user.id) in users):
			response = money.getMoney(users[str(update.message.from_user.id)],
				users[update.message.from_user.username])

			if(response):
				output = str(money.parseMoney(response))
				message = "Bonjour " + update.message.from_user.first_name\
				+ "\n" + output
			else:
				message = "Désolé " + update.message.from_user.first_name\
				+ ", impossible de récupérer ton solde..."
		else:
			message = update.message.from_user.first_name\
			+ " tu n'es pas encore enregistré pour avoir ton solde.\n"\
			+ "Tu peux t'enregistrer avec la commande /addme BadgeID Nom Prénom"

	users.close()
	update.message.reply_text(message, quote=False)


def register_sold(bot, update):
	message = ""

	with shelve.open(FILE) as users:
		if(str(update.message.from_user.id) in users):
			message = "Arrête " + update.message.from_user.first_name\
			+ ", tu t'es déjà enregistré pour avoir ton solde."
		else:
			badge_id, badge_name = badge_split(update.message.text)

			if(badge_id == 0 and badge_name == 0):
				message = "Enfin " + update.message.from_user.first_name\
				+ ", fait un effort! Usage : /addme IdBadge Nom Prénom"
			else:
				users[str(update.message.from_user.id)] = str(badge_id)
				users[update.message.from_user.username] = badge_name
				message = "Bien joué " + update.message.from_user.first_name\
				+ "! Tu es bien enregistré en base. Tu peux désormais demander"\
				+ " ton solde avec la commande /money"

	users.close()
	update.message.reply_text(message, quote=False)

def unregister_sold(bot, update):
	message = ""

	with shelve.open(FILE) as users:
		if(str(update.message.from_user.id) in users):
			del users[str(update.message.from_user.id)] 
			del users[update.message.from_user.username] 
			message = update.message.from_user.first_name\
			+ " tes identifiants pour ton solde ont été supprimés de la base."
		else:
			message = "Aucune trace de " + update.message.from_user.first_name\
			+ " dans la base !"

	users.close()
	update.message.reply_text(message, quote=False)

# bot error handler
def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

# Split message into id and name
def badge_split(message):
	badge = message.split()
	if(len(badge) < 4):
		return 0, 0
	else:
		card = badge[1]
		name = ' '.join(badge[2:])
		return card,name

def main():
	# Create the EventHandler and pass it your bot's token.
	updater = Updater(TOKEN)

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", welcome))
	dp.add_handler(CommandHandler("bonjour", hello))
	dp.add_handler(CommandHandler("menu", display_menu))
	dp.add_handler(CommandHandler("money", display_sold))
	dp.add_handler(CommandHandler("addme", register_sold))
	dp.add_handler(CommandHandler("forgetme", unregister_sold))

	# log all errors
	dp.add_error_handler(error)

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	main()
