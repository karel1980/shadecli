import glob
import os
import ConfigParser
import requests
from time import sleep

class Shadecli:
	def __init__(self, dry_run=False):
		self.dry_run = dry_run
		self.config = self.read_config();

	def read_config(self):
		config = ConfigParser.RawConfigParser()
		p = os.path.expanduser('~/.shadecli/shadecli.ini')
		config.read(p)
		return config

	def set_const(self, shade_spec, value):
		shades = self.parse_shadespec(shade_spec)
		values = [ value ] * len(shades)
		self.plot(shades, values)

	def anim(self, speed):
		import numpy as np

		""" speed: value from 0 to 10. 10 """
		normalized_speed = np.clip(speed, 0, 10) / 10.0

		max_interval = 4
		min_interval = 0.5

		interval = max_interval - normalized_speed*(max_interval - min_interval)

		phase = 0
		while True:
			phase += 10
			self.sine(phase)
			sleep(interval)

	def sine(self, phase):
		import numpy as np
		shades = self.all_shades()
		inputs = np.linspace(0, np.pi*2, len(shades))
		inputs += phase / 360.0 * np.pi*2
		sin_values = np.sin(inputs)

		smin = self.config.getint('shades', 'minvalue')
		smax = self.config.getint('shades', 'maxvalue')
		shade_values = ((sin_values + 1) / 2) * (smax - smin) + smin

		self.plot(shades, shade_values)

	def all_shades(self):
		return list(range(self.get_numshades()))

	def get_numshades(self):
		return self.config.getint('shades', 'numshades')

	def plot(self, shades, values):
		user = self.config.get('openhab','user')
		password = self.config.get('openhab','pass')
		host = self.config.get('openhab','host')

		for i,value in zip(shades,values):
			url = "http://%s:8080/CMD?screen_%s=%s"%(host, i, value)
			if self.dry_run:
				print url
			else:
				requests.get(url, auth=(user, password))

	def parse_shadespec(self, specs):
		# TODO: warn if unknown shades are used
		shades = []
		for spec in specs:
			for part in spec.split(","):
				if "-" in part:
					a,b = part.split("-")
					shades += list(range(int(a),int(b)+1))
				else:
					shades.append(int(part))

		return set(shades)

