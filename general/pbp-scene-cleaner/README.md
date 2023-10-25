Play-by-post Scene Cleaner
==========================
The purpose of this script is to clean up exported files from a PBP Discord server. While PBP can be a ton of fun for the TTRPG lover, they pose a problem when it comes to reading over old posts. They're often littered with OOC comments, and switching channels can cause you to lose your place. Also, figuring out a sequential order for scenes can be rough, since it's not uncommon for servers to have dozens of active channels at a time.  

Features
--------
* Breaks scenes out into text files based on scene break markers or by time since the last post
* Removes OOC text that has been bracketed
* Processes only categories / channels set by the user
* Can filter by date

Quirks / Bugs I'll solve later, or maybe never
------
* If a scene break marker is part of a post, it sometimes ends up in the next scene.
* If DiscordChatExporter changes its `csv` formatting, this script will more than likely epically fail. 

Requires
--------
* Python 3+ (Written in 3.11.3, but it should be fine in earlier versions)
* DiscordChatExporter (https://github.com/Tyrrrz/DiscordChatExporter) for the raw exports

Notes
-----
Running this script requires some ability to edit some variables. These are all called out in the script under the first section. Read the comments! 

Also, this script will **not** create the exported files. You have to use DiscordChatExporter (above) to get them. The format **must** be `csv`, and they need to be put in `exported_csv`  unless you update the script to point to a new directory. 