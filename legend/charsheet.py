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
            self.skills[skill] = 2

    def __init__(self, **kwargs):
        # All the static stuff first
        stats = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
        self.stats = {}
        for stat in stats: 
            self.stats[stat] = kwargs['stats'][stat] if 'stats' in kwargs else 10
        simple = (('size', 'medium'), ('race', None), ('mclass', None), ('level', 1), ('name', None),
            ('tracks', []), ('init_stat_bonus', None), ('init_skill_bonus', None))
        for attr, default in simple:
            setattr(self, attr, kwargs[attr] if attr in kwargs else default)

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

def apply_race(ch, race):
    for stat, mod in race.stats:
        ch.stats[stat] += mod
    basic = (('size', 'average'), ('type', 'humanoid'), ('vision', None))
    for attr, default in basic:
        setattr(ch, attr, getattr(race, attr) if hasattr(race, attr) else default)
    if hasattr(race, "skill_bonus"):
        for s in race.skill_bonus:
            ch = races.apply_skill_bonus(ch, s)
    if hasattr(race, 'stats_choice') and ch.init_stat_bonus in race.stats_choice[0]:
        ch = races.apply_ability_bonus(ch, ch.init_stat_bonus, 2)
    if hasattr(race, 'skill_choice') and ch.init_skill_bonus in race.skill_choice[0]:
        ch = races.apply_skill_bonus(ch, ch.init_skill_bonus)

    return ch

print("Starting program...")

stats = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']

mychar = Character(
    stats={'STR': 12, 'DEX': 14, 'CON': 8, 'INT': 14, 'WIS': 18, 'CHA': 14},
    size="small",
    race="HUMAN",
    mclass="fighter",
    name="Tester",
    tracks=(('special', 'slow')),
    init_skill_bonus='History'
)
print("Initial")
pprint (mychar.__dict__)
print("Applying race")
mychar = apply_race(mychar, getattr(races, mychar.race))
pprint(mychar.__dict__)
