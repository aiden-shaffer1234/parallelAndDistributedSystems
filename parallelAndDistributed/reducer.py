import sys

count = 0
total = 0
area = 0
accuracy = 0
for line in sys.stdin:
    count += 1
    line = line.strip()
    area, accuracy, count_in = line.split(" ")
    area = float(area)
    accuracy = float(accuracy)
    count_in = int(count_in)

    total += count_in

ratio = total / (count * 10000)
ratio *= area
remainder = ratio % accuracy
ratio -= remainder

print("{:.3f}".format(ratio))
