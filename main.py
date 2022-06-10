from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Create Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 50, 1200, "black")
quake = Spell("Quake", 40, 1000, "black")

# Create White Magic
cure = Spell("Cure", 12, 120, "White")
cura = Spell("Cura", 18, 180, "white")
curaga = Spell("Curaga", 18, 800, "white")

# Creating Inventory Items
potion = Item("Potion", "potion", "Heals 100 HP", 100)
hipotion = Item("Hi-Potion", "potion", "Heals 500 HP", 500)
superpotion = Item("Super-Potion", "potion", "Heals 1000 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully Restores HP/MP of 1 party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully Restores party's HP/MP", 9999)
molly = Item("Molly", "attack", "Deals 450 damage", 450)
grenade = Item("Grenade", "attack", "Deals 800 damage", 800)
lavabomb = Item("Lava-Bomb", "attack", "Deals 1200 damage", 1200)

# Spells and items
player_spells =  [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{"item": potion, "quantity" : 8},
				{"item": hipotion, "quantity" : 6},
				{"item": superpotion, "quantity" : 3},
				{"item": elixer, "quantity" : 3},
				{"item": hielixer, "quantity" : 1},
				{"item": molly, "quantity" : 2},
				{"item": grenade, "quantity" : 3},
				{"item": lavabomb, "quantity": 1}]

enemy_spells = [fire, meteor, curaga]

# Instantiate People
player1 = Person("Grimheir", 3000, 600, 300, 34, player_spells, player_items)
player2 = Person("JeoFrost", 8000, 150, 600, 34, player_spells, player_items)
player3 = Person("Lizblaze", 4200, 180, 380, 34, player_spells, player_items)
player4 = Person("Dremthos", 4100, 200, 390, 34, player_spells, player_items)

enemy1 = Person("Imp Zeak", 1250, 500, 560, 325, enemy_spells, [])
enemy2 = Person("Eskatron", 63000, 5000, 720, 325, enemy_spells, [])
enemy3 = Person("Imp Eein", 1250, 500, 560, 325, enemy_spells, [])
enemy4 = Person("Imp Dink", 1250, 500, 560, 325, enemy_spells, [])

players = [player1, player2, player3, player4]
enemies = [enemy1, enemy2, enemy3, enemy4]

running = True
i = 0

print("\nMessage from HQ:" + bcolors.FAIL + bcolors.BOLD + "\nALERT: Base Under Enemy Attack\n" + bcolors.ENDC)

while running:
	# try:
	print( bcolors.BOLD + "\nStats:\n" +  bcolors.ENDC)
	white = bcolors.WHITE
	header = bcolors.HEADER +  bcolors.BOLD
	print(header + "NAME		"+ white + "│" + header +" HP			" + white + "     	     │" + header + " MP"+  bcolors.ENDC)
	print("────────────────┼────────────────────────────────────┼───────────────────")
	for player in players:
		player.get_stats()
	print("────────────────┴────────────────────────────────────┴───────────────────")
	
	print( bcolors.BOLD + "\nEnemy:" +  bcolors.ENDC)
	for enemy in enemies:
		enemy.get_enemy_stats()

	for player in players:

		player.choose_action()
		choice = input("    Choose Action: ")
		index = int(choice)-1

		if index == 0:
			dmg = player.generate_damage()
			enemy = player.choose_target(enemies)
			enemies[enemy].take_damage(dmg)
			
			print("\nYou Attacked", enemies[enemy].name.replace(" ", ""), "for", dmg, "points of damage")

			if enemies[enemy].get_hp() == 0:
				print(bcolors.OKGREEN + bcolors.BOLD + str(enemies[enemy].name).replace(" ", "") + " Defeated!" + bcolors.ENDC)
				del enemies[enemy]
		elif index == 1:
			player.choose_magic()
			magic_choice = int(input("Choose Magic: ")) -1 

			if magic_choice == -1:
				continue

			spell = player.magic[magic_choice]
			magic_dmg = spell.generate_spell_damage()

			current_mp = player.get_mp()

			if spell.cost > current_mp:
				print(bcolors.FAIL + "\nNOT ENOUGH MP\n" + bcolors.ENDC)
				continue

			player.reduce_mp(spell.cost)
			if spell.type == "white":
				player.heal(magic_dmg)
				print(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(magic_dmg) + "HP" + bcolors.ENDC)
			
			elif spell.type == "black":
				enemy = player.choose_target(enemies)
				enemies[enemy].take_damage(magic_dmg)
				print(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg) + " points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
				
				if enemies[enemy].get_hp() == 0:
					print(bcolors.OKGREEN + bcolors.BOLD + str(enemies[enemy].name).replace(" ", "") + " Defeated!" + bcolors.ENDC)
					del enemies[enemy]
				
		elif index == 2:
			player.choose_items()
			item_choice = int(input("Choose Item: ")) - 1

			if item_choice == -1:
				continue

			item = player.items[item_choice]["item"]
			player.items[item_choice]["quantity"] -= 1

			if item.type == "potion":
				player.heal(item.prop)
				print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop), "HP" + bcolors.ENDC)

			elif item.type == "elixer":

				if item == "MegaElixer":
					for i in players:
						i.hp = i.maxhp
						i.mp = i.maxmp
					print(bcolors.OKGREEN + "\nTeam HP/MP restored" + bcolors.ENDC)
				else:
					player.hp = player.maxhp
					player.mp = player.maxmp
					print(bcolors.OKGREEN + "\nPlayer HP/MP restored" + bcolors.ENDC)
			
			elif item.type == "attack":
				enemy = player.choose_target(enemies)
				enemies[enemy].take_damage(item.prop)

				print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop), " points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)
				
				if enemies[enemy].get_hp() == 0:
					print(bcolors.OKGREEN + bcolors.BOLD + str(enemies[enemy].name).replace(" ", "") + " Defeated!" + bcolors.ENDC)
					del enemies[enemy]
	
	# Check if battle is over
	defeated_enemies = 0
	defeated_players = 0

	for enemy in enemies:
		if enemy.get_hp() == 0:
			defeated_enemies += 1
	
	for player in players:
		if player.get_hp() == 0:
			defeated_players += 1
	
	# Check if player won
	if defeated_enemies == 4:
		print(bcolors.OKGREEN + bcolors.BOLD + "All Enemies Defeated! You WON!" + bcolors.ENDC)
		running = False
	
	# Check if enemy won
	if defeated_players == 4:
		print(bcolors.FAIL + bcolors.BOLD + "Your ENEMIES have Defeated You..." + bcolors.ENDC)
		running = False
	
	print("\n")
	# Enemy attack phase
	for enemy in enemies:
		# Choose attack type
		enemy_choice = random.randrange(0, 2)

		if enemy_choice == 0:
			# Choose Target 
			target = random.randrange(0,len(players))
			enemy_dmg = enemy.generate_damage()
			
			players[target].take_damage(enemy_dmg)
			print(bcolors.FAIL + bcolors.BOLD + enemy.name.replace(" ", ""), "attacks " + players[target].name + " for " + str(enemy_dmg) + bcolors.ENDC)
		
		elif enemy_choice == 1:
			spell, magic_dmg = enemy.choose_enemy_spell()
			enemy.reduce_mp(spell.cost)
			
			if spell.type == "white":
				enemy.heal(magic_dmg)
				print(bcolors.OKGREY + bcolors.BOLD + spell.name + " heals " + enemy.name + " for " + str(magic_dmg) + "HP" + bcolors.ENDC)
			
			elif spell.type == "black":
				target = random.randrange(0,len(players))
				players[target].take_damage(magic_dmg)
				print(bcolors.FAIL + bcolors.BOLD + enemy.name.replace(" ", "") + "'s " + spell.name + " attacks " + players[target].name + " for " + str(magic_dmg) + bcolors.ENDC)
				
				if players[target].get_hp() == 0:
					print("\n" + bcolors.FAIL + bcolors.BOLD + "Alert: " + players[target].name + " Died!" + bcolors.ENDC)
					del players[target]

	# except Exception as e:
	# 	# print(e)
	# 	print("\nInvalid Action, Please try Again!\n")
