import sys
import random as r

# input comes from STDIN (standard input)

#pre processor
num = 0
accuracy = 0
rects = []
x = []
y = []
z = []

for line in sys.stdin:
    line = line.strip()
    line = line.split("\t")
    if len(line) < 6:
        num = int(line[0])
        accuracy = float(line[1])
    else:
        x1, y1, z1, x2, y2, z2 = [float(x) for x in line]

        x += [x1, x2]
        y += [y1, y2]
        z += [z1, z2]
        # check x, y, z
        tup  = ((x1,x2),(y1,y2),(z1,z2))
        rects.append(tup)
    
bounds = (min(x),max(x),min(y),max(y),min(z),max(z))
area = (bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) * (bounds[5] - bounds[4])
#mapper

count = 0
x = [r.uniform(bounds[0],bounds[1]) for _ in range(10000)]
y = [r.uniform(bounds[2],bounds[3]) for _ in range(10000)]
z = [r.uniform(bounds[4],bounds[5]) for _ in range(10000)]

for i in range(10000):
    inside = False
    for rect in rects:
        if x[i] >= min(rect[0]) and x[i] <= max(rect[0]):
            if y[i] >= min(rect[1]) and y[i] <= max(rect[1]):
                if z[i] >= min(rect[2]) and z[i] <= max(rect[2]):
                    inside = True
                    break
    if inside:
        count += 1

print(str(area) + " " + str(accuracy) + " " + str(count))