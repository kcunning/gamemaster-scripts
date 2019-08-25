test_data = [
    ['bg', 'bg', 'bg', 'bg', 'bg'],
    ['bg', 'NW', 'N', 'NE', 'bg'],
    ['bg', 'W', 'bg', 'E', 'bg'],
    ['bg', 'SW', 'S', 'SE', 'bg'],
    ['bg', 'bg', 'bg', 'bg', 'bg'],
]

boxw = 70
boxh = 70

paths = []

for ri in range(len(test_data)):
    for ci in range(len(test_data[ri])):
        val = test_data[ri][ci]
        if val == "N":
            paths.append([
                [ci * boxw, ri * boxh], 
                [ci * boxw + boxw, ri * boxh]])

        if val == "NW":
            paths.append([
                [ci * boxw, ri * boxh + 70],
                [ci * boxw, ri * boxh], 
                [ci * boxw + boxw, ri * boxh]])

print(paths)
