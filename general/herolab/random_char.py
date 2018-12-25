from random import shuffle

stats = ['STR', 'DEX', 'INT', 'WIS', 'CHA', 'CON']
bonuses = [0, 0, 0, 1, 1, -1]

for i in range(3):
    shuffle(stats)
    shuffle(bonuses)
    for j in range(len(stats)):
        print stats[j], bonuses[j],
    print

