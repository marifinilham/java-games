from modules.scrapper import Dedomil

version = '1.0.0'

class Main:
	def __init__(self):
		self.cli()

	def cli(self):
		prompt = input(f'[java-games-{version}] ').split()
		if len(prompt) == 0:
			return self.cli()

		key = prompt[0]
		param = ' '.join(prompt[1:])

		if key == 'search':
			dedomil.search(param)

		elif key == 'exit':
			return

		self.cli()

dedomil = Dedomil()
Main()