import pprint
import itertools
import networkx as nx
from matplotlib import pyplot as plt
from typing import Set

EN, M, C, PI = ('EN', 'M', 'C', 'Pi')

def label(label, *args):
    return f'{label}{args}'

n = int(input())

var = []

def powerset(s: Set):
    S = []
    s_ = list(s)
    n = len(s)
    for i in range(1 << n):
        S.append(frozenset(s_[j] for j in range(n) if (i & (1 << j))))

    return S

for i in range(1, n+1):
    for j in range(i+1, n+1):
        var.append((C, i, j))

S = powerset([i for i in range(1, n+1)])

for s in S:
    for i in range(1, n+1):
        if i in s:
            continue
        var.append((M, s, i))
        var.append((EN, s, i))

for s in S:
    var.append((PI, s))

var2idx = {
    x[0]: x[1] for x in zip(var, range(len(var)))
}

e = []

for v in var:
    if v[0] == EN:
        e.append(
            (var2idx[(M, v[1], v[2])], var2idx[v])
        )
        
        for x in v[1]:
            e.append(
                (var2idx[(EN, v[1] - {x}, v[2])], var2idx[v])
            )
        
        for (i, j) in itertools.combinations(v[1] | {v[2]}, 2):
            e.append(
                (var2idx[(C, min(i, j), max(i, j))], var2idx[v])
            )
        e.append(
            (var2idx[v], var2idx[(PI, v[1] | {v[2]})])
        )

# G = nx.DiGraph([(var[x[0]], var[x[1]]) for x in e])
# nx.draw_circular(G, with_labels=True)
# plt.show()

print(len(var), len(e))
for (i, j) in e:
    print(i, j)
print(
    var2idx[(C, 1, 2)],
    # var2idx[(PI, frozenset(x for x in range(1, n+1)))]
    var2idx[(PI, frozenset(x for x in range(1, (n+1)//2)))]
)