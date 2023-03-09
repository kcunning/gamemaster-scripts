from random import choice

# Assumptions:
# Book One - 1-4
# Book Two - 5-8
# Book Three - 9-11
# Book Four - 12-14
# Book Five - 15-17
# Book Six - 18-20

adventures = {
    "Age of Ashes": [1,2,3,4,5,6],
    "Extinction Curse": [1,2,3,4,5,6],
    "Agents of Edgewatch": [1,2,3,4,5,6],
    "Abomination Vaults": [1,2,3],
    "Fists of the Ruby Phoenix": [4,5,6],
    "Strength of Thousands": [1,2,3,4,5,6],
    "Quest for the Frozen Flame": [1,2,3],
    "Outlaws of Alkenstar": [1,2,3],
}

standalones = {
    "Shadows at Sundown": [3],
    "Malevolence": [1],
    "Night of the Grey Death": [5],
    "Fall of Plaguestone": [1],
    "The Slithering": [2],
    "Troubles in Otari": [1]
}

by_level = {}

for ap in adventures:
    for lvl in adventures[ap]:
        if not lvl in by_level:
            by_level[lvl] = []
        by_level[lvl].append(ap)

lvls = list(range(1,7))
random_aps = []

for i in lvls:
    while True:
        ap = choice(by_level[i])
        ## Uncomment if you want zero repeats
        # if not ap in random_aps:
        #     random_aps.append(ap)
        #     break

        # Uncomment if you want repeats, but not back to back
        if random_aps and ap != random_aps[-1]:
            random_aps.append(ap)
            break
        elif not random_aps:
            random_aps.append(ap)
            break

i = 1
for ap in random_aps:
    print(i, ap)
    i += 1
