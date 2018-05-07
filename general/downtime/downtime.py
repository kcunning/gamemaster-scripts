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

def get_event(table, val):
    keys = t.keys()
    keys.sort()
    # Go until you find the min that's too much
    for i in range(len(keys)):
        if val < keys[i] and i != 0:
            return keys[i-1]
        elif val < keys[i]:
            return keys[0]
    return keys[-1]

