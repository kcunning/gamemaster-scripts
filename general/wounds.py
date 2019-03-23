import csv
from random import choice

def get_lines(fn="wounds_chars.csv"):
    lines = []
    with open(fn) as f:
        reader = csv.reader(f)
        for line in reader:
            lines.append(line)
    return lines

def create_char_dict(lines):
    d = {}
    for name, wounds, current in lines:
        d[name] = [int(wounds), int(current)]
    return d

def wound_random_char(d):
    c = choice(d.keys())
    print "Wounding", c
    while d[c][1] == d[c][0]:
            print "Cancel that.", c, "is out of the battle."
            c = choice(d.keys())
            print "Wounding", c
    d[c][1] += .5
    print c, "now has", d[c][1], "wounds."

def print_chars_status(d):
    in_battle = []
    out_of_battle = []

    for c in d:
        if d[c][0] > d[c][1]:
            s = "{ch} ({c}/{w})".format(ch=c, c=str(d[c][1]), w=str(d[c][0]))
            in_battle.append(s)
        else:
            out_of_battle.append(c)

    print "In battle:"
    in_battle.sort()
    for ch in in_battle: print ch
    if not in_battle: print "None"

    print "\nOut of battle:"
    for ch in out_of_battle: print ch
    if not out_of_battle: print "None"

    print



lines = get_lines()
chars = create_char_dict(lines)
lines = get_lines('wounds_mobs.csv')
mobs = create_char_dict(lines)

r = 1
print "Starting battle"
while True:
    print "Round", r
    wound_random_char(chars)
    wound_random_char(mobs)
    print_chars_status(chars)
    print_chars_status(mobs)
    r += 1

    inp = raw_input("X to stop: ")
    if inp.lower() == 'x': break