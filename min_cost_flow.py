class MinCostFlow:
    class Edge:
        def __init__(self, v, cap, cost, rev):
            self.v = v
            self.cap = cap
            self.cost = cost
            self.rev = rev

    def __init__(self, V):
        self.V = V
        self.G = [[] for _ in range(V)]

    def add_edge(self, u, v, cap, cost):
        self.G[u].append(self.Edge(v, cap, cost, len(self.G[v])))
        self.G[v].append(self.Edge(u, 0, -cost, len(self.G[u])-1))

    def min_cost_flow(self, s, t, f):
        from heapq import heappush, heappop

        res = 0
        h = [0] * self.V
        prevv = [0] * self.V
        preve = [0] * self.V
        while f > 0:
            # update h using dijkstra
            heap = []
            INF = 10**18
            dist = [INF] * self.V
            dist[s] = 0
            heappush(heap, (0, s))
            while heap:
                d, u = heappop(heap)
                if dist[u] < d:
                    continue
                for i in range(len(self.G[u])):
                    e = self.G[u][i]
                    if e.cap > 0 and dist[e.v] > dist[u] + e.cost + h[u] - h[e.v]:
                        dist[e.v] = dist[u] + e.cost + h[u] - h[e.v]
                        prevv[e.v] = u
                        preve[e.v] = i
                        heappush(heap, (dist[e.v], e.v))

                if dist[t] == INF:
                    return -1
                for v in range(self.V):
                    h[v] += dist[v]

                m = f
                v = t
                while v != s:
                    m = min(m, self.G[prevv[v]][preve[v]].cap)
                    v = prevv[v]
                f -= m
                res += m * h[t]
                v = t
                while v != s:
                    e = self.G[prevv[v]][preve[v]]
                    e.cap -= d
                    self.G[v][e.rev].cap += d
                    v = prevv[v]
