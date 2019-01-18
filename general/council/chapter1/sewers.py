#!/usr/bin/env python3

# This file is meant to run the random sewer encounter that appears
# in part two of _Council of Thieves: The Bastards of Erebus_. It
# will not run the encounters for you, but it will save you from lots of
# looking back and forth between the source material and your dice.

import random

def nothing():
    pass

def junction():
    c = random.randint(1, 10)
    if c == 1:
        dc = 20
    else:
        dc = 12
    return "Find waymarker: DC {} Perception".format(str(dc))

def intersection():
    t = random.randint(1, 3) + 1
    c = random.randint(1, 10)
    if c == 1:
        dc = 20
    else:
        dc = 12
    return "Intersection with {} hallways. DC {} Perception".format(
        str(t), str(dc))

def encounter():
    r = random.randint(1, 100)
    if r < 36:
        return "Hellnights (3)!"
    elif r < 46:
        return "Ooze bugs (8)"
    elif r < 56:
        return "Goblin patrol (1)"
    elif r < 61:
        return "Goblin lair (3)"
    elif r < 76:
        r2 = random.randint(1, 100)
        if r2 < 76:
            return "Undead (3 skeletons)"
        else:
            return "Undead (2 zombies)"
    elif r < 86:
        return "Hazard"
    elif r < 91:
        return "Cache"
    else:
        return "Special"

def blockage():
    r = random.randint(1, 100)
    if r < 30:
        return "Blockage: Dead end"
    else:
        return "Blockage: Can be cleared"

def exit_sewer():
    r = random.randint(1, 100)
    if r < 21:
        return "Exit is an outflow to the harbor"
    else:
        return "Exit is to the town"

def get_sewer_feature():
    r = random.randint(1, 100)
    if r < 21:
        return 'no change', nothing
    elif r < 41:
        return 'junction', junction
    elif r < 61:
        return 'intersection', intersection
    elif r < 81:
        return 'encounter', encounter
    elif r < 91:
        return 'blockage', blockage
    else:
        return 'exit', exit_sewer

events = []

print("Let's run around some sewers!")
while True:
    t, f = get_sewer_feature()
    print("***{}***".format(t))
    r = f()
    print("\t", r)

    events.append(t + ': ' + str(r))

    while True:
        i = input("Any key for another, e for events, q to quit: ")
        if i.lower() == 'e':
            for event in events:
                print(event)
        else:
            break
    if i.lower() == 'q':
        print("Here were all of your events:")
        for event in events: print(event)
        break
