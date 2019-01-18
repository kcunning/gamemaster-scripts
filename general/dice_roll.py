#!/usr/bin/env python3

# The purpose of this script is just roll every die I might need
# because having to pick out which sided die I need is too much
# effort.

from random import randint
from datetime import datetime

def get_rolls(dtypes, n):
    r = {}
    r['time'] = datetime.now()
    r['plus'] = n
    for dt in dtypes:
        num = randint(1, dt)
        r[dt] = str(num) + "/" + str(num + n)
    return r

def print_rolls(rolls, dtypes):
    print(rolls['time'].strftime("%H:%M:%S"))
    for dt in dtypes:
        print("\t", dt, "->", rolls[dt])

def print_roll_history(history, dice_types):
    for log in history:
        print(log['time'].strftime("%H:%M:%S"), "Modifier:", log['plus'])
        print("\t",)
        for dt in dice_types:
            print(str(dt) + "->" + log[dt],)
        print()

dice_types = [2, 4, 6, 8, 10, 12, 20, 100]

roll_log = []

while True:
    c = input("[Q]uit / [L]og / Any key: ")
    if c.lower() == 'q':
        break
    elif c.lower() == 'l':
        print_roll_history(roll_log, dice_types)
        continue

    if len(c) > 1 and c[0] == '-' and c[1:].isdigit():
        # It's a negative number!
        n = int(c[1:]) * -1
    elif c.isdigit():
        n = int(c)
    else:
        n = 0

    rolls = get_rolls(dice_types, n)
    roll_log.append(rolls)
    print_rolls(rolls, dice_types)

