from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring

def get_char_loot(ch):
    # Characters always have gold
    gold = ch['money']['@total']

    # Except for characters who have no gear
    try:
        gear = ch['gear']['item']
    except KeyError:
        gear = []

    # Except for characters who have magic items
    try:
        magic = ch['magicitems']['item']
    except KeyError:
        magic = []

    return gold, gear, magic

def print_char_loot(loot, d):
    for item in loot:
        # If an item name starts with a '+', Google sheets acts weird. 
        # Prepending an apostrophe fixes this behavior.
        if item[0][0] == "+":
            item[0] = "'" + item[0]
        print d.join(map(str, item))

def main(fn):
    f = open(fn)
    lines = f.readlines()
    s = "".join(lines)
    d = bf.data(fromstring(s))

    items = []
    g = 0

    for ch in d['document']['public']['character']:
        gold, gear, magic = get_char_loot(ch)
        g += gold
        for item in gear:
            try:
                items.append([item['@name'], str(item['cost']['@value']), str(item['@quantity'])])
            except TypeError:
                # Sometimes there's no items
                pass

        for item in magic:
            try:
                items.append([item['@name'], str(item['cost']['@value']), str(item['@quantity'])])
            except TypeError:
                # Sometimes there's no items
                pass

    items.append(['Gold', g, 1])

    print_char_loot(items, "\t")

main('walcourt.xml')
