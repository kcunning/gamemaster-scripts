# The purpose of this script is just roll every die I might need
# because having to pick out which sided die I need is too much
# effort.

from random import randint
from datetime import datetime

def get_rolls(dtypes):
    r = {}
    r['time'] = datetime.now()
    for dt in dtypes:
        r[dt] = randint(1, dt)
    return r

def print_rolls(rolls, dtypes):
    print rolls['time'].strftime("%H:%M:%S")
    for dt in dtypes:
        print "\t", dt, "->", rolls[dt]

def print_roll_history(history, dice_types):
    for log in history:
        print log['time'].strftime("%H:%M:%S"),
        for dt in dice_types:
            print dt, "->", log[dt], "||",
        print

dice_types = [2, 4, 6, 8, 10, 12, 20, 100]

roll_log = []

while True:
    c = raw_input("[Q]uit / [L]og / Any key: ")
    if c.lower() == 'q':
        break
    elif c.lower() == 'l':
        print_roll_history(roll_log, dice_types)
        continue

    rolls = get_rolls(dice_types)
    roll_log.append(rolls)
    print_rolls(rolls, dice_types)

