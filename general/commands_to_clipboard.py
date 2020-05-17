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
        '!r 1d20 + 9 Comp bow, first attack',
        '!r 1d20 + 4 Comp bow, second attack',
        '!r 1d20 - 1 Comp bow, third attack',
        '!r 1d6 + 1d8 + 1d10 Bow Damage: Regular, Precision, Crit',
        '!r 1d20 + 9 Percep',
        '!r 1d20 + 7 Fort',
        '!r 1d20 + 10 Reflex',
        '!r 1d20 + 5 Will',
        '!r 1d20 + 5 Skills: Forest Lore, Medicine, Nature, Scouting',
        '!r 1d20 + 6 Skills: Athletics',
        '!r 1d20 + 7 Skills: Survival',
        '!r 1d20 + 8 Skills: Acrobatics, Stealth, Thievery'
    ],
}

copy_commands(commands['Rowan'])