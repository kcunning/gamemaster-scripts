''' This script takes all of my frequently used commands with dice rollers
    and pops them onto the clipboard in Windows.

    This is useful since you can see your copy history in windows by 
    hitting Windows + V. Note that you need to turn on copy history for this to 
    work as intended.
'''
from time import sleep
import pyperclip

def copy_commands(lines):
    print("Copying...")
    lines.reverse()
    for line in lines:
        print("\t", line)
        pyperclip.copy(line)
        # Gotta sleep, or Windows won't add it to the history
        sleep(1)


commands = {
    "Rowan": [
        '!r 1d20 + 10 Comp bow, first attack',
        '!r 1d20 + 5 Comp bow, second attack',
        '!r 1d20 + 0 Comp bow, third attack',
        '!r 1 + 2d6 + 1d8 + 1d10 + 2d6 Bow Damage: Bonus, Regular, Precision, Crit',
        '!r 1d20 + 8 Percep',
        '!r 1d20 + 8 Fort',
        '!r 1d20 + 11 Reflex',
        '!r 1d20 + 8 Will',
        '!r 1d20 + 6 Skills: Forest Lore, Nature, Scouting',
        '!r 1d20 + 7 Skills: Athletics',
        '!r 1d20 + 8 Skills: Medicine'
        '!r 1d20 + 6 Skills: Survival',
        '!r 1d20 + 9 Skills: Acrobatics, Stealth, Thievery'
    ],
    "Seph-origin": [
        '!r 10d10e10 Tech roll (Int, Tech) (spec Hacking)',
        '!r 9d10e10 Science roll (Int, Science) (Electronics spec) ',
        '!r 8d10e10 Academics roll (Int, Academics) (spec Mythology)'
    ]
}

copy_commands(commands['Seph-origin'])