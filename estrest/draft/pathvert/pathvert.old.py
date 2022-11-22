def pathvert(adj, visited, onpath, dest, v):
    visited[v] = True
    if v == dest:
        onpath[v] = True
    for u in adj[v]:
        if not visited[u]:
            onpath[v] |= pathvert(adj, visited, onpath, dest, u)
        else:
            onpath[v] |= onpath[u]
    return onpath[v]

n, m = [int(x) for x in input().split()]

adj = [[] for _ in range(n+1)]

for _ in range(m):
    u, v = [int(x) for x in input().split()]
    adj[u].append(v)

src, dest = [int(x) for x in input().split()]

visited = [False for _ in range(n+1)] 
onpath = [False for _ in range(n+1)]

pathvert(adj, visited, onpath, dest, src)

print(*[int(x) for x in onpath])
