import json
from pprint import pprint

f = open("data/general_feats.txt")
lines = f.readlines()
f.close()

# pprint(lines)

# feats = {}
# i = 0
# while i < len(lines):
#     # Assume first line is title of the feat
#     ttl = lines[i].strip()
#     print ("Title", ttl)
#     d = ''
#     i += 1
#     while i < len(lines):
#         line = lines[i].strip()
#         if not line:
#             i += 1
#             feats[ttl] = {'description': d}
#             break
#         else:
#             d += line
#             i += 1

# with open('data/general_feats.json', 'w') as dumpfile:
#     json.dump(feats, dumpfile, indent=4)

with open('data/general_feats.json') as f:
    jfeats = json.load(f)

for feat in jfeats:
    print(feat)
