#-*- coding: utf-8 -*-

import csv, sys, os

from PIL import Image

# To do:
#  - Add doors to image
#  - Add door types to console
#  - Corners?!

def get_lines(fname):
    lines = []
    with open(fname) as f:
        reader = csv.reader(f, delimiter="\t")
        for line in reader:
            lines.append(line)

    return lines

def get_door_char(lines, r, c):
    # Doors we need
    # - Room to N and S
    # - Room to E and W
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
    
    return "++"

def get_nsew(lines, r, c, t=""):
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

    return "\N{FULL BLOCK}\N{FULL BLOCK}" 

def print_dungeon(lines):
    for r in range(len(lines)):
        line = lines[r]
        # print(line)
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

def create_map_image(lines, style="base"):
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
    print(tiles)

    for r in range(len(lines)-1):
        line = lines[r]
        for c in range(len(line)-1):
            s = get_nsew(lines, r, c)
            x = c * 40
            y = r * 40
            if s in tiles:
                map_image.paste(tiles[s], (x, y))
            else:
                map_image.paste(tiles['floor'], (x, y))
            print(s, end="\t")
        print()

    map_image.save(os.path.abspath("output/test_image.png"), "PNG")


lines = get_lines("dungeon1.tsv")
print_dungeon(lines)
create_map_image(lines)