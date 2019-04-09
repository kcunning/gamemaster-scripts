from collections import OrderedDict

def mult(xp, n, levels=[1, 2, 3, 4, 5]):
    poss = []
    for level in levels:
        x = xp
        if level * n <= xp:
            poss.append("{o} -> {lvl} x {n}".format(
                o=level-1,
                lvl=level,
                n=int(xp / level / n)))
    return poss


def straight(xp, n):
    return ["{n} total".format(n=int(xp / n))]

xp = 13

costs = OrderedDict(
    [
        ("Increase Attribute (5 per level)", mult(xp, 5, levels=[2,3,4,5])),
        ("Increase Skill (3 per level)", mult(xp,3)),
        ("New Specialty (3 each)", straight(xp,3)),
        ("Clan Discipline (5 per level)", mult(xp,5)),
        ("Other Discipline (7 per level)", mult(xp,7)),
        ("Caitiff Discipline (6 per level)", mult(xp,6)),
        ("Blood Sorcery Ritual (3 per level)", mult(xp,3)),
        ("Thin-blood Formula (3 per level)", mult(xp,3)),
        ("Advantage (3 each)", straight(xp,3)),
        ("Blood Potency (10 per level)", mult(xp,10, levels=list(range(2, 11)))),
    ])


print ("You have", xp, "XP")
for option in costs:
    print ("{o}:".format(o=option))
    for i in costs[option]:
        print ("\t", i)