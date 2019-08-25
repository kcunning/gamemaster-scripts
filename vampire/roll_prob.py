''' Dice roller probability

Probability with Vampire dice isn't quite as simple as it is with other
games. 

Given a set number of dice and a set difficulty, what's the chance of 
succeeding.

'''
from random import choice

def get_total_successes(crit, normal):
    total = crit*2 + normal
    return total

def roll_sim(dice, dc, hunger=1, runs=100):
    wins = 0
    crit = 0
    messy = 0
    bestial = 0
    die = [-1,0,0,0,0,1,1,1,1,2]

    for i in range(runs):
        roll = []
        for i in range(dice):
            roll.append(choice(die))
        # print(roll)
        c = 0
        r = 0
        for d in roll:
            if d == 2:
                c += 1
            elif d == 1:
                r += 1

        if c//2 != c/2:
            c -= 1
            r += 1
        # print(c, r, get_total_successes(c, r))
        total = get_total_successes(c, r)
        # Just a win
        if total >= dc:
            wins += 1
        
        # Critical win: There's at least one crit
        if c > 0 and total >= dc:
            crit +=1

        # Messy crit: One of the first X die has a crit, and there's 
        # more than one crit total
        h = False
        for i in range(hunger):
            if roll[i] == 2:
                h = True
                break
        if h and total >= dc:
            messy += 1

        # Bestial failure: One of the first X die has a beast, and the
        # roll is a failure
        m = False
        for i in range(hunger):
            if roll[i] == -1:
                m = True
                break
        if m and total < dc:
            bestial += 1

    print("Wins: {w} out of {r}. [Crit: {c}, Messy: {m}, Bestial: {b}]".format(
        w=wins, r=runs, c=crit, m=messy, b=bestial))



dice = 6
dc = 3
hunger = 3

for i in range(20):
    roll_sim(dice, dc, hunger, 100)