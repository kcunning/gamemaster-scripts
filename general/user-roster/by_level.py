'''
'''

from bs4 import BeautifulSoup

import os, glob

def get_char_levels(nm):
    abbrvs = {
        'A': 'Alchemist',
        'B': 'Barbarian',
        'Ba': 'Bard',
        'Ch': 'Champion',
        'Cl': 'Cleric',
        'D': 'Druid',
        'F': 'Fighter',
        'M': 'Monk',
        'R': 'Ranger',
        'Ro': 'Rogue',
        'S': 'Sorcerer',
        'W': 'Wizard',
        'I': 'Investigator',
        'O': 'Oracle',
        'Sw': 'Swashbuckler',
        'Wt': 'Witch'
    }

    lvls = ['1', '2', '3', '4', '5', '6']

    combos = []

    for ab in abbrvs:
        for lvl in lvls:
            combos.append(ab+lvl)
            combos.append(ab+' '+lvl)
    rs = []
    for lvl in lvls:
        if lvl in nm:
            rs.append(lvl)
    return rs

# all time will give you inactive players.
# fn = "Kellandale - out of character - introduce-yourself [654109188548591616].html"
# fn = glob.glob("*introduce-yourself*after*")[0]
# 60 days will remove inactive players
fn = "introduce-all-time.html"
with open(fn, encoding="utf8") as fp:
    soup = BeautifulSoup(fp)

nm_spans = soup.find_all('span', {'class': 'chatlog__author-name'})

roster = {}

for span in nm_spans:
    roster[span.attrs['title']] = span.text

active = {}

for u in roster:
    if ':' in roster[u]:
        active[u] = roster[u]

recent = []
fnames = glob.glob("*after*.html")
for fn in fnames:
    with open(fn, encoding="utf8") as fp:
        soup = BeautifulSoup(fp)
    nm_spans = soup.find_all('span', {'class': 'chatlog__author-name'})
    for span in nm_spans:
        if not span.attrs['title'] in recent:
            recent.append(span.attrs['title'])

lvls = ['1', '2', '3', '4', '5', '6']
char_levels = {}
for lvl in lvls:
    char_levels[lvl] = []

for u in active:
    if not u in recent:
        act = ' [Inactive]'
    else:
        act = ''
    print(active[u])
    rs = get_char_levels(active[u])
    print (rs)
    print('***')
    for r in rs:
        char_levels[r].append(active[u] + act)

for lvl in lvls:
    print("\nLevel {x} [{n}]".format(x=lvl, n=len(char_levels[lvl])))
    for char in char_levels[lvl]:
        print('  ', char)