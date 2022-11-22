import operator
from typing import List

def dfs(
    in_: List[List[int]],
    out: List[List[int]],
    visited: List[bool],
    v: int,
    rev: bool
):
    visited[v] = True
    adj = in_ if rev else out
    for u in adj[v]:
        if not visited[u]:
            dfs(in_, out, visited, u, rev)

n, m = [int(x) for x in input().split()]

in_ = [[] for _ in range(n+1)]
out = [[] for _ in range(n+1)]

for _ in range(m):
    u, v = [int(x) for x in input().split()]
    out[u].append(v)
    in_[v].append(u)

src, dest = [int(x) for x in input().split()]

visited_1 = [False for _ in range(n+1)] 
visited_2 = [False for _ in range(n+1)]

dfs(in_, out, visited_1, src, False)
dfs(in_, out, visited_2, dest, True)

onpath = list(map(operator.and_, visited_1, visited_2))

for i in range(1, n+1): 
    for j in out[i]:
        onpath[i] |= onpath[j]

print(*[int(x) for x in onpath])