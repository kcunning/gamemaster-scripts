#-*- coding: utf-8 -*-

import csv, sys, os

from PIL import Image

# To do:
#  - Add doors to image
#  - Add door types to console
#  - Figure out what a room is, since tsv doesn't contain that
#  - Populate the dungeon

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
    ew_door = "\N{LEFTWARDS ARROW}\N{RIGHTWARDS ARROW}"
    ns_door = "\N{UPWARDS ARROW}\N{DOWNWARDS ARROW}"
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
    if north and south:
        return ns_door
    if east and west:
        return ew_door

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

    # Do we need a wall to the south
    if line[c] and next_line and not next_line[c]:
        s += "S"

    # Do we need a wall to the east?
    if line[c] and c != len(line)-1 and not line[c+1]:
        s += "E"
    
    # Do we need a wall to the west?
    if line[c] and c != 0 and not line[c-1]:
        s += "W"

    

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
    for r in range(len(lines)-1):
        line = lines[r]
        for c in range(len(line)-1):
            s = lines[r][c]
            x = c * 40
            y = r * 40
            off = 0
            if s in tiles.keys():
                map_image.paste(tiles[s], (x-off, y-off))
            else:
                map_image.paste(tiles['floor'], (x-off, y-off))

    # Overlay the corners
    for r in range(len(lines)-1):
        line = lines[r]
        for c in range(len(line)-1):
            s = lines[r][c]
            # if s != "floor":
            #     continue
            north = lines[r-1][c]
            south = lines[r+1][c]
            east = lines[r][c+1]
            west = lines[r][c-1]

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

    map_image.save(os.path.abspath("output/test_image.png"), "PNG")

def main(fn="dungeon1.tsv", out="all"):
    lines = get_lines(fn)
    if out in ["all", "console"]:
        print_dungeon(lines)

    if out in ["all", "image"]:
        matrix = create_map_matrix(lines)
        create_map_image(matrix)

if __name__ == "__main__":
    main()