from random import randint
import datetime

lvl = 10
base_rounds = 10 
rounds = lvl * base_rounds

print("You have", rounds, "rounds to try to get through.")

for i in range(rounds):
    r = randint(1, 100)
    print(r)
    if r >= 96:
        break

print("Number of rounds:", i)
if i == rounds - 1:
    print("Nothing got through")
else:
    print("It took", str(datetime.timedelta(seconds=i*6)))