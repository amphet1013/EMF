#!/usr/bin/python3

import sys
from localpaths import rootpath

###

emf_path = rootpath / 'EMF/EMF'
tactics_path = emf_path / 'common/combat_tactics/emf_combat_tactics_codegen.txt'
call_to_glory_tactics_path = emf_path / 'common/combat_tactics/emf_call_to_glory_combat_tactics_codegen.txt'
localization_path = emf_path / 'localisation/1_emf_combat_tactics_codegen.csv'

###

class CombatTacticLevel:
	def __init__(self,prefix,name_prefix,sprite_offset,mtth_score_prefix,global_offensive_modifier,global_defensive_modifier,requires_flank_leader=True,has_tech_mtth_score_modifier=False):
		self.prefix = prefix
		self.name_prefix = name_prefix
		self.sprite_offset = sprite_offset
		self.mtth_score_prefix = mtth_score_prefix
		self.global_offensive_modifier = global_offensive_modifier
		self.global_defensive_modifier = global_defensive_modifier
		self.requires_flank_leader = requires_flank_leader
		self.has_tech_mtth_score_modifier = has_tech_mtth_score_modifier

combat_tactics_levels = [
	CombatTacticLevel("good","Devastating",-10,"good",0.25,0.25),
	CombatTacticLevel("","",0,"ok",0,0),
	CombatTacticLevel("bad","Failed",10,"bad",-0.25,-0.25,False,True)
]

glorious_combat_tactic_level = CombatTacticLevel("glorious","Glorious",-10,"good",0.5,0.5)

###

f = open('./combat_tactics.csv')
generic_tactics_data_array = [line.strip().split(',') for line in f]
f.close()

f = open('./cultural_tactics.csv')
cultural_tactics_data_array = [line.strip().split(',') for line in f]
f.close()

f = open('./call_to_glory_combat_tactics.csv')
special_call_to_glory_tactics_data_array = [line.strip().split(',') for line in f]
f.close()

replacement_tactics_list = {}
replacement_glorious_tactics_list = {}
for i in range(1,len(generic_tactics_data_array[0])):
	replacement_tactics_list[generic_tactics_data_array[0][i]] = []
	replacement_glorious_tactics_list[generic_tactics_data_array[0][i]] = []
for i in range(1,len(cultural_tactics_data_array[0])):
	replacement_tactics_list[cultural_tactics_data_array[1][i]].append(cultural_tactics_data_array[0][i])
for i in range(1,len(special_call_to_glory_tactics_data_array[0])):
	replacement_glorious_tactics_list[special_call_to_glory_tactics_data_array[1][i]].append(special_call_to_glory_tactics_data_array[0][i])

###

def print_header(f, spec=None, call_to_glory=False):
	if spec:
		print('# -*- {} -*-'.format(spec), file=f)
		print('''
################################################################################
# WARNING: Do NOT modify this file manually!
#
# This file is code-generated and any manual changes will be overwritten.
#
# Generated by src/combat_tactics_gen.py
################################################################################

### At the moment we have a pretty basic icon system for combat tactics showing
### the uniticon which has the biggest bonus value in the tactic.
### This is the sprite number for each unit:
### Good 	 1=LI	 2=HI	 3=PIKE	 4=LC	 5=KNIGHTS	 6=ARCHERS	 7=HORSE ARCH.	 8=GALLEY	 9=ELEPHANT	10=CAMEL
### Neutral 11=LI	12=HI	13=PIKE	14=LC	15=KNIGHTS	16=ARCHERS	17=HORSE ARCH.	18=GALLEY	19=ELEPHANT	20=CAMEL
### Bad 	21=LI	22=HI	23=PIKE	24=LC	25=KNIGHTS	26=ARCHERS	27=HORSE ARCH.	28=GALLEY	29=ELEPHANT	30=CAMEL
''', file=f)
		if call_to_glory:
			print('''# Tactics based off the following Lodge retinues info:
# Norse Lodge: light_infantry + heavy_infantry 				150 + 100
# Tengri Lodge: light_cavalry + horse_archers 				100 + 150
# Slavic Lodge: light_infantry + light_cavalry 				200 + 50
# Baltic Lodge: light_infantry + heavy_infantry + archers 	100 + 100 + 50
# Finnish Lodge: light_infantry + archers 					100 + 150
# West-African Lodge: light_infantry + pikemen 				150 + 100
# Zunist Lodge: pikemen + archers 							150 + 100
# Bon Lodge: light_infantry + light_cavalry + archers 		100 + 50 + 100
# Hellenic Lodge: pikemen + heavy infantry 					200 + 50
# Aztec Lodge: light_infantry + heavy_infantry 				100 + 150
#
# Glorious tactic system:
# Vanilla:
# - call_to_glory modifier on commander unlocks glorious_countercharge_tactic that boosts all troop types' offense.
# - call_to_glory modifier on commander unlocks a different, unique tactic based on which warrior lodge of which the commander is a member. The special tactic in question tends to boost the troop types they get as event troops from the Call to Glory interaction.
#   - Winter's Maw Tactic - Norse (heavy infantry)
#   - Wolf's Howling Tactic - Tengri (horse archers)
#   - Slavic Last Stand Tactic - Slavic (light infantry)
#   - Baltic Last Stand Tactic - Baltic (heavy infantry)
#   - Elk's Lament Tactic - Finnish (archers)
#   - Bull Horns Tactic - West-africans (pikemen)
#   - Lightburst Tactic - Zunists (archers)
#   - Balanced Charge Tactic - Bon (light infantry/cavalry)
#   - Quincunx Tactic - Hellenic (pikemen)
#
# EMF:
# - call_to_glory modifier on commander unlocks "glorious" versions of the 8 default tactics. Glorious versions of the default tactics are similar to "good" versions of those tactics, but give a +50% baseline instead of a +25% and aren't locked by culture; they are locked away from certain lodges because...
# - Depending on which warrior lodge the character belongs to, one of the 8 default "glorious" tactics is replaced by one specific to the lodge. The lodge-specific tactic gives an additional +50% in total to stats based on the troop types gotten through the Call to Glory interaction (the same way cultural combat tactics upgrade default, non-glorious combat tactics).
#   - Winter's Maw Tactic - Norse (upgraded Advance)
#   - Wolf's Howling Tactic - Tengri (upgraded Swarm)
#   - Lightning Raid Tactic - Slavic (upgraded Raid)
#   - Last Stand Tactic - Baltic (upgraded Advance)
#   - Elk's Lament Tactic - Finnish (upgraded Volley)
#   - Bull Horns Tactic - West-Africans (upgraded Harass)
#   - Missile Swarm Tactic - East-Africans (upgraded Harass)
#   - Lightburst Tactic - Zunists (upgraded Volley)
#   - Lightning Raid Tactic - Bon (upgraded Raid)
#   - Quincunx Tactic - Hellenic (upgraded Stand Fast)
#	- Water Fire Tactice - Aztec (upgraded Advance)''', file=f)

def main():
	with tactics_path.open('w', encoding='cp1252', newline='\n') as f:
		print_header(f, 'ck2.combat_tactics')
		print_generic_combat_tactics(f)
		print_cultural_combat_tactics(f)
	
	with call_to_glory_tactics_path.open('w', encoding='cp1252', newline='\n') as f:
		print_header(f, 'ck2.combat_tactics', True)
		print_call_to_glory_combat_tactics(f)
	
	with localization_path.open('w', encoding='cp1252', newline='\n') as f:
		print_localizations(f)
	return 0

def print_generic_combat_tactics(f):
	print('''
##########################################################################
# Generic Tactics
##########################################################################''', file=f)
	for i in range(1,len(generic_tactics_data_array[0])):
		tactic_name = generic_tactics_data_array[0][i]
		tactic_values = {}
		for j in range(1,len(generic_tactics_data_array)):
			tactic_values[generic_tactics_data_array[j][0]] = generic_tactics_data_array[j][i]
		for tactic_level in combat_tactics_levels:
			print_tactic(f, tactic_level, tactic_name, tactic_values)

def print_cultural_combat_tactics(f):
	print('''
##########################################################################
# Cultural Tactics
##########################################################################''', file=f)
	for i in range(1,len(cultural_tactics_data_array[0])):
		tactic_name = cultural_tactics_data_array[0][i]
		tactic_values = {}
		for j in range(1,len(cultural_tactics_data_array)):
			tactic_values[cultural_tactics_data_array[j][0]] = cultural_tactics_data_array[j][i]
		for tactic_level in combat_tactics_levels:
			print_tactic(f, tactic_level, tactic_name, tactic_values, True)

def print_call_to_glory_combat_tactics(f):
	print('''
##########################################################################
# Call to Glory Tactics
##########################################################################''', file=f)
	for i in range(1,len(generic_tactics_data_array[0])):
		tactic_name = generic_tactics_data_array[0][i]
		tactic_values = {}
		for j in range(1,len(generic_tactics_data_array)):
			tactic_values[generic_tactics_data_array[j][0]] = generic_tactics_data_array[j][i]
		print_tactic(f, glorious_combat_tactic_level, tactic_name, tactic_values)
	print('''
##########################################################################
# Lodge-Specific Glorious Tactic definitions
##########################################################################''', file=f)
	for i in range(1,len(special_call_to_glory_tactics_data_array[0])):
		tactic_name = special_call_to_glory_tactics_data_array[0][i]
		tactic_values = {}
		for j in range(1,len(special_call_to_glory_tactics_data_array)):
			tactic_values[special_call_to_glory_tactics_data_array[j][0]] = special_call_to_glory_tactics_data_array[j][i]
		print_tactic(f, glorious_combat_tactic_level, tactic_name, tactic_values, True)

def print_localizations(f):
	print('''#CODE;ENGLISH;FRENCH;GERMAN;;SPANISH;;;;;;;;;x
########################################################################
# NOTE: This file is code-generated and should NOT be edited manually. #
########################################################################''', file=f)
	for i in range(1,len(generic_tactics_data_array[0])):
		tactic_name = generic_tactics_data_array[0][i]
		tactic_values = {}
		for j in range(1,len(generic_tactics_data_array)):
			tactic_values[generic_tactics_data_array[j][0]] = generic_tactics_data_array[j][i]
		print_tactic_localization(f, glorious_combat_tactic_level, tactic_name, tactic_values)
		for tactic_level in combat_tactics_levels:
			print_tactic_localization(f, tactic_level, tactic_name, tactic_values)
	for i in range(1,len(cultural_tactics_data_array[0])):
		tactic_name = cultural_tactics_data_array[0][i]
		tactic_values = {}
		for j in range(1,len(cultural_tactics_data_array)):
			tactic_values[cultural_tactics_data_array[j][0]] = cultural_tactics_data_array[j][i]
		for tactic_level in combat_tactics_levels:
			print_tactic_localization(f, tactic_level, tactic_name, tactic_values, True)
	for i in range(1,len(special_call_to_glory_tactics_data_array[0])):
		tactic_name = special_call_to_glory_tactics_data_array[0][i]
		tactic_values = {}
		for j in range(1,len(special_call_to_glory_tactics_data_array)):
			tactic_values[special_call_to_glory_tactics_data_array[j][0]] = special_call_to_glory_tactics_data_array[j][i]
		print_tactic_localization(f, glorious_combat_tactic_level, tactic_name + "_tactic", tactic_values, True)
	
def print_tactic_localization(f, tactic_level, tactic_name, tactic_values, is_cultural=False):
	localization_text = (tactic_level.prefix + "_" if tactic_level.prefix else "")+tactic_name+";"
	if tactic_level.name_prefix and (tactic_level.prefix != "glorious" or not is_cultural):
		localization_text += tactic_level.name_prefix + " "
	localization_text += tactic_values["name"]+" Tactic;;;;;;;;;;;;;x"
	print(localization_text, file=f)

def print_tactic(f, tactic_level, tactic_name, tactic_values, is_cultural=False):
	is_charge_tactic = tactic_values["ischarge"] and tactic_values["ischarge"] == "TRUE"
	print("""
# {6} Tactic
{0}{1} = {{
	days = {2}
	sprite = {3}
	group = {4}
	trigger = {{
		phase = {5}
		emf_{5}_{4}_tactic_troop_requirements = yes""".format(tactic_level.prefix + "_" if tactic_level.prefix else "",tactic_name + "_tactic" if tactic_level.prefix == "glorious" and is_cultural else tactic_name,tactic_values["days"],str(int(tactic_values["sprite"])+tactic_level.sprite_offset),tactic_values["group"],tactic_values["phase"],tactic_values["name"] if tactic_level.prefix == "glorious" and is_cultural else (tactic_level.name_prefix + " " if tactic_level.name_prefix else "") + tactic_values["name"]), file=f)
	if is_charge_tactic:
		print("""		is_flanking = no
		days = {0} # duration of combat >= {0} days""".format(10), file=f)
	if tactic_level.requires_flank_leader or is_cultural:
		print("""		flank_has_leader = yes""", file=f)
	if tactic_level.prefix == "glorious":
		print("""		leader = {
			has_character_modifier = call_to_glory""", file=f)
		if is_cultural:
			print("""			society_member_of = warrior_lodge_{0}""".format(tactic_name), file=f)
		elif tactic_name in replacement_glorious_tactics_list and len(replacement_glorious_tactics_list[tactic_name]) > 0:
			if len(replacement_glorious_tactics_list[tactic_name]) == 1:
				print("""			NOT = {{ society_member_of = warrior_lodge_{0} }}""".format(replacement_glorious_tactics_list[tactic_name][0]), file=f)
			else:
				print("""			NOR = {""", file=f)
				for replaced_tactic_name in replacement_glorious_tactics_list[tactic_name]:
					print("""				society_member_of = warrior_lodge_{0}""".format(replaced_tactic_name), file=f)
				print("""			}""", file=f)
		print("""		}""", file=f)
	elif is_cultural:
		print("""		leader = {{
			emf_{0}_culture = yes
		}}""".format(tactic_name), file=f)
	elif tactic_name in replacement_tactics_list and len(replacement_tactics_list[tactic_name]) > 0:
		print("""		NOT = {
			leader = {""", file=f)
		if len(replacement_tactics_list[tactic_name]) == 1:
			print("""				emf_{0}_culture = yes""".format(replacement_tactics_list[tactic_name][0]), file=f)
		else:
			print("""				OR = {""", file=f)
			for replaced_tactic_name in replacement_tactics_list[tactic_name]:
				print("""					emf_{0}_culture = yes""".format(replaced_tactic_name), file=f)
			print("""				}""", file=f)
		print("""			}
		}""", file=f)
	print("""	}}
	
	mean_time_to_happen = {{
		days = {0}""".format(tactic_values["weight"]), file=f)
	print("""		emf_{0}_tactic_leader_score = yes""".format(tactic_level.mtth_score_prefix), file=f)
	if tactic_level.has_tech_mtth_score_modifier:
		print("""		emf_{0}_tactic_tech_{1}_score = yes""".format(tactic_level.mtth_score_prefix,tactic_values["phase"]), file=f)
	if is_charge_tactic:
		print("""		modifier = {
			factor = 3
			troops = {
				who = knights
				value = 0.3
			}
		}
		modifier = {
			factor = 3
			troops = {
				who = heavy_infantry
				value = 0.3
			}
		}""", file=f)
	print("""	}}
	
	light_infantry_offensive = {0}
	heavy_infantry_offensive = {1}
	pikemen_offensive = {2}
	light_cavalry_offensive = {3}
	camel_cavalry_offensive = {4}
	knights_offensive = {5}
	archers_offensive = {6}
	horse_archers_offensive = {7}
	war_elephants_offensive = {8}

	light_infantry_defensive = {9}
	heavy_infantry_defensive = {10}
	pikemen_defensive = {11}
	light_cavalry_defensive = {12}
	camel_cavalry_defensive = {13}
	knights_defensive = {14}
	archers_defensive = {15}
	horse_archers_defensive = {16}
	war_elephants_defensive = {17}""".format(
	str(float(tactic_values["light_infantry_offensive"])+tactic_level.global_offensive_modifier),
	str(float(tactic_values["heavy_infantry_offensive"])+tactic_level.global_offensive_modifier),
	str(float(tactic_values["pikemen_offensive"])+tactic_level.global_offensive_modifier),
	str(float(tactic_values["light_cavalry_offensive"])+tactic_level.global_offensive_modifier),
	str(float(tactic_values["camel_cavalry_offensive"])+tactic_level.global_offensive_modifier),
	str(float(tactic_values["knights_offensive"])+tactic_level.global_offensive_modifier),
	str(float(tactic_values["archers_offensive"])+tactic_level.global_offensive_modifier),
	str(float(tactic_values["horse_archers_offensive"])+tactic_level.global_offensive_modifier),
	str(float(tactic_values["war_elephants_offensive"])+tactic_level.global_offensive_modifier),
	str(float(tactic_values["light_infantry_defensive"])+tactic_level.global_defensive_modifier),
	str(float(tactic_values["heavy_infantry_defensive"])+tactic_level.global_defensive_modifier),
	str(float(tactic_values["pikemen_defensive"])+tactic_level.global_defensive_modifier),
	str(float(tactic_values["light_cavalry_defensive"])+tactic_level.global_defensive_modifier),
	str(float(tactic_values["camel_cavalry_defensive"])+tactic_level.global_defensive_modifier),
	str(float(tactic_values["knights_defensive"])+tactic_level.global_defensive_modifier),
	str(float(tactic_values["archers_defensive"])+tactic_level.global_defensive_modifier),
	str(float(tactic_values["horse_archers_defensive"])+tactic_level.global_defensive_modifier),
	str(float(tactic_values["war_elephants_defensive"])+tactic_level.global_defensive_modifier)), file=f)
	
	if is_charge_tactic:
		print("""
	change_phase_to = melee""", file=f)
	
	if tactic_values["enemy"]:
		print("""
	enemy = {{
		group = {0}
		factor = 1
	}}""".format(tactic_values["enemy"]), file=f)
	print("}", file=f)

###

if __name__ == '__main__':
	sys.exit(main())
