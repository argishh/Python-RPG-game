import random
from classes.magic import Spell
from classes.inventory import Item

class bcolors:
	FAIL = '\033[91m'
	WARNING = '\033[93m'
	HEADER = '\033[95m'
	WHITE = '\033[97m'
	OKGREY = '\033[90m'
	OKGREEN = '\033[92m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

class Person:
	def __init__(self, name, hp, mp, atk, df, magic, items):
		self.name = name
		self.maxhp = hp
		self.hp = hp
		self.maxmp = mp
		self.mp = mp
		self.atkl = atk-10
		self.atkh = atk+10
		self.df = df
		self.magic = magic
		self.items = items
		self.actions = ["Attack", "Magic", "Items"]

	def generate_damage(self):
		return random.randrange(self.atkl, self.atkh)

	def take_damage(self, dmg):
		self.hp -= dmg
		if self.hp < 0:
			self.hp = 0
		return self.hp

	def heal(self, dmg):
		self.hp += dmg
		if self.hp > self.maxhp:
			self.hp = self.maxhp

	def get_hp(self):
		return self.hp
	
	def get_max_hp(self):
		return self.maxhp

	def get_mp(self):
		return self.mp
	
	def get_max_mp(self):
		return self.maxmp

	def reduce_mp(self, cost):
		self.mp -= cost
	
	def choose_action(self):
		i = 1
		print("\n\n" + bcolors.BOLD + " => " + self.name + bcolors.ENDC)
		print(bcolors.OKCYAN + bcolors.BOLD + "    Actions" + bcolors.ENDC)
		for item in self.actions:
			print("    ", str(i) + ":", item)
			i += 1
		
	def choose_magic(self):
		i = 1
		print(bcolors.OKBLUE + bcolors.BOLD + "\n    Magic" + bcolors.ENDC)
		for spell in self.magic:
			print("    ", str(i) + ":", spell.name, " (Cost:", spell.cost, ")")
			i += 1

	def choose_items(self):
		i = 1
		print(bcolors.OKBLUE + bcolors.BOLD + "\n    Items" + bcolors.ENDC)
		for item in self.items:
			print("    ", str(i) + ":", item["item"].name + ":", item["item"].description, bcolors.OKBLUE + bcolors.BOLD + "(x" + str(item["quantity"]) + ")" + bcolors.ENDC)
			i += 1

	def choose_target(self, enemies):
		i = 1
		print("\n"+bcolors.FAIL + bcolors.BOLD + "    Target: " + bcolors.ENDC)

		if len(enemies) == 1:
			return 0

		for enemy in enemies:
			if enemy.get_hp() != 0:
				print("        " + str(i) + "." + enemy.name)
				i += 1
		choice = int(input("        Enter Target: "))
		return choice-1

	def get_enemy_stats(self):
		hp_bar = ""
		bar_ticks = (self.hp / self.maxhp) * 100/2

		while bar_ticks > 0:
			hp_bar += "■"
			bar_ticks -= 1
		
		while len(hp_bar) < 50:
			hp_bar += " "

		hp_string = str(self.hp) + "/" + str(self.maxhp)
		current_hp = ""

		if len(hp_string) < 11:
			decresed = 11 - len(hp_string)
			while decresed > 0:
				current_hp += " "
				decresed -= 1
			current_hp += hp_string
		
		else:
			current_hp = hp_string

		print(bcolors.BOLD + self.name + "│ " + current_hp + "│" + bcolors.FAIL + hp_bar + bcolors.WHITE + bcolors.BOLD + "│" + bcolors.ENDC)


	def get_stats(self):
		hp_bar = ""
		bar_ticks = (self.hp / self.maxhp) * 100/4

		mp_bar = ""
		mp_ticks = (self.mp / self.maxmp) *100/10

		while bar_ticks > 0:
			hp_bar += "■"
			bar_ticks -= 1

		while len(hp_bar) <= 25:
			hp_bar += " "

		while mp_ticks > 0:
			mp_bar += "■"
			mp_ticks -= 1
		
		while len(mp_bar) < 10:
			mp_bar += " "

		hp_string = str(self.hp) + "/" + str(self.maxhp)
		current_hp = ""

		mp_string = str(self.mp) + "/" + str(self.maxmp)
		current_mp = ""

		if len(hp_string) < 9:
			decresed = 9 - len(hp_string)
			while decresed > 0:
				current_hp += " "
				decresed -= 1
			current_hp += hp_string
		
		else:
			current_hp = hp_string

		if len(mp_string) < 7:
			decresed = 7 - len(mp_string)
			while decresed > 0:
				current_mp += " "
				decresed -= 1
			current_mp += mp_string
		
		else:
			current_mp = mp_string

		# print("			_______________________		      ___________")
		print(bcolors.BOLD + self.name + "	│" + current_hp + "│" + bcolors.OKGREEN + hp_bar	+ bcolors.WHITE + bcolors.BOLD + "│" + current_mp + "│" + bcolors.OKBLUE+ mp_bar + bcolors.ENDC + "│")
		# print(bcolors.BOLD + self.name + "	│" +str(self.hp) + "/" + str(self.maxhp) + "│" + bcolors.OKGREEN + "■■■■■■■■■■■■■■■■■■■■■■■"	+ bcolors.WHITE + bcolors.BOLD + "│" + "    │" + str(self.mp) + "/" + str(self.maxmp) + "│" + bcolors.OKBLUE+ "■■■■■■■■■■■" + bcolors.ENDC + "│")
		
	def choose_enemy_spell(self):
	
		magic_choice = random.randrange(0, 3)
		spell = self.magic[magic_choice]
		magic_dmg = spell.generate_spell_damage()
		
		pct = self.hp // self.maxhp * 100

		if self.mp < spell.cost:
			return "attack", self.generate_damage()
	
		if spell.type == "white" and pct > 50:
			self.choose_enemy_spell()
		else:
			return spell, magic_dmg
