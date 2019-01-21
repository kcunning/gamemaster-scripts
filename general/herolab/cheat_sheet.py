#!/usr/bin/env python3

from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring

''' Things to get:
    * Their class
    * What they're wearing
    * Their attacks with all weapons on their person
    * Saves
    * AC / HP
'''

def get_data(fn):
    ''' Gets the data from a Hero Lab XML export
    '''
    f = open(fn)
    lines = f.readlines()
    s = "".join(lines)
    d = bf.data(fromstring(s))
    f.close()

    return d

def find_armor(ch, t):
    if 'item' in ch[t]:
        for item in ch[t]['item']:
            if 'itemslot' in item:
                if item['itemslot']['$'] == "Armor":
                    return item['@name']

def get_passive_vals(ch):
    pvals = {}
    svd = {}
    for save in ch['saves']['save']:
        svd[save['@abbr']] = save['@save']

    skd = {}
    names = ["Perception", "Stealth"]
    for skill in ch['skills']['skill']:
        if skill['@name'] in names:
            skd[skill['@name']] = skill['@value']
    
    armd = {}
    armd['ac'] = ch['armorclass']['@ac']
    # Now to find the armor...
    a = find_armor(ch, "magicitems")
    if not a:
        a = find_armor(ch, "gear")
    return {'skills': skd, 'saves': svd}


def get_char_details(ch):
    v = {
        "name": ch["@name"],
        "classes": ch['classes']['@summary']
    }

    return v

def get_combat_vals(ch):
    comb = {}
    w = ch['melee']['weapon']

    # comb['melee'].append(
    #     {'name':w['@name'],
    #      'damage':w['@damage'],
    #      'crit':w['@crit'],
    #      'attack':w['@attack']})
    try:
        comb['melee'] = {'name':w['@name'],
             'damage':w['@damage'],
             'crit':w['@crit'],
             'attack':w['@attack']}
    except TypeError:
        pass

    try:
        w = ch['ranged']['weapon']
        comb['ranged'] = {'name':w['@name'],
         'damage':w['@damage'],
         'crit':w['@crit'],
         'attack':w['@attack']}
    except KeyError:
        pass

    return comb

def get_spell_status(ch):
    pass

def get_char_vals(ch):
    ''' Gets the vals that I use the most for a character during combat.
    '''
    # AC, melee attack, ranged attack
    # Saves, perception, stealth
    # Init
    # Spells (if any, not a list)
    # CMD / CMB
    vals = {}
    
    vals['character'] = get_char_details(ch)
    vals['combat'] = get_combat_vals(ch)
    vals['passive'] = get_passive_vals(ch)

    return vals

def print_sheet(ch):
    print(ch)
    # Print combat stuff
    tpl = "\t{name}:\
        \t\t{atk} DMG: {dmg} Crit: {crit}"
    for key in ch['combat']:
        print(key)
        for d in ch['combat'][key]:
            print(d, key)
            

def main():
    d = get_data("sewer-foes.xml")
    chars = d['document']['public']['character']
    cheats = []
    for ch in chars:
        cheats.append(get_char_vals(ch))

    print_sheet(cheats[0])
        

if __name__ == '__main__':
    main()
