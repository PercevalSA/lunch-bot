#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import re
import requests
from html.parser import HTMLParser

# Class to parse money
class MoneyParser(HTMLParser):

	def __init__(self, *args, **kwargs):
		self.solde = ""
		self.keep = False
		
		super(MoneyParser, self).__init__(*args, **kwargs)

	def handle_starttag(self, tag, attrs):
		if(tag == "div"):
			try:
				if(attrs[0][0] == "id"):
					if (attrs[0][1] == "soldedispo" or attrs[0][1] == "dateheure"):
						self.keep = True
			except IndexError:
				pass

		if(tag == "td" and self.keep):
			self.solde = self.solde + ": "

	def handle_endtag(self, tag):
		if(tag == "tr" and self.keep):
			self.solde = self.solde + "\n"
			self.keep = False

	def handle_data(self, data):
		if(self.keep):
			self.solde += data
			self.solde = re.sub('\s+', ' ', self.solde)

	def getSolde(self):
		return self.solde

def getMoney( card_id, name ):

	url = "https://www.e-chargement.com/identif_badge.Asp"
	payload = {'badge_div': '8776', 'badge_number': card_id, 'badge_nom': name}
	response = requests.post(url, data=payload)
	response.encoding = 'utf-8'
	
	if response.status_code == 200:
		return response.text
	else:
		return null

def parseMoney( text ):
	parser = MoneyParser()
	parser.feed(text)
	return parser.getSolde()
