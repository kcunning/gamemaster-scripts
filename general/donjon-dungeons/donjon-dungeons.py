#-*- coding: utf-8 -*-

import csv, sys, os

from PIL import Image

# To do:
#  - Add stairs up and stairs down
#  - Figure out what a room is, since tsv doesn't contain that
#  - Populate the dungeon
#  - Get image size from the actual image rather than hard-coding it
#  - Fix the issue where we need a blank first and last row
#  - A player map (don't show what doors are locked / trapped / secret / fine)
#  - Command line options

def get_lines(fname, delimiter="\t"):
    ''' Gets the lines from a file and cleans them up.
    '''
    lines = []
    with open(fname) as f:
        reader = csv.reader(f, delimiter=delimiter)
        for line in reader:
            lines.append(line)

    return lines

def get_door_char(lines, r, c):
    ''' Returns the correct character for a door

        This is incomplete, since it just works with the console
        output, and doesn't return anything special for special doors
        (secret, locked, etc)
    '''
    line = lines[r]
    prev_line = lines[r-1] if r != 0 else None
    next_line = lines[r+1] if r != len(lines) - 1 else None
    door_types = ['DL', 'DST', 'DT']
    doors = {
        'DL_EW': "\N{LEFTWARDS ARROW FROM BAR}\N{RIGHTWARDS ARROW FROM BAR}",
        'DL_NS': "\N{UPWARDS ARROW FROM BAR}\N{DOWNWARDS ARROW FROM BAR}",
        'DST_NS': "\N{UPWARDS ARROW TO BAR}\N{DOWNWARDS ARROW TO BAR}",
        'DST_EW': "\N{LEFTWARDS ARROW TO BAR}\N{RIGHTWARDS ARROW TO BAR}",
        'DT_NS': "\N{WHITE FROWNING FACE}\N{UP DOWN ARROW}",
        'DT_EW': "\N{WHITE FROWNING FACE}\N{LEFT RIGHT ARROW}",
        'D_NS': "\N{UPWARDS ARROW}\N{DOWNWARDS ARROW}",
        'D_EW': "\N{LEFTWARDS ARROW}\N{RIGHTWARDS ARROW}"
    }
    ew_door = "\N{LEFTWARDS ARROW}\N{RIGHTWARDS ARROW}"
    ns_door = "\N{UPWARDS ARROW}\N{DOWNWARDS ARROW}"
    secret_ew = "\N{LEFTWARDS ARROW TO BAR}\N{RIGHTWARDS ARROW TO BAR}"
    secret_ns = "\N{UPWARDS ARROW}\N{DOWNWARDS ARROW}"
    trap_ew = "\N{LEFTWARDS ARROW}\N{RIGHTWARDS ARROW}"
    trap_ns = "\N{UPWARDS ARROW}\N{DOWNWARDS ARROW}"
    locked_ew = "\N{LEFTWARDS ARROW}\N{RIGHTWARDS ARROW}"
    locked_ns = "\N{UPWARDS ARROW}\N{DOWNWARDS ARROW}"
    if not prev_line or not next_line:
        # If this is the first or last row, we can assume that it's an EW door
        return ew_door

    if c == 0 or c == len(line) - 1:
        return ns_door
    # Get the symbols above and below
    north = prev_line[c]
    south = next_line[c]
    east = line[c-1]
    west = line[c+1]
    
    if line[c] in door_types:
        dt = line[c]
    else:
        dt = 'D'

    if north and south:
        return doors[dt + "_NS"]
    if east and west:
        return doors[dt + "_EW"]

    # Default door, just in case.
    return "++"

def get_nsew(lines, r, c, t=""):
    ''' Gets where we need walls. If the cell next to a target cell is blank,
        then where they touch needs a wall.

        Note: The order is always assumed to be NSEW, with letters removed
        if you don't need that wall. NEW is fine. NWE will not work.

        At the moment, `t` isn't used
    '''
    prev_line = lines[r-1] if r != 0 else None
    next_line = lines[r+1] if r != len(lines) - 1 else None
    line = lines[r]

    # The final string should be, in order, NSEW. If you remove a letter,
    # the order should remain the same.

    s = t

    # Do we need a wall to the north?
    if line[c] and prev_line and not prev_line[c]:
        s += "N"
    elif line[c] == "F" and not prev_line:
        s += "N"

    # Do we need a wall to the south
    if line[c] and next_line and not next_line[c]:
        s += "S"
    elif line[c] == "F" and not next_line:
        s += "S"

    # Do we need a wall to the east?
    if line[c] and c != len(line)-1 and not line[c+1]:
        s += "E"
    
    # Do we need a wall to the west?
    if line[c] and c != 0 and not line[c-1]:
        s += "W"

    # Check for doors. Presume that there are no walls around doors
    if line[c].startswith("D"):
        dtypes = ['DT', 'DL', 'DST']
        dtype = 'd' if not line[c] in dtypes else line[c].lower()
        if not prev_line or not next_line:
            # If this is the first or last row, we can assume that it's an EW door
            s =  dtype + "EW"

        elif c == 0 or c == len(line) - 1:
            s = dtype + "NS"
        else:
            north = prev_line[c]
            south = next_line[c]
            east = line[c-1]
            west = line[c+1]
            if north and south:
                s = dtype + "NS"
            if east and west:
                s = dtype + "EW"

    if line[c] and s == t:
        s += "floor"

    if not line[c] and s == t:
        s += "bg"

    return s


def get_floor(lines, r, c):
    ''' Just a function to return the unicode characters for
        the floor.
    '''
    return "\N{FULL BLOCK}\N{FULL BLOCK}" 

def print_dungeon(lines):
    ''' Prints out the dungeon to the console.
    '''
    for r in range(len(lines)):
        line = lines[r]
        for c in range(len(line)):
            s = line[c]
            if s=="F":
                w = get_floor(lines, r, c)
                print(w, end="")
            elif s.startswith("D"):
                d = get_door_char(lines, r, c)
                print(d, end="")
            else:
                print("  ", end="")
        print()

def create_map_matrix(lines):
    ''' Creates a matrix out of the raw map data. Each cell contains what
        sort of walls that square needs, or if it is a floor or background
        square
    '''
    matrix = []
    for r in range(len(lines)):
        row = []
        line = lines[r]
        for c in range(len(line)):
            s = get_nsew(lines, r, c)
            row.append(s)
        matrix.append(row)

    return matrix

def create_map_image(lines, style="base"):
    ''' Creates an image based off of the TSV and outputs it to an output
        folder.

        TODO: Better output file name.
        TODO: Actually use the style param
    ''' 
    imgdir = os.path.abspath("images/base/")
    outdir = os.path.abspath("output/")
    files = os.listdir(imgdir)
    png_files = filter(lambda x: x.endswith(".png"), files)

    # Get the tiles
    tiles = {}
    for fn in png_files:
        imgpath = os.path.abspath("images/base/" + fn)
        tiles[fn.split(".")[0]] = Image.open(imgpath)

    img_h = len(lines) * 40
    img_w = len(lines[0]) * 40

    map_image = Image.new("RGB", (img_w, img_h))

    # Lay down the walls
    for r in range(len(lines)):
        line = lines[r]
        for c in range(len(line)):
            s = lines[r][c]
            x = c * 40
            y = r * 40
            off = 0
            if s in tiles.keys():
                map_image.paste(tiles[s], (x-off, y-off))
            else:
                map_image.paste(tiles['floor'], (x-off, y-off))

    # Overlay the corners
    for r in range(len(lines)):
        line = lines[r]
        for c in range(len(line)):
            s = lines[r][c]
            # if s != "floor":
            #     continue
            north = lines[r-1][c]
            west = lines[r][c-1]
            east = lines[r][c+1] if not c+1 == len(line) else ""
            south = lines[r+1][c] if not r+1 == len(lines) else ""


            x = c * 40
            y = r * 40
            off = 0
            # Check for the SE corner
            if "E" in south and "S" in east:
                map_image.paste(tiles['cSE'], (x, y), tiles['cSE'])
            # Check for the NE corner
            if "N" in east and "E" in north:
                map_image.paste(tiles['cNE'], (x, y), tiles['cNE'])
            # Check for the SW corner
            if "S" in west and "W" in south:
                map_image.paste(tiles['cSW'], (x, y), tiles['cSW'])
            # Check for the NW corner
            if "N" in west and "W" in north:
                map_image.paste(tiles['cNW'], (x, y), tiles['cNW'])

            # Do the whole thing again for the doors
            if s.startswith('d') and s.endswith('EW'):
                map_image.paste(tiles['cSE'], (x-40, y), tiles['cSE'])
                map_image.paste(tiles['cNE'], (x-40, y), tiles['cNE'])
                map_image.paste(tiles['cSW'], (x+40, y), tiles['cSW'])
                map_image.paste(tiles['cNW'], (x+40, y), tiles['cNW'])

            if s.startswith('d') and s.endswith('NS'):
                map_image.paste(tiles['cSE'], (x, y-40), tiles['cSE'])
                map_image.paste(tiles['cNE'], (x, y+40), tiles['cNE'])
                map_image.paste(tiles['cSW'], (x, y-40), tiles['cSW'])
                map_image.paste(tiles['cNW'], (x, y+40), tiles['cNW'])


    map_image.save(os.path.abspath("output/test_image.png"), "PNG")

def main(fn="dungeon1.tsv", out="all"):
    lines = get_lines(fn)
    if out in ["all", "console"]:
        print_dungeon(lines)

    if out in ["all", "image"]:
        matrix = create_map_matrix(lines)
        print(matrix)
        create_map_image(matrix)

if __name__ == "__main__":
    main()