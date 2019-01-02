from random import shuffle

def get_random_stats(arr):
    ''' Given a list of numbers (n=6), returns a dictionary of random stats. 
    '''
    stat_names = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    shuffle(arr)

    stats = {}

    for i in range(len(arr)):
        stats[stat_names[i]] = arr[i]

    return stats

def get_top_three(stats):
    ''' Returns the highest three stats from the stats dict
    '''
    v = stats.values()
    v.sort()
    v.reverse()

    top = []
    for i in v[:3]:
        for stat in stats:
            if stats[stat] == i:
                top.append(stat)
                continue
    return top

def get_potential_class(stats):
    ''' In theory, I should be able to suggest a class for the NPC
        based on their random stats.

        I got the stat suggestions from
        http://triangularroom.com/2015/09/30/pathfinder-for-beginners-ability-scores-by-class/
        
        It's only a suggestion, but still faster than looking up classes 
        in the book
    '''
    cores = {
        "barbarian": [['STR','CON','DEX']],
        "bard": [['CHA', 'DEX', 'CON']],
        "cleric": [['WIS', 'CHA', 'STR'], ['WIS', 'CHA', 'DEX']],
        "druid": [['WIS', 'DEX', 'CON']],
        "fighter": [['STR', 'CON', 'DEX']],
        "monk": [['STR', 'WIS', 'CON']],
        "paladin": [['STR', 'CHA', 'CON']],
        "ranger": [['DEX', 'WIS', 'INT'], ['STR', 'WIS', 'INT']],
        "rogue": [['DEX', 'CON', 'WIS']],
        "sorcerer": [['CHA', 'DEX', 'CON']],
        "wizard": [['INT', 'DEX', 'CON']]
    }

    top = get_top_three(stats)
    results = {"exact": [], "partial": []}
    for core in cores:
        for arr in cores[core]:
            if top == arr:
                results['exact'].append(core)
            elif top[0] == arr[0] and top[1] == arr[1]:
                results['partial'].append(core)
            elif top == [arr[0], arr[2], arr[1]]:
                results['partial'].append(core)
    return results

def print_results(stats, cldict):
    ''' Prints out the stats and potential classes all nice like.
    '''
    print "STR: {STR} DEX: {DEX} CON: {CON}".format(**stats)
    print "INT: {INT} WIS: {WIS} CHA: {CHA}".format(**stats)
    print "Classes with exact matches:"
    if not cldict['exact']:
        print "\tNone"
    else:
        print "\t" + ", ".join(cldict['exact'])
    print "Classes with partial matches:"
    if not cldict['partial']:
        print "\tNone"
    else:
        print "\t" + ", ".join(cldict['partial'])

def main():
    ''' The meat and potatoes. For now, just sends the basic array.
    '''
    basic_arr = [13, 12, 11, 10, 9, 8]
    heroic_arr = [15, 14, 13, 12, 10, 8]

    # Keep going until you get a random character with at least
    # one partial match or one exact match
    while True:
        stats = get_random_stats(basic_arr)

        results = get_potential_class(stats)

        if results['exact'] or results['partial']:
            break

    print_results(stats, results)

if __name__ == '__main__':
    main()