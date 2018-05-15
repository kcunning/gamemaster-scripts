''' A script to help run the downtime rules from Pathfinder 

Official rules: 
    http://paizo.com/pathfinderRPG/prd/ultimateCampaign/downtime.html
Source for this script (better formatting): 
    https://www.d20pfsrd.com/gamemastering/other-rules/downtime/
'''

from random import randint
import os, sys

def get_roll_table(filename):
    ''' The format for the roll table file:
            - Values are tab separated
            - Each row contains:
                - Min roll
                - Max roll
                - Title
                - Description (optional)
        A dict is returned, with the min roll as the key. 
    '''
    with open(filename) as f:
        lines = f.readlines()

    table = {}
    for line in lines:
        vals = line.split('\t')
        row = {'min': int(vals[0]), 'max': int(vals[1]), 'title': vals[2].strip()}
        if len(vals) > 3:
            row['desc'] = vals[3].strip()
        else:
            row['desc'] = ''
        table[int(vals[0])] = row
    return table

def select_table(dir="tables"):
    tables = os.listdir('tables')
    for table in tables:
        if 'generic' in table:
            tables.remove(table)
    while True:
        print "Select a table:"
        for i in range(len(tables)):
            print i, "-", tables[i]
        c = raw_input("Num: ")
        if not c.isdigit() or int(c) > len(tables) -1 or int(c) < 0:
            print c, "is not valid."
        else:
            table = tables[int(c)]
            return "tables/" + table

def print_row(row):
    tpl = "{min}-{max} {title}"
    print tpl.format(
        min=row['min'],
        max=row['max'],
        title=row['title']),

    if row['desc']:
        print "--", row['desc']
    else:
        print 

def print_tsv(vals):
    keys = vals[0].keys()
    keys.extend(['influence bonus', 'capital bonus', 'labor bonus', 'other'])
    print "\t".join(keys)
    for val in vals:
        for key in keys:
            if key in val:
                print val[key], " \t ",
        print

def get_event(table, val):
    keys = table.keys()
    keys.sort()
    # Go until you find the min that's too much
    for i in range(len(keys)):
        if val < keys[i] and i != 0:
            return keys[i-1]
        elif val < keys[i]:
            return keys[0]
    return keys[-1]

def check_event_type(table, i):
    ''' Some rows require a re-roll on another table.
    '''
    # Building specific event?
    pass

def main():
    print "Starting a new downtime session!"
    while True:
        num = raw_input("How many days? ")
        if not num.isdigit():
            print num, "is not valid."
            num = raw_input("How many days? ")
        else:
            break

    days = []
    # filename = select_table()
    table = get_roll_table("tables/generic_building_events.txt")
    print "What building type?"
    bfile = select_table()
    btable = get_roll_table(bfile)
    for i in range(int(num)):
        print "Working on day", i + 1
        r = randint(1, 101)
        e = get_event(table, r)
        if table[e]['title'].lower() == "building-specific event":
            print "Building specific event..."
            r = randint(1, 101)
            e = get_event(btable, r)
            days.append(dict(btable[e]))
            days[-1]['table'] = bfile
            days[-1]['day'] = i + 1
            print_row(btable[e])
            continue
        if table[e]['title'].lower() =="roll twice":
            print "Rolling twice..."
            for j in [1, 2]:
                print "Roll", j
                r = randint(1, 101)
                e = get_event(table, r) 
                if table[e]['title'].lower() == "building-specific event":
                    print "Building specific event..."
                    r = randint(1, 101)
                    e = get_event(btable, r)
                    days.append(dict(btable[e]))
                    days[-1]['table'] = bfile
                    days[-1]['day'] = i + 1
                    print_row(btable[e])
                else:
                    days.append(dict(table[e]))
                    days[-1]['table'] = "generic"
                    days[-1]['day'] = i + 1
                    print_row(table[e])
            continue

        days.append(dict(table[e]))
        days[-1]['table'] = "generic"
        days[-1]['day'] = i + 1
        print_row(table[e])

    return days

results = main()
print "*"*20
print_tsv(results)


