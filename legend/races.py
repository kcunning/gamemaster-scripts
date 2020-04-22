class Race:

	def __init__(self, **kwargs):
		for key in kwargs:
			setattr(self, key, kwargs[key])

# Dwarf!

def eng_bonus(ch):
    ch.skills['engineering'] += 1 + ch.level // 8
    return ch

DWARF = Race(
    stats= (('CON', 2), ('INT', 2), ('CHA', -2)),
    size= 'average',
    type= 'humaniod',
    special= (eng_bonus,),
    vision=['darkvision']
)

def ment_bonus(ch):
    # Needs to be updated to be either Wis or Int
    ch.stats['INT'] += 2
    return ch

def nat_bonus(ch):
    ch.skills['nature'] += 1 + ch.level // 8
    return ch

ELF = Race(
    stats= (('DEX', 2), ('CON', -2)),
    size= 'average',
    type= 'humaniod',
    special= (ment_bonus, nat_bonus),
    vision=['ghostwise sight']
)