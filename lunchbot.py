#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""
Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging, shelve
import menu, money
from collections import defaultdict
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)

logger = logging.getLogger(__name__)

# Needed constants
# Telegram bot token
TOKEN= ""
# file to store users data
FILE = "users.dat"

welcome_message = """Bonjour, je m'appelle Franklin, je peux t'afficher ton solde
restant auprès du restaurant de la tour Franklin.\n
Pour t'enregistrer et consulter ton solde tu dois m'envoyer: /addme BadgeID Nom Prénom
Tu trouveras ton ID de badge en haut d'un ticket de caisse du restaurant
à coté de la mention 'Badge'. Tu pourras alors me demander ton solde restant avec /money\n
Bon Appétit!\n
PS: Si tu veux supprimer tes données personnelles, tu peux le faire avec
/forgetme. Mais attention je ne pourrais plus t'indiquer ton solde!"""

# Bot command handlers

def welcome(bot, update):
	update.message.reply_text(welcome_message, quote=False)

def display_menu(bot, update):
	response = menu.getMenu()
	if (response):
		output = menu.parseMenu(response)
		if(output != ""):
			update.message.reply_text("Le Menu du jour est : \n" + output, quote=False)
		else:
			update.message.reply_text("Il n'y a pas de menu pour aujourd'hui :'( \n", quote=False)

def display_sold(bot, update):
	with shelve.open(FILE) as users:
		if(str(update.message.from_user.id) in users):
			response = money.getMoney(users[str(update.message.from_user.id)], users[update.message.from_user.username])
			if(response):
				output = money.parseMoney(response)
				update.message.reply_text("Bonjour " + update.message.from_user.first_name + "\n" + output, quote=False)
		else:
			update.message.reply_text(update.message.from_user.first_name + " tu n'es pas encore enregistré pour avoir ton solde.\nTu peux t'enregistrer avec la commande /addme BadgeID Nom Prénom", quote=False)

	users.close()

def register_sold(bot, update):
	with shelve.open(FILE) as users:
		if(str(update.message.from_user.id) in users):
			update.message.reply_text("Arrête " + update.message.from_user.first_name + ", tu t'es déjà enregistré pour avoir ton solde.", quote=False)
		else:
			badge_id, badge_name = badge_split(update.message.text)
			if(badge_id == 0 and badge_name == 0):
				update.message.reply_text("Enfin " + update.message.from_user.first_name + ", fait un effort! Usage : /addme IdBadge Nom Prénom", quote=False)
			else:
				users[str(update.message.from_user.id)] = str(badge_id)
				users[update.message.from_user.username] = badge_name
				update.message.reply_text("Bien joué " + update.message.from_user.first_name + "! Tu es bien enregistré en base. Tu peux désormais demander ton solde avec la commande /money", quote=False)
			
	users.close()

def unregister_sold(bot, update):
	with shelve.open(FILE) as users:
		if(str(update.message.from_user.id) in users):
			del users[str(update.message.from_user.id)] 
			del users[update.message.from_user.username] 
			update.message.reply_text(update.message.from_user.first_name + " tes identifiants pour ton solde ont été supprimés de la base.", quote=False)
		else:
			update.message.reply_text("Aucune trace de " + update.message.from_user.first_name + " dans la base !", quote=False)
	users.close()

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
