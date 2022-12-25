from requests import Session, get, post
from bs4 import BeautifulSoup as be
from re import search

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

		elif key == 'set':
			self.setting(param)

		elif key == 'del':
			self.delete(param)

		elif key == 'exit':
			return

		self.cli()

class Dedomil(Scrap):
	def __init__(self):
		self.sesi = Session()
		self.host = 'http://dedomil.net'
		self.config = {
			'id': 0
		}
		self.old_config = self.config.copy()
		self.last_search = {}

		super().__init__()

	def search(self, args):
		q = ' '.join(args)
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
			print(f'{x}. {y}')

	def check_config(self, key):
		config = self.config
		keys = config.keys()
		if key not in keys:
			return print('key not found:', key)

		return [config, keys]

	def setting(self, args):
		key, val = args
		config, keys = self.check_config(key)

		if type(config[key]) == int and not val.isdigit():
			return print('value type not match')

		config[key] = val

	def delete(self, args):
		key, = args
		config, keys = self.check_config(key)

		config[key] = self.old_config[key]