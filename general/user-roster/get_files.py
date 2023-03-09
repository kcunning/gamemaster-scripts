import sys, os
from datetime import datetime, timedelta

disco_path = "C:\\Users\\katie\\projects\\gamemaster-scripts\\general\\user-roster\\DiscordChatExporter.CLI\\DiscordChatExporter.Cli.exe"
token = "NDg1MTQ0NDgzNTI5NDkwNDQz.GdU54Z.VV3QUlOTUVtMWs5dllGT0djZTFiLTF4aEVZQUo3T0p5MkducUY2bnR4bS1wYzBmZDBHTUVzN0RGOFF3TDE3ZXZSQ2xqUmlpLUwxR1RjSHRQ"
guild = "518199891982286858"
# guild = "746341796686069820" #DbD
intro_id = "654109188548591616"

start = datetime.now() - timedelta(days=60)

print(start)

os.system("{exe} channels -t {t} -g {g}".format(exe=disco_path, t=token, 
    g=guild))

# De comment this later
# os.system("{exe} exportguild -t {t} -g {g} --after {start}".format(exe=disco_path, t=token, 
#     g=guild, start=start.strftime("%m/%d/%Y")))

os.system("{exe} exportguild -t {t} -g {g}".format(exe=disco_path, t=token, 
    g=guild))

# os.system("{exe} exportguild -t {t} -g {g}".format(exe=disco_path, t=token, 
#     g=guild))

# os.system("{exe} exportguild -t {t} -g {g}".format(exe=disco_path, t=token, 
#     g=guild))

# Decomment this later
# os.system("{exe} export -t {t} -c {i} -o introduce-all-time.html".format(exe=disco_path, t=token, 
#     i=intro_id))