from requests import Session, get, post
from bs4 import BeautifulSoup as be
from re import search
from .func import space, phead

version = '1.2.1'

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
			'screens': {}
		}
		self.old_config = self.config.copy()
		self.last_search = {}

		super().__init__()

	@staticmethod
	def retrieve(resp, cls):
		web = be(resp.text, 'html.parser')
		return web.select(f'div[class={cls}]')

	@staticmethod
	def dump(var, name):
		phead('id', name)
		for x,y in var.items():
			print(f'\u001b[4m{x}.  {space(x)}{y}\033[0m')

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

		games = self.retrieve(r, 'GMENU')
		self.last_search = {}
		phead('id', 'game')
		for game in games:
			game_id = search('\d+', game.a['href']).group()
			game_name = game.a.text
			self.last_search[game_id] = game_name
			print(f'\u001b[4m{game_id}.  {space(game_id)}{game_name}\033[0m')

	def get_last(self):
		if len(self.last_search) == 0:
			return print('empty')

		self.dump(self.last_search, 'game')

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
			self.models()

	def screens(self, ret=0):
		if available := self.config['screens']:
			return self.dump(available, 'resolution')

		r = self.sesi.get(f'{self.host}/games/{self.config["id"]}/screens')
		if r.status_code == 404:
			return print('game not found')

		resols = self.retrieve(r, 'GMENU')
		available = {}
		for res in resols:
			a = res.a
			id_res = a['href'].split('/')[-1]
			available[id_res] = a.text

		self.config['screens'] = available.copy()

		if ret:
			return available

		self.dump(available, 'resolution')

	def models(self):
		id_game = self.config['id']
		screens = self.screens(1)
		if screen := self.config['screen']:
			screens = screens[screen]

		for x,y in screens:
			r = self.sesi.get(f'{host}/games/{id_game}/screen/{x}')
			print