import random

n = int(input())
p = float(input())

e = []
for i in range(1, n+1):
    for j in range(i+1, n+1):
        if random.random() < p:
            e.append((i, j))

print(n, len(e))
for (i, j) in e:
    print(i, j)
print(1, n)