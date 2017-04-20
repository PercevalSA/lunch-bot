#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import requests
from html.parser import HTMLParser

# Class to parse menu
class MenuParser(HTMLParser):

	def __init__(self, *args, **kwargs):
		self.menu = ""
		self.plat = False
		self.prix = False

		super(MenuParser, self).__init__(*args, **kwargs)

	def handle_starttag(self, tag, attrs):

		if(tag == "span"):
			try:
				if(attrs[0][1] == "platNom"):
					self.plat = True
			
				if(attrs[1][1] == "platPrix"):
					self.prix = True
			except IndexError:
				pass

		if(tag == "div" and attrs[0][0] == "id"):
			if(attrs[0][1] == "collapse1"):
				self.menu = self.menu +"\n## Entrées ##\n"
			if(attrs[0][1] == "collapse2"):
				self.menu = self.menu +"\n## Plats du jour ##\n"
			if(attrs[0][1] == "collapse10"):
				self.menu = self.menu +"\n## Plats à thème ##\n"
			if(attrs[0][1] == "collapse27"):
				self.menu = self.menu +"\n## Grillades viande ##\n"
			if(attrs[0][1] == "collapse11"):
				self.menu = self.menu +"\n## Légumes ##\n"
			if(attrs[0][1] == "collapse22"):
				self.menu = self.menu +"\n## Desserts ##\n"

	def handle_endtag(self, tag):
		if(tag == "span"):
			self.plat = False
			self.prix = False	

	def handle_data(self, data):

		if(self.plat):
			self.menu = self.menu + " * " + ' '.join(data.split())
		if(self.prix):
			self.menu = self.menu + " : " + ' '.join(data.split()) + "\n"

	def getMenu(self):
		return self.menu


def getMenu( day="Today" ):
	# TO DO : implement other days of the week
	if (day == "Today"):
		url = "http://www.aspp.fr/app.php/restaurants/28"

		response = requests.get(url)
		response.encoding = 'utf-8'

		if response.status_code == 200:
			return response.text
		else:
			return null

def parseMenu( text ):
	parser = MenuParser()
	parser.feed(text)
	return parser.getMenu()
