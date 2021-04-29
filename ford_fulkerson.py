class FordFulkerson:
    class Edge:
        def __init__(self, v, cap, rev):
            self.v = v
            self.cap = cap
            self.rev = rev

    def __init__(self, V):
        self.V = V
        self.G = [[] for _ in range(V)]
        self.used = [False] * V

    def add_edge(self, u, v, cap):
        self.G[u].append(self.Edge(v, cap, len(self.G[v])))
        self.G[v].append(self.Edge(u, 0, len(self.G[u])-1))

    # find a path
    # u: current node, t: sink node, f: current flow
    def dfs(self, u, t, f):
        if u == t:
            return f
        self.used[u] = True
        for e in self.G[u]:
            if not self.used[e.v] and e.cap > 0:
                d = self.dfs(e.v, t, min(f, e.cap))
                if d > 0:
                    e.cap -= d
                    self.G[e.v][e.rev].cap += d
                    return d
        return 0

    # find the max flow from s to t
    def max_flow(self, s, t):
        flow = 0
        while True:
            self.used = [False] * self.V
            INF = 10**18
            f = self.dfs(s, t, INF)
            if f == 0:
                return flow
            flow += f
