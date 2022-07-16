def floyd_warshall(dist):
    v = len(dist)
    for k in range(v):
        for i in range(v):
            for j in range(v):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])


def dijkstra(G, s):
    from heapq import heappush, heappop

    INF = 10**18
    dist = [INF] * len(G)
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, v = heappop(pq)
        if d > dist[v]:
            continue
        for u, weight in G[v]:
            nd = d + weight
            if dist[u] > nd:
                dist[u] = nd
                heappush(pq, (nd, u))
    return dist


def bfs(G, s):
    from collections import deque

    INF = 10**18
    dist = [INF] * len(G)
    dist[s] = 0
    que = deque([0])
    while que:
        v = que.popleft()
        for u in G[v]:
            if dist[u] == INF:
                dist[u] = dist[v] + 1
                que.append(u)
    return dist


# returns None if the graph contains a negative cycle
def bellman_ford(G, V, s):
    INF = 10**18
    dist = [INF] * V
    dist[s] = 0
    for i in range(V):
        for u, v, weight in G:
            if dist[v] > dist[u] + weight:
                dist[v] = dist[u] + weight
                if i == V - 1:
                    return None
    return dist


def prim(dist):
    n = len(dist)
    INF = 10**18
    min_cost = [0] + [INF] * (n-1)
    used = [False] * n
    ret = 0
    while True:
        v = -1
        for u in range(n):
            if not used[u] and (v == -1 or min_cost[u] < min_cost[v]):
                v = u
        if v == -1:
            break
        used[v] = True
        ret += min_cost[v]

        for u in range(n):
            min_cost[u] = min(min_cost[u], dist[v][u])
    return ret

from union_find import UnionFind

def kruskal(G, V):
    uf = UnionFind(V)
    G = sorted(G, key=lambda e: e[2])
    ret = 0
    for u, v, weight in G:
        if not uf.same(u, v):
            uf.unite(u, v)
            ret += weight
    return ret


def topological_sort(G):
    ret = []
    start = []
    par_count = [0] * len(G)
    for u in range(len(G)):
        for v in G[u]:
            par_count[v] += 1
    for v in range(len(G)):
        if par_count[v] == 0:
            start.append(v)

    while start:
        u = start.pop()
        ret.append(u)
        for v in G[u]:
            par_count[v] -= 1
            if par_count[v] == 0:
                start.append(v)

    if any(c > 0 for c in par_count):
        # G is not a DAG
        return None
    return ret

def scc_decomposition(G):
    n = len(G)
    G_rev = [[] for _ in range(n)]
    for u in range(n):
        for v in G[u]:
            G_rev[v].append(u)

    # dfs
    vs = []
    visited = [False] * n
    used = [False] * n
    for u in range(n):
        if visited[u]:
            continue
        stack = [u]
        while stack:
            v = stack.pop()
            if used[v]:
                continue
            if not visited[v]:
                visited[v] = True
            else:
                vs.append(v)
                used[v] = True
                continue
            stack.append(v)
            for c in G[v]:
                if not visited[c]:
                    stack.append(c)

    # reverse dfs
    visited = [False] * n
    component = [-1] * n
    k = 0
    for u in vs[::-1]:
        if visited[u]:
            continue
        stack = [u]
        while stack:
            v = stack.pop()
            visited[v] = True
            component[v] = k
            for c in G_rev[v]:
                if not visited[c]:
                    stack.append(c)
        k += 1

    return component

def euler_tour(G, root):
    N = len(G)
    stack = [(root, -1, 1), (root, -1, 0)]
    et = []
    first = [-1] * N
    last = [-1] * N
    k = 0
    while stack:
        v, p, t = stack.pop()
        if t == 0:
            et.append(v)
            first[v] = k
            k += 1
            for c in G[v]:
                if c != p:
                    stack.append((c, v, 1))
                    stack.append((c, v, 0))
        else:
            last[v] = k
    return et, first, last

def tree_diameter(G):

    def dfs(s):
        stack = [(s, -1, 0)]
        ret = [(0, v) for v in range(len(G))]
        while stack:
            v, p, e = stack.pop()
            if e == 0:
                stack.append((v, p, 1))
                for c in G[v]:
                    if c != p:
                        stack.append((c, v, 0))
            else:
                for c in G[v]:
                    if c != p:
                        d, t = ret[c]
                        ret[v] = max(ret[v], (d + 1, t))
        return ret[s]

    _, u = dfs(0)
    d, v = dfs(u)
    return d, v