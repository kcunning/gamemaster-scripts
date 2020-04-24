from skills import base

class Race:

	def __init__(self, **kwargs):
		for key in kwargs:
			setattr(self, key, kwargs[key])

def apply_skill_bonus(ch, skill):
    ch.skills[skill] += 1 + ch.level // 8
    return ch

def apply_ability_bonus(ch, stat, n):
    ch.stats[stat] += n
    return ch

DWARF = Race(
    stats= (('CON', 2), ('INT', 2), ('CHA', -2)),
    size= 'average',
    type= 'humaniod',
    skill_bonus=["Engineering"],
    vision=['darkvision']
)

ELF = Race(
    stats= (('DEX', 2), ('CON', -2)),
    stats_choice=('INT', 'WIS', 2),
    size= 'average',
    type= 'humaniod',
    skill_bonus=["Nature"],
    vision=['ghostwise sight']
)

GNOME = Race(
    stats= (('CON', 2), ('CHA', 2), ('STR', -2)),
    size= 'small',
    type= 'humaniod',
    skill_bonus=["Diplomacy"],
    vision=['darkvision']
)

HALFLING = Race(
    stats= (('DEX', 2)),
    size= 'small',
    type= 'humaniod',
    skill_bonus=["Diplomacy"],
    vision=['darkvision']
)

HUMAN = Race(
    stats= (),
    stats_choice=(('INT', 'WIS', 'STR', 'DEX', 'CON', 'CHA'), 2),
    size= 'average',
    type= 'humaniod',
    skill_choice=(base.keys(), 1)
)