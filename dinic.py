class Dinic:
    class Edge:
        def __init__(self, v, cap, rev):
            self.v = v
            self.cap = cap
            self.rev = rev

    def __init__(self, V):
        self.V = V
        self.G = [[] for _ in range(V)]

    def add_edge(self, u, v, cap):
        self.G[u].append(self.Edge(v, cap, len(self.G[v])))
        self.G[v].append(self.Edge(u, 0, len(self.G[u])-1))

    # calculates the shortest distance from s
    def bfs(self, s):
        from collections import deque

        self.level = [-1] * self.V
        self.level[s] = 0
        queue = deque()
        queue.append(s)
        while queue:
            u = queue.popleft()
            for e in self.G[u]:
                if e.cap > 0 and self.level[e.v] == -1:
                    self.level[e.v] = self.level[u] + 1
                    queue.append(e.v)

    # finds a path
    def dfs(self, u, t, f):
        if u == t:
            return f
        i = self.iter[u]
        while i < len(self.G[u]):
            e = self.G[u][i]
            if e.cap > 0 and self.level[u] < self.level[e.v]:
                d = self.dfs(e.v, t, min(f, e.cap))
                if d > 0:
                    e.cap -= d
                    self.G[e.v][e.rev].cap += d
                    return d
            i += 1
            self.iter[u] += 1
        return 0

    # finds the max flow from s to v
    def max_flow(self, s, t):
        flow = 0
        INF = 10**18
        while True:
            self.bfs(s)
            if self.level[t] == -1:
                return flow
            self.iter = [0] * self.V
            while True:
                f = self.dfs(s, t, INF)
                if f == 0:
                    break
                flow += f

    # checks if v is reachable from s in the residual network
    def min_cut(self, s):
        visited = [False] * self.V
        st = [s]
        visited[s] = True
        while st:
            u = st.pop()
            for e in self.G[u]:
                if e.cap > 0 and not visited[e.v]:
                    visited[e.v] = True
                    st.append(e.v)
        return visited