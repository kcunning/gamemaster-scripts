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
        "fighter": [['STR', 'CON', 'DEX'], ['STR', 'DEX', 'CON']],
        "monk": [['STR', 'WIS', 'CON']],
        "paladin": [['STR', 'CHA', 'CON']],
        "ranger": [['DEX', 'WIS', 'INT'], ['STR', 'WIS', 'INT']],
        "rogue": [['DEX', 'CON', 'WIS']],
        "sorcerer": [['CHA', 'DEX', 'CON']],
        "wizard": [['INT', 'DEX', 'CON']]
    }

    advs = {
        "alchemist": [['INT', 'DEX', 'CON']],
        "cavalier": [['STR', 'CON', 'DEX']],
        "samurai": [['STR', 'CON', 'DEX']],
        "gunslinger": [['DEX', 'WIS', 'CON']],
        "inquisitor": [['DEX', 'WIS', 'CON']],
        "magus": [['STR', 'INT', 'CON']],
        "oracle": [['CHA', 'STR', 'CON']],
        "summoner": [['CHA', 'DEX', 'CON']],
        "witch": [['INT', 'DEX', 'CON']],
        "archanist": [['INT', 'CHA', 'DEX']],
        "bloodranger": [['STR', 'CON', 'CHA']],
        "brawler": [['STR', 'CON', 'DEX']],
        "hunter": [['WIS', 'DEX', 'CON']],
        "investigator": [['STR', 'INT', 'DEX']],
        "shaman": [['WIS', 'CHA', 'CON']],
        "skald": [['STR', 'CHA', 'CON']],
        "swashbuckler": [['DEX', 'CHA', 'CON']],
        "warpriest": [['STR', 'WIS', 'CON']],
        "vigilante": [["CHA", "DEX", "CON"]]
    }

    occults = {
        "kineticist": [["CON", "DEX", "WIS"]],
        "medium": [["CHA", "DEX", "CON"]],
        "mesmerist": [["CHA", "DEX", "CON"]],
        "occultist": [["INT", "STR", "DEX"]],
        "psychic": [["INT", "WIS", "DEX"], ["INT", "CHA", "DEX"]],
        "spiritualist": [["WIS", "DEX", "CON"]],
    }

    all_classes = {}
    all_classes.update(cores)
    all_classes.update(advs)
    all_classes.update(occults)

    top = get_top_three(stats)
    results = {"exact": [], "partial": []}
    for name in all_classes:
        for arr in all_classes[name]:
            if top == arr:
                results['exact'].append(name)
            elif top[0] == arr[0] and top[1] == arr[1]:
                results['partial'].append(name)
            elif top == [arr[0], arr[2], arr[1]]:
                if not name in results['partial'] and not name in results['exact']:
                    results['partial'].append(name)
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