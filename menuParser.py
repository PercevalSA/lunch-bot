#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import requests
from html.parser import HTMLParser

menu = ""

# Class to parse menu
class MyHTMLParser(HTMLParser):

	def __init__(self, *args, **kwargs):
		global menu
		self.plat = False
		self.prix = False
		menu = ""

		super(MyHTMLParser, self).__init__(*args, **kwargs)

	def handle_starttag(self, tag, attrs):
		global menu

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
				menu = menu +"\n## Entrées ##\n"
			if(attrs[0][1] == "collapse2"):
				menu = menu +"\n## Plats du jour ##\n"
			if(attrs[0][1] == "collapse10"):
				menu = menu +"\n## Plats à thème ##\n"
			if(attrs[0][1] == "collapse27"):
				menu = menu +"\n## Grillades viande ##\n"
			if(attrs[0][1] == "collapse11"):
				menu = menu +"\n## Légumes ##\n"
			if(attrs[0][1] == "collapse22"):
				menu = menu +"\n## Desserts ##\n"

	def handle_endtag(self, tag):
		if(tag == "span"):
			self.plat = False
			self.prix = False	

	def handle_data(self, data):
		global menu

		if(self.plat):
			menu = menu + " * " + ' '.join(data.split())
		if(self.prix):
			menu = menu + " : " + ' '.join(data.split()) + "\n"


def getMenu( day="Today" ):

	if (day == "Today"):
		url = "http://www.aspp.fr/app.php/restaurants/28"

		response = requests.get(url)

		if response.status_code == 200:
			return response.text
		else:
			return null

def parseMenu( text ):
	parser = MyHTMLParser()
	parser.feed(text)
	return menu