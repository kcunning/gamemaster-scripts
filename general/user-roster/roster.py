'''
'''

from bs4 import BeautifulSoup

def get_classlevels(nm):
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

    lvls = ['1', '2', '3']

    combos = []

    for ab in abbrvs:
        for lvl in lvls:
            combos.append(ab+lvl)
            combos.append(ab+' '+lvl)

    rs = []
    for combo in combos:
        if combo in nm:
            r = combo.replace(' ', '')[:-1]
            rs.append(abbrvs[r])
    return rs

# all time will give you inactive players.
fn = "introduce-60-days.html"
# 60 days will remove inactive players
# fn = "introduce-60-days.html"
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
fnames = ['general-60-days.html', 'introduce-60-days.html']
for fn in fnames:
    with open(fn, encoding="utf8") as fp:
        soup = BeautifulSoup(fp)
    nm_spans = soup.find_all('span', {'class': 'chatlog__author-name'})
    for span in nm_spans:
        if not span.attrs['title'] in recent:
            recent.append(span.attrs['title'])

char_classes = {}

for u in active:
    if not u in recent:
        act = ' [Inactive]'
    else:
        act = ''
    print(active[u])
    rs = get_classlevels(active[u])
    print (rs)
    print('***')
    for r in rs:
        if not r in char_classes:
            char_classes[r]  = [active[u] + act]
        else:
            char_classes[r].append(active[u] + act)

keys = list(char_classes.keys())
keys.sort()

inactive_ppl = []
for key in keys:
    for u in char_classes[key]:
        if '[Inactive]' in u:
            inactive_ppl.append(u)


for key in keys:
    print('{key} ({n}):\n\t{users}'.format(
        key=key, n=len(char_classes[key]), users='\n\t'.join(char_classes[key])).replace(
        "||", "|"))
    print()