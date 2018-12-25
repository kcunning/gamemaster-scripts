from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring

def get_data(fn):
    ''' Gets the data from a Hero Lab XML export
    '''
    f = open(fn)
    lines = f.readlines()
    s = "".join(lines)
    d = bf.data(fromstring(s))
    f.close()

    return d

def remove_no_diffs(d1):
    ''' Given a dictionary where each key has a two-value list, 
        return a dict of the key:value pairs where there is a difference
        between the first and second list items.
    '''
    rd = {}

    for k in d1:
        if d1[k][0] != d1[k][1]:
            rd[k] = d1[k]

    return rd

def compare_arr(a1, a2):
    ''' Compares two lists and returns a list of differences.
    '''
    r = list(set(a2) - set(a1))
    r2 = ["Added: " + i for i in r]
    r2.extend("Removed: " + i for i in list(set(a1) - set(a2)))

    return r2

def compare_attributes(c1, c2):
    ''' Takes two characters and compares the attributes.
        Returns a list of attributes that have changed.
    '''
    d = {}
    for a in c1['attributes']['attribute']:
        d[a['@name']] = [a['attrvalue']['@base']]
    for a in c2['attributes']['attribute']:
        d[a['@name']].append(a['attrvalue']['@base'])

    r = remove_no_diffs(d)

    return r

def compare_skills(c1, c2):
    ''' Takes two characters and compares skills.
        Returns a dictionary of skills where the ranks have changed
    '''
    d = {}

    for s in c1['skills']['skill']:
        d[s['@name']] = [s['@ranks']]
    for s in c2['skills']['skill']:
        if not s['@name'] in d:
            d[s['@name']] = [0, s['@ranks']]
            continue
        d[s['@name']].append(s['@ranks'])

    r = remove_no_diffs(d)

    return r

def compare_feats(c1, c2):
    ''' Takes two characters and compares feats.
        Returns a list of feats that have been added.
    '''
    f1 = []
    f2 = []
    for feat in c1['feats']['feat']:
        f1.append(feat['@name'])
    for feat in c2['feats']['feat']:
        f2.append(feat['@name'])

    r = compare_arr(f1, f2)

    return r

def compare_traits(c1, c2, t=['traits', 'trait']):
    ''' Takes two characters and compares traits.
        Returns traits that have beend added and removed
    '''
    a, b = t
    if not c1[a]:
        t1 = []
    else:
        t1 = []
        for i in c1[a][b]:
            t1.append(i['@name'])

    if not c2[a]:
        t2 = []
    else:
        t2 = []
        for i in c2[a][b]:
            t2.append(i['@name'])
    
    tds = compare_arr(t1, t2)

    return tds

def compare_items(c1, c2, t="magicitems"):
    ''' Takes two characters, and compares the items in their inventory.
        Returns a list of the items with how they changed prepended to the
        item name ('Added', 'Removed', 'Modified')

        TODO: Add # of items added to added items.
    '''
    items1 = {}
    if 'item' in c1[t]:
        for i in c1[t]['item']:
            if i['@name'] in items1:
                items1[i['@name']] += i['@quantity']
            else:
                items1[i['@name']] = i['@quantity']

    items2 = {}
    if 'item' in c2[t]:
        for i in c2[t]['item']:
            if i['@name'] in items2:
                items2[i['@name']] += i['@quantity']
            else:
                items2[i['@name']] = i['@quantity']

    added_removed = compare_arr(items1.keys(), items2.keys())

    mods = []
    # How to find the items where only the quantity changed. 
    for key in items1.keys():
        if key in items2 and items1[key] != items2[key]:
            mods.append("Modified: {k} ({a} -> {b})".format(
                k=key,
                a=str(items1[key]),
                b=str(items2[key])))

    added_removed.extend(mods)

    return added_removed

def compare_books(c1, c2):
    ''' Takes two characters and compares the books enabled for
        that character. Change type is prepened to the book name 
        ('Added', 'Removed')
    '''
    b1 = c1['settings']['@summary'].split(";")
    b2 = c2['settings']['@summary'].split(";")

    r = compare_arr(b1, b2)
    return r

def compare_spells(c1, c2, t='spellbook'):
    ''' Takes two characters and compares spells known / owned and returns
        a list of changes. The change is prepended to the spell name 
        ('Added', 'Removed')
    '''
    sb1 = []
    if 'spell' in c1[t]:
        for s in c1[t]['spell']:
            sb1.append(s['@name'])

    sb2 = []
    if 'spell'  in c2[t]:
        for s in c2[t]['spell']:
            sb2.append(s['@name'])

    r = compare_arr(sb1, sb2)

    return r



def compare_chars(c1, c2):
    ''' Takes two characters and compares to each other to see what has changed.
        Returns a dictionary of all changes.
    '''
    diffs = {}
    # Class change?
    if c1['classes']['@summary'] != c2['classes']['@summary']:
        diffs['classes'] = (c1['classes']['@summary'], c2['classes']['@summary'])
    
    # Money change?
    if c1['money']['@total'] != c2['money']['@total']:
        diffs['money'] = (c1['money']['@total'], c2['money']['@total'])

    # Attributes
    dattrs = compare_attributes(c1, c2)
    if dattrs:
        diffs['attributes'] = dattrs
   
    # Skills
    dattrs = compare_skills(c1, c2)
    if dattrs: diffs['skills'] = dattrs

    # Feats
    r = compare_feats(c1, c2)
    if r: diffs['feats'] = r

    # Traits
    r = compare_traits(c1, c2)
    if r: diffs['traits'] = r

    # Magic known
    r = compare_spells(c1, c2, 'spellbook')
    if r: diffs['spellbook'] = r
    r = compare_spells(c1, c2, 'spellsknown')
    if r: diffs['spellsknown'] = r

    # Flaws
    r = compare_traits(c1, c2, ['flaws', 'flaw'])
    if r: diffs['flaws'] = r

    # Items
    r = compare_items(c1, c2, 'magicitems')
    if r: diffs['magicitems'] = r

    r = compare_items(c1, c2, 'gear')
    if r: diffs['gear'] = r

    # Settings
    r = compare_books(c1, c2)
    if r: diffs['settings'] = r

    return diffs

def main(fn1, fn2):
    d = get_data(fn1)
    c1 = d['document']['public']['character']
    d = get_data(fn2)
    c2 = d['document']['public']['character']

    diffs = compare_chars(c1, c2)
    print "Diffs", diffs

if __name__ == '__main__':
        main("arc1.xml", "arc2.xml")

