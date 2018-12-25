from random import shuffle

def get_random_stats(arr):
    stat_names = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    shuffle(arr)

    stats = {}

    for i in range(len(arr)):
        stats[stat_names[i]] = arr[i]

    return stats

def get_top_three(stats):
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
    print "Top:", top
    results = {"exact": [], "partial": []}
    # First, find an exact match.
    for core in cores:
        for arr in cores[core]:
            if top == arr:
                results['exact'].append(core)
            elif top[0] == arr[0] and top[1] == arr[1]:
                results['partial'].append(core)
    return results

def main():
    basic_arr = [13, 12, 11, 10, 9, 8]
    heroic_arr = [15, 14, 13, 12, 10, 8]

    while True:
        stats = get_random_stats(basic_arr)

        results = get_potential_class(stats)

        if results['exact'] or results['partial']:
            break

    print stats
    print results

if __name__ == '__main__':
    main()