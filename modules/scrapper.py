from requests import Session, get, post
from bs4 import BeautifulSoup as be
from re import search
from .func import space

version = '1.0.4'

class Scrap:
	def __init__(self):
		self.cli()

	def cli(self):
		ps1 = f'[java-games-{version}]'
		if idgame := self.config['id']:
			ps1 += f'[{idgame}]'
		ps1 += ' '

		prompt = input(ps1).split()
		if len(prompt) == 0:
			return self.cli()

		key = prompt[0]
		param = prompt[1:]

		if key == 'search':
			self.search(param)

		elif key == 'last':
			self.get_last()

		elif key in ('set', 'del'):
			self.configure(key, param)

		elif key in ('fetch') and self.config['id']:
			self.fetch(param)

		elif key == 'exit':
			return

		self.cli()

class Dedomil(Scrap):
	def __init__(self):
		self.sesi = Session()
		self.host = 'http://dedomil.net'
		self.config = {
			'id': 0,
			'res': 0
		}
		self.old_config = self.config.copy()
		self.last_search = {}

		super().__init__()

	@staticmethod
	def retrieve(resp):
		web = be(resp.text, 'html.parser')
		return web.select('div[class=GMENU]')

	def search(self, args):
		q = ' '.join(args)
		path = self.host+'/games/search'
		r = self.sesi.post(
			path,
			data = {
				'q': q
			}
		)

		if r.url == path:
			print('game not found')
			return

		games = self.retrieve(r)
		self.last_search = {}
		for game in games:
			game_id = search('\d+', game.a['href']).group()
			game_name = game.a.text
			self.last_search[game_id] = game_name
			print(f'{game_id}. {game_name}')

	def get_last(self):
		if len(self.last_search) == 0:
			return print('empty')

		for x,y in self.last_search.items():
			print(f'\u001b[4m{x}.{space}{y}\033[0m')

	def configure(self, which, args):
		key = args[0]
		config = self.config
		keys = config.keys()
		if key not in keys:
			return print('key not found:', key)
		
		if which == 'set':
			val = args[1]
			if type(config[key]) == int and not val.isdigit():
				return print('value type not match')

			config[key] = val
		
		elif which == 'del':
			config[key] = self.old_config[key]

	def fetch(self, args):
		which = 'all' if len(args) == 0 else args[0]

		if which == 'all':
			print('semua')

		elif which == 'res':
			self.screens()

		elif which == 'model':
			screen = 'all' if len(args) != 2 else args[1]
			screens = self.screens(1)
			


	def screens(self, ret=0):
		r = self.sesi.get(f'{self.host}/games/{self.config["id"]}/screens')
		if r.status_code == 404:
			return print('game not found')

		resols = self.retrieve(r)
		available = {}
		for res in resols:
			a = res.a
			id_res = a['href'].split('/')[-1]
			available[id_res] = a.text

		if ret:
			return available

		for x,y in available.items():
			print(f'\u001b[4m{x}.{space(x)}{y}\033[0m')