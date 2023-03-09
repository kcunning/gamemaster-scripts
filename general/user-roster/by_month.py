from bs4 import BeautifulSoup
from datetime import datetime

import os, glob

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

    lvls = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

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

fn = "introduce-all-time.html"
with open(fn, encoding="utf8") as fp:
    soup = BeautifulSoup(fp)

nm_spans = soup.find_all('span', {'class': 'chatlog__author-name'})

roster = {}
dates = {}

for span in nm_spans:
    roster[span.attrs['title']] = span.text
    if not span.attrs['title'] in dates:
        d = span.parent.find('span', {'class':"chatlog__timestamp"}).text
        dt = datetime.strptime(d, '%d-%b-%y %I:%M %p')
        dates[span.attrs['title']] = "{Y}-{M:02}".format(Y=dt.year, M=dt.month)

users_by_month = {}

for month in set(dates.values()):
    users_by_month[month] = []
    for user in dates:
        if dates[user] == month and ':' in roster[user]:
            users_by_month[month].append(roster[user])

months = list(users_by_month.keys())
months.sort()
for key in months:
    print (key)
    print ("  ", end="")
    print ("\n  ".join(users_by_month[key]))
