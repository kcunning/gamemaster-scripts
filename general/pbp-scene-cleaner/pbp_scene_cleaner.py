import csv, glob
import dateutil.parser
from datetime import datetime

#######################################################
#           STUFF YOU WILL WANT TO CHANGE             #
#######################################################

# First, you will need to export your files and put them in the folder `exported_csv`. 
# They MUST be in CSV format, or this script WILL NOT WORK. Export is created by 
# DiscordChatExporter: https://github.com/Tyrrrz/DiscordChatExporter

# `tpl` is the template for your exported files. You'll need to add every category you want to 
# process. 

# If you just want to run a single file, set `fn` to the filename and path, or just have one file 
# in that folder.
tpl = "exported_csv/* - {cat} - *.csv"
# The exported filename format is {Name of your server} - {Category} - {channel} [{channel_id}].csv
# Add every category you want to process to this list.
categories = ['RP Channels']

# Sometimes, you just want to run one channel in a category. Add the channel name to this list.
# channels = ['*secure-group-text-messages*csv', '*kindred-party-line*csv']
channels = ['']

# Start and end dates for the export. Just copy and paste the Date from the CSV, since
# we use dateutil, or use this format: M/D/YYYY H:MM AM/PM. 
# You don't need to set both. If you only set start, we'll go from that time
# until the end of the file, and if you only set end, we'll only process everything from the start
# to that time
start = None
end = None

# If you want to remove OOC comments, set this to true, and make sure your makers are in `ooc_markers`
remove_ooc = True
# The format for each marker is the opening marker, a space, and the end marker. PUT THAT SPACE IN THERE.
ooc_markers = ['(( ))', '[[ ]]', '[ ]']

# If you sometimes do scene breaks by hand, set this to True, and make sure your divider is in `divs`
detect_breaks = True
divs = ["==="]

# If you want to break scenes by number of days the channel has been quiet, set this to the 
# number that works best for you
global max_days
max_days = 5

#######################################################
#           STUFF YOU WILL WANT TO LEAVE ALONE        #
#######################################################

if start and end:
    assert end > start, "Start must be a date before end, if both are set to a date rather than None."

def get_lines(fn):
    ''' Gets the lines from the CSV
    '''
    lines = []
    with open(fn, encoding="utf-8") as f:
        reader = csv.reader(f)
        for line in reader:
            lines.append(line)
    return lines

def get_by_daterange(dds, start, end):
    '''If we're filtering by daterange, return the lines that fit within the range
    '''
    if not start:
        # We gonna party like it's...
        start = datetime(1999, 12, 31)
    if not end:
        end = datetime.now()

    cleaned = []
    for dd in dds:
        t = dateutil.parser.parse(dd['Date'])
        if t >= start and t <= end:
            cleaned.append(dd)

    return cleaned

def detect_scene_breaks(dds, divs=["========"]):
    ''' Returns a list of scenes, where each scene is a list of posts for that scene.

        Scenes are detected two ways: A long pause between posts, or someome adding a scene break.
        The length of the user-added break varies, so there will be some rough logic around it.
    '''
    scenes = []
    scene = []
    for i in range(len(dds)):
        curr = dds[i]
        scene.append(curr)

        # Get the next one, but if we're at the end, just add the last item and move on with life
        try:
            foll = dds[i+1]
        except IndexError:
            scenes.append(scene)
            break

        # Compare the dates
        cdate = dateutil.parser.parse(curr['Date'])
        fdate = dateutil.parser.parse(foll['Date'])
        diff = fdate - cdate

        # If the number of days between the current and the following is low, don't start a new scene
        if diff.days > max_days:
            scenes.append(scene)
            scene = []
            continue

        div_break = False
        for div in divs:
            if div in foll['Content']:
                div_break = True

        if div_break:
            scenes.append(scene)
            scene = []

    return scenes
            
def scrub_ooc(dds, markers="(( ))"):
    ''' PBP often incluses OOC, which we oftend don't need after the scene is over. This
        Removes any text between the given markers.
    '''
    start, end = markers.split(' ')
    cleaned = []
    for dd in dds:
        if start in dd['Content'] and end in dd['Content']:
            # What we need to do is split the string up to the first marker, then after the second marker.
            c1 = dd['Content'][:dd['Content'].find(start)]
            c2 = dd['Content'][dd['Content'].find(end) + len(end):]
            c = c1 + c2
            dd['Content'] = c
        if dd['Content'].strip():
            cleaned.append(dd)
    return cleaned

def create_dict_list(lines):
    ''' Given a list of lines from a CSV, turn them into a list of dictionaries, which are much 
        easier to handle. 
    '''
    hr = lines[0]
    dds = []
    for line in lines[1:]:
        dd = {}
        for i in range(len(hr)):
            dd[hr[i]] = line[i]
        dds.append(dd)
    return dds

def output_lines(fn, dds):
    ''' Split out the lines to a given filename
    '''
    with open(fn, 'w', encoding="utf-8") as f:
        for dd in dds:
            f.write(dd['Content'] + '\n')
            f.write('\n')

# Now we're in the meat of it!

fns = []
for cat in categories:
    fns += glob.glob(tpl.format(cat=cat))
for channel in channels:
    fns += glob.glob(channel)

for fn in fns:
    # Get the lines from the CSV
    lines = get_lines(fn)
    dds = create_dict_list(lines)

    # Get the right date range
    if start or end:
        # Clean the lines for a date range.
        dds = get_by_daterange(dds, start, end)

    # Remove OOC chatter, if that's what we want
    if remove_ooc:
        for marker in ooc_markers:
            dds = scrub_ooc(dds, marker)

    # Detect breaks, if we want, or if not, just put it all in one lump
    if detect_breaks:
        scenes = detect_scene_breaks(dds, divs)
    else:
        scenes = [dds]

    # Export every scene to a file. The filename is the date of the first post and the channel. 
    for scene in scenes:
        server, folder, channel = fn.split(' - ')
        channel = channel.split(' ')[0]
        first_date = dateutil.parser.parse(scene[0]['Date'])
        tpl = "%Y-%m-%d-%H-%M"
        export_fn = "processed_txt/{date}_{channel}.txt".format(
            date=first_date.strftime(tpl),
            channel=channel)
        output_lines(export_fn, scene)