import re

cont = True

while cont:
    print("Enter/Paste your content. 'x' to quit completely.")
    contents = []
    while True:
        line = input()
        if line == '':
            break
        if line == 'x':
            cont = False
        contents.append(line)

    txt = " ".join(contents)

    words = txt.split(' ')

    regex = re.compile(r'^[0-9]+d[0-9]+')
    for word in words:
        if regex.match(word):
            print("Found dice roll", word)
            txt = txt.replace(word, "[[{w}]]".format(w=word))

    print(txt)

