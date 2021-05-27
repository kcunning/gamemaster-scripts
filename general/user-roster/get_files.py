import sys, os
from datetime import datetime, timedelta


disco_path = "C:\\Users\\katie\\OneDrive\\Desktop\\DiscordChatExporter.CLI\\DiscordChatExporter.Cli.exe"
token = "NDg1MTQ0NDgzNTI5NDkwNDQz.Xl7AOw.6F2mx05KDqxgOstohXHf2EqV8OQ"
guild = "518199891982286858"
intro_id = "654109188548591616"

start = datetime.now() - timedelta(days=90)

print(start)

# os.system("{exe} channels -t {t} -g {g}".format(exe=disco_path, t=token, 
#     g=guild, start=start.strftime("%m/%d/%Y")))

os.system("{exe} exportguild -t {t} -g {g} --after {start}".format(exe=disco_path, t=token, 
    g=guild, start=start.strftime("%m/%d/%Y")))

os.system("{exe} export -t {t} -c {i} -o introduce-all-time.html".format(exe=disco_path, t=token, 
    i=intro_id))