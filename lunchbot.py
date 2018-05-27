#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import json
import logging
import franklin
from dbconnector import *
from random import choice
from telegram import ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(level=logging.INFO,
	format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

handler = logging.FileHandler('lunchbot.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

# Needed constants
# Telegram bot token
TOKEN = ""

# start commmand's speech
welcome_message = """Bonjour, je m'appelle Franklin, je peux t'afficher ton \
solde restant et le menu du restaurant Eurest de la tour Franklin à la défense.\n
Pour t'enregistrer et consulter ton solde tu dois m'envoyer :
/register BadgeID Nom Prénom
Tu trouveras ton ID de badge, ton nom et ton prénom, en haut d'un ticket de \
caisse du restaurant, à coté de la mention 'Badge'.
Tu pourras alors me demander ton solde restant avec /money\nBon Appétit !\n
PS : En utilisant Franklin, tu accèptes que tes données personnelles soient \
stockées par le service :)
PPS : Si tu veux supprimer tes données personnelles, tu peux le faire avec \
/forgetme. Mais attention je ne pourrais plus t'indiquer ton solde !
"""

# Bot command handlers

def welcome(bot, update):
	update.message.reply_text(welcome_message, quote=False)

	log = "START : {"\
	+ str(update.message.from_user.id) + ", "\
	+ str(update.message.from_user.username) + "}"
	logger.info(log)

def hello(bot, update):
	sounds_path = "kaamelott-soundboard/sounds/"
	sounds_list = "sounds.json"

	sounds = json.load(open(sounds_path + sounds_list, 'r'))
	sound = choice(sounds)
	# ['character', 'episode', 'file', 'title']

	audio_file = sounds_path + sound['file']
	audio_title = sound['character'] + ' : ' + sound['title']

	bot.send_chat_action(chat_id=update.message.from_user.id, 
		action=ChatAction.UPLOAD_AUDIO, timeout=30)
	bot.send_voice(chat_id=update.message.from_user.id,
		voice=open(audio_file, 'rb'), caption=audio_title, timeout=30)

def display_menu(bot, update):
	update.message.reply_text(franklin.get_menu(), quote=False)

	log = "MENU : {"\
	+ str(update.message.from_user.id) + ", "\
	+ str(update.message.from_user.username) + "}"
	logger.info(log)

def display_balance(bot, update):
	money, date = get_balance(update.message.from_user.id)

	if(money != -1):
		message = "Solde disponible : " + str(money) + " €\n"\
		+ "Date de dernière mise à jour : " + str(date)
	else:
		message = "Désolé " + update.message.from_user.first_name\
		+ " mais tu n'es pas encore enregistré.e pour avoir ton solde. "\
		+ "Tu peux t'enregistrer avec la commande :\n/register BadgeID Nom Prénom"

	log = "GET BALANCE : {"\
	+ str(update.message.from_user.id) + ", "\
	+ str(update.message.from_user.username) + ", "\
	+ str(money) + ", "\
	+ str(date) + "}"
	logger.info(log)

	update.message.reply_text(message, quote=False)

# Split message into id and name
def badge_split(message):
	badge = message.split()
	if(len(badge) < 4):
		return 0, 0
	else:
		card = badge[1]
		name = ' '.join(badge[2:])
		return card,name

def force_update(bot, update):
	message = ""
	if(get_user(update.message.from_user.id)):
		message = "Ton solde a été mis à jour"
		update_balance(update.message.from_user.id)
	else:
		message = "Désolé " + update.message.from_user.first_name\
		+ " mais tu n'es pas encore enregistré.e pour avoir ton solde. "\
		+ "Tu peux t'enregistrer avec la commande :\n/register BadgeID Nom Prénom"

	update.message.reply_text(message, quote=False)

def register(bot, update):
	message = ""
	log = "REGISTER : {" + str(update.message.from_user.id) + ", "\
	+ str(update.message.from_user.username) + ", "

	if(get_user(update.message.from_user.id)):
		message = "Arrête " + update.message.from_user.first_name\
		+ ", tu t'es déjà enregistré.e pour avoir ton solde."
		log += "ERROR already exists"
	else:
			badge_id, badge_name = badge_split(update.message.text)
			log += str(badge_id) + ", " + str(badge_name) + ", "

			if(badge_id == 0 and badge_name == 0):
				message = "Enfin " + update.message.from_user.first_name\
				+ ", fait un effort ! Usage : /register IdBadge Nom Prénom"
				log += str(update.message.text)
			else:

				error = new_user(update.message.from_user.id, badge_id, badge_name)

				print(error)

				if(error == 0):
					message = "Bien joué " + update.message.from_user.first_name\
					+ " ! Tu es bien enregistré.e en base. Tu peux désormais "\
					+ " afficher ton solde avec la commande /money"
					log += "OK"
				elif(error == -1):
					message = "Ton identifiant de badge n'est pas correct.\n"\
					+ "Usage : /register IdBadge Nom Prénom"
					log += "ERROR"
				elif(error == -2):
					message = "L'utilisateur " + str(badge_name) + " n'existe pas\n"\
					+ "Usage : /register IdBadge Nom Prénom"
					log += "ERROR dont exist"

	log += "}"
	logger.info(log)

	update.message.reply_text(message, quote=False)

def deregister(bot, update):
	message = ""

	log = "DEREGISTER : {"\
	+ str(update.message.from_user.id)\
	+ ", " + str(update.message.from_user.username)

	if(delete_user(update.message.from_user.id)):
		log += " SUCCESS" 
		message = "Tes identifiants ont bien été supprimés de la base."
	else:
		message = "Impossible de supprimer ton compte. Peut-être que tu n'existes pas / plus"
		log += " FAIL" 

	log += "}"
	logger.info(log)

	update.message.reply_text(message, quote=False)

def unknown_command(bot, update):
	message = "Désolé " + update.message.from_user.first_name\
	+ ", je n'ai pas compris. Je réponds aux commandes suivantes : "\
	+ "/menu, /money, /register, /forgetme, /bonjour"
	update.message.reply_text(message, quote=False)

	log = "UNKOWN COMMAND : {" + update.message.from_user.id + " : "\
	+ update.message.text + "}"
	logger.info(log)

# bot error handler
def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
	logger.info('Starting Franklin')

	# Create database if not existent
	logger.info('Database initialization')
	db_init()

	# Create the EventHandler and pass it your bot's token.
	updater = Updater(TOKEN)

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", welcome))
	dp.add_handler(CommandHandler("bonjour", hello))
	dp.add_handler(CommandHandler("menu", display_menu))
	dp.add_handler(CommandHandler("money", display_balance))
	dp.add_handler(CommandHandler("update", force_update))
	dp.add_handler(CommandHandler("register", register))
	dp.add_handler(CommandHandler("forgetme", deregister))

	# unkown commands
	dp.add_handler(MessageHandler(Filters.all, unknown_command))
	
	# log all errors
	dp.add_error_handler(error)

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()
	logger.info('Stopping Franklin')

if __name__ == '__main__':
	main()
