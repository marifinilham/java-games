from requests import Session, get, post
from bs4 import BeautifulSoup as be

class Dedomil:
	def __init__(self):
		self.sesi = Session()
		self.host = 'http://dedomil.net'

	def search(self, q):
		path = self.host+'/games/search'
		s = self.sesi.post(
			path,
			data = {
				'q': q
			}
		)

		if s.url == path:
			print('game not found')
			return

		web = be(s.text, 'html.parser')
		games = web.select('div[class=GMENU]')
		for game in games:
			print(game.a['href'], game.a.text)