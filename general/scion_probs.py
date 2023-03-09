from random import randint

pool = 10
base = 8
runs = 1000

wins = {}

# First, the probs for exploding
for i in range(1, runs):
    arr = [randint(1, 10) for i in range(pool)]
    for i in arr:
        if i == 10:
            arr.append(randint(1,10))

    w = 0
    for i in arr:
        if i > 7:
            w += 1

    if not w in wins:
        wins[w] = 1
    else:
        wins[w] += 1
    print(arr, w)



wins2 = {}

for i in range(1, runs):
    arr = [randint(1, 10) for i in range(pool)]

    w = 0
    for i in arr:
        if i > 10:
            w += 2
        elif i > 7:
            w += 1
        elif i == 1:
            w -= 1

    if not w in wins2:
        wins2[w] = 1
    else:
        wins2[w] += 1
    print(arr, w)

vals = list(wins.keys())
vals.sort()

print("Exploding...")
for val in vals:
    print("{v}: {n} ({p}%)".format(v=val, n=wins[val], p=int(wins[val]/runs*100)))

print("Adding...")
vals = list(wins2.keys())
vals.sort()

for val in vals:
    print("{v}: {n} ({p}%)".format(v=val, n=wins2[val], p=int(wins2[val]/runs*100)))



