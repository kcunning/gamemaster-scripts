from bs4 import BeautifulSoup

import os, glob

edict = {}

fnames = glob.glob("*after*.html")
for fn in fnames:
    with open(fn, encoding="utf8") as fp:
        soup = BeautifulSoup(fp)
    emojis = soup.find_all('img', {'class': 'emoji'})
    for emoji in emojis:
        if not emoji.attrs['alt'] in edict:
            edict[emoji.attrs['alt']] = 0
        edict[emoji.attrs['alt']] += 1

for key in edict.keys():
    print (key, ";", edict[key])