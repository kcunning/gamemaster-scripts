''' This is a character sheet manager for the TTRPG Legend by ruleofcool.com.
    It's not even close to done.
'''

from collections import OrderedDict
from pprint import pprint

import races
import skills

class Character:
    def get_mod(self, stat):
        s = self.stats[stat]
        return (s - 10) // 2

    def add_base_skills(self):
        self.skills = {}
        for skill in skills.base:
            self.skills[skill] = 0

    def __init__(self, **kwargs):
        # All the static stuff first
        stats = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
        self.stats = {}
        for stat in stats: 
            self.stats[stat] = kwargs['stats'][stat] if 'stats' in kwargs else 10
        simple = (('size', 'medium'), ('race', None), ('mclass', None), ('level', 1), ('name', None),
            ('tracks', []), ('init_stat_bonus', None), ('init_skill_bonus', None), ('init_extra_bonus', None))
        for attr, default in simple:
            setattr(self, attr, kwargs[attr] if attr in kwargs else default)

        saves = ('Fort', 'Ref', 'Will')
        self.saves = {}
        for save in saves:
            self.saves[save] = 0

        # Derived stuff. Not sure if should be attr or calc'd each time?
        self.initiative = self.get_mod('DEX')
        self.dr = self.get_mod('CON') // 2
        dcs = (('AWARENESS', 'WIS'), ('BLUFF','WIS'), ('DIPLOMACY','INT'), ('INTIMIDATE','CHA'), 
            ('PERCEPTION','CHA'))
        self.dcs = {}
        for dc, stat in dcs:
            self.dcs[dc] = 10 + self.get_mod(stat) + self.level
        self.dcs['MANEUVER'] = 10 + self.level // 2
        self.dcs['MANEUVER'] += self.get_mod('STR') if self.get_mod('STR') > self.get_mod('DEX') else self.get_mod('DEX')
        self.add_base_skills()

        self.bab = 0
        self.ac = 10

print("Starting program...")

stats = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']

mychar = Character(
    stats={'STR': 10, 'DEX': 10, 'CON': 10, 'INT': 10, 'WIS': 10, 'CHA': 10},
    race="orc",
    mclass="fighter",
    name="Tester",
    tracks=(('special', 'slow')),
    init_stat_bonus='INT',
    init_skill_bonus='History',
    init_extra_bonus='Ref'
)
print("Initial")
pprint (mychar.__dict__)
print("Applying race")
r = getattr(races, mychar.race)
mychar = r(mychar)
pprint(mychar.__dict__)
