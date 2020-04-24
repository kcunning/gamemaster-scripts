from skills import base

def dwarf(ch):
    # Apply stat changes
    ch.stats['CON'] += 2
    ch.stats['INT'] += 2
    ch.stats['CHA'] -= 2

    # Apply Size and type
    ch.size = "Average"
    ch.type = "Humanoid"
    ch.movement = 30

    # Apply skill changes
    ch.skills['Engineering'] += 1 + 1 + ch.level // 8

    # Apply vision changes
    ch.vision = "Darkvision"

    # Bonus feats
    # TODO: Add feats

    return ch

def elf(ch):
    # Apply stat changes
    ch.stats['DEX'] += 2
    ch.stats[ch.init_stat_bonus] += 2
    ch.stats['CON'] -= 2

    # Apply Size and type
    ch.size = "Average"
    ch.type = "Humanoid"
    ch.movement = 30

    # Apply skill changes
    ch.skills['Nature'] += 1 + ch.level // 8
    # Apply vision changes
    ch.vision = "Ghostwise Sight - 45 ft"

    # Bonus feats
    # TODO: Add feats

    return ch

def halfling(ch):
    # Apply stat changes
    ch.stats['DEX'] += 2
    ch.stats[ch.init_stat_bonus] += 2
    ch.stats['CON'] -= 2

    # Apply Size and type
    ch.size = "Average"
    ch.type = "Humanoid"
    ch.movement = 30

    # Apply skill changes
    ch.skills['Nature'] += 1 + ch.level // 8
    # Apply vision changes
    ch.vision = "Ghostwise Sight - 45 ft"

    # Bonus feats
    # TODO: Add feats

    return ch

def halfling(ch):
    # Apply stat changes
    ch.stats['DEX'] += 2
    ch.saves['Will'] += 1

    # Apply Size and type
    ch.size = "Small"
    ch.type = "Humanoid"
    ch.movement = 30

    # Apply skill changes
    ch.skills['Nature'] += 1 + ch.level // 8

    # Apply vision changes

    # Bonus feats
    # TODO: Add feats

    return ch

def human(ch):
    # Apply stat changes
    ch.stats[ch.init_stat_bonus] += 2

    # Apply Size and type
    ch.size = "Average"
    ch.type = "Humanoid"
    ch.movement = 30

    # Apply skill changes
    ch.skills[ch.init_skill_bonus] += 1 + ch.level // 8
    # Apply that extra bonus
    # Attack?
    if ch.init_extra_bonus == 'Attack':
        ch.bab += 1
    # AC?
    elif ch.init_extra_bonus == 'AC':
        ch.ac += 1
    # Saving throw?
    else:
        # Assume it's a save
        ch.saves[ch.init_extra_bonus] += 1

    # Bonus feats
    # TODO: Add feats

    return ch

def orc(ch):
    # Apply stat changes
    ch.stats['STR'] += 2
    ch.stats['CON'] += 2
    ch.stats['CHA'] -= 2

    # Apply Size and type
    ch.size = "Average"
    ch.type = "Humanoid"
    ch.movement = 30

    # Apply vision
    ch.vision = 'Darkvision'

    # Apply skill changes
    ch.skills['Athletics'] += 1 + ch.level // 8

    # Bonus feats
    # TODO: Add feats

    return ch