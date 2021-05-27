'''
'''

from bs4 import BeautifulSoup

import os, glob


ignore = ['Administration', 'Adventure Logs', 'Archived Channels', 'Extra Life', 'General',
    'logs and dice', 'out of character', 'Voice Channels', 'introduce']

skipping = []
checking = []
fnames = glob.glob("*after*.html")
for fn in fnames:
    check = True
    for s in ignore:
        if s in fn:
            check = False
    if 'message' in fn:
        check = True
    if check:
        checking.append(fn)
    else:
        skipping.append(fn)

print("Skipping", skipping)

recent = []
for fn in checking:
    print("Checking", fn)
    with open(fn, encoding="utf8") as fp:
        soup = BeautifulSoup(fp)
    nm_spans = soup.find_all('span', {'class': 'chatlog__author-name'})
    for span in nm_spans:
        if not span.attrs['title'] in recent:
            recent.append(span.attrs['title'])

print(recent, len(recent))
