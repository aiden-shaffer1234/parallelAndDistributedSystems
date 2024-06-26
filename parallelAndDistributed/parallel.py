import multiprocessing as mp
import random as r


def func(values, rects):
    count = 0
    x = [r.uniform(values[0],values[1]) for _ in range(10000)]
    y = [r.uniform(values[2],values[3]) for _ in range(10000)]
    z = [r.uniform(values[4],values[5]) for _ in range(10000)]

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

    return count

if __name__ == "__main__":
    
    rects = []
    x   = []
    y   = []
    z   = []
    string = input("number of values and degree of accuracy").split("\t")
    nums = int(string[0])
    accuracy = float(string[1])

    print("enter values")
    
    for _ in range(nums):
        x1, y1, z1, x2, y2, z2 = [float(x) for x in input().split(" ")]

        x += [x1, x2]
        y += [y1, y2]
        z += [z1, z2]

        # check x, y, z
        tup  = ((x1,x2),(y1,y2),(z1,z2))
        rects.append(tup)

    values = (min(x),max(x),min(y),max(y),min(z),max(z))
    pool = mp.Pool(mp.cpu_count())
    num = 150 * 10000

    results = [pool.apply_async(func, args=(values,rects)) for _ in range(150)]

    numInside = 0

    for p in results:
        numInside += p.get()
    
    # delta x * delta y * delta z
    area = (values[1] - values[0]) * (values[3] - values[2]) * (values[5] - values[4])
    ratio = numInside / num * area
    remainder = ratio % accuracy
    ratio -= remainder

    print("{:.3f}".format(ratio))

        






