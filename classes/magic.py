import random

class Spell:
	def __init__(self, name, cost, dmg, type):
		self.name = name
		self.cost = cost
		self.dmg = dmg
		self.type = type
	
	def get_spell_name(self):
		return self.name
	
	def generate_spell_damage(self):
		low = self.dmg - 5
		high = self.dmg + 5
		return random.randrange(low, high)

	