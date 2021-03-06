#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Inteface with Eurest website

import datetime, requests
from bs4 import BeautifulSoup

def check_user(card_id, name):
	url = "https://www.e-chargement.com/identif_badge.asp"
	payload = {'badge_div': '8776', 'badge_number': card_id, 'badge_nom': name}
	response = requests.post(url, data=payload)
	response.encoding = 'utf-8'

	if "err" in response.url :
		return False
	else:
		return True

def get_money(card_id, name):

	url = "https://www.e-chargement.com/identif_badge.asp"
	payload = {'badge_div': '8776', 'badge_number': card_id, 'badge_nom': name}
	response = requests.post(url, data=payload)
	response.encoding = 'utf-8'

	if response.status_code == 200:
		soup = BeautifulSoup(response.text, 'html.parser')
		infos = soup.find_all("td", { "class" : "bold" }) 
		money = float(infos[1].text[:-3].replace(",",".")) # -3 to delete '€'
		date = infos[2].text

		return money, date
	else:
		return null


def get_menu():

	# needed urls
	cookie_url  = "http://www.tourfranklin.eurest.fr"
	menu_url    = "http://www.tourfranklin.eurest.fr/ajaxWidgetMenu.aspx"
	# list of restaurants : tuple (name, id)
	restaurants = [('Charpentier', 1983), ('Musée', 1985)]

	# Get a legit Cookie
	cookie_response = requests.head(cookie_url)
	cookie_response.encoding = 'utf-8'
	cookie_parts = cookie_response.headers['Set-Cookie'].split(' ')
	cookie = ' '.join([cookie_parts[0], cookie_parts[3], cookie_parts[9]])

	# Forge Requests
	now = datetime.datetime.now()
	headers = {'cookie': cookie}

	# Get menus
	menus = ""
	for restaurant in restaurants:
		payload = {'day': now.strftime("%Y-%m-%d"), 'divId': '12108', 
		'spsId': restaurant[1], 'widgetMenu': 'false'}

		response = requests.post(menu_url, headers=headers, data=payload)
		response.encoding = 'utf-8'

		# Parsing
		if response.status_code == 200:
			soup = BeautifulSoup(response.text, 'html.parser')
			menu = soup.get_text("\n", strip=True)
			menus += restaurant[0] + ' : ' + menu[27:] + '\n\n'

		else:
			menus += "Désolé, je n'arrive pas à récupérer le menu du "\
			+ restaurant[0] +". Tu peux aller vérifier par toi même : "\
			+ cookie_url + '\n\n'

	return menus
