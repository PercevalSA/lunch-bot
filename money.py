#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import requests
from bs4 import BeautifulSoup


def get_money(card_id, name):

	url = "https://www.e-chargement.com/identif_badge.Asp"
	payload = {'badge_div': '8776', 'badge_number': card_id, 'badge_nom': name}
	response = requests.post(url, data=payload)
	response.encoding = 'utf-8'

	if response.status_code == 200:
		soup = BeautifulSoup(response.text, 'html.parser')
		infos = soup.find_all("td", { "class" : "bold" }) 
		money = infos[1].text
		date = infos[2].text

		return  "Solde disponible sur votre compte : " + money\
		+ "\nDate et heure à laquelle est calculé votre solde : " + date
	else:
		return null
