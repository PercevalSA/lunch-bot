#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""
Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import settings
import logging
import menuParser as mp
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO)

logger = logging.getLogger(__name__)

# Bot command handlers
def start(bot, update):
	if(settings.LAUNCHED):
		update.message.reply_text('Je suis déjà à votre service !')
	else:
		update.message.reply_text('Bonjour, je vous donnerai le menu lorsque vous me le demanderez.')
		settings.LAUNCHED = True

def stop(bot, update):
	if(settings.LAUNCHED):
		update.message.reply_text("D'accord, je me tais")
		settings.LAUNCHED = False
	else:
		update.message.reply_text("Mais je n'ai rien fait !!!")

def help(bot, update):
	update.message.reply_text('/menu: affiche le menu du jour')

def menu(bot, update):
	if(settings.LAUNCHED):
		menu = mp.getMenu()
		if (menu):
			output = mp.parseMenu(menu)
			if(output != ""):
				update.message.reply_text("Le Menu du jour est : \n" + output, quote=False)
			else:
				update.message.reply_text("Il n'y a pas de menu pour aujourd'hui :'( \n", quote=False)

# bot error handler
def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
	# Create the EventHandler and pass it your bot's token.
	updater = Updater(settings.TOKEN)

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("stop", stop))
	dp.add_handler(CommandHandler("help", help))
	dp.add_handler(CommandHandler("menu", menu))

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