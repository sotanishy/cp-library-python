class BipartiteMatching:
    def __init__(self, V):
        self.V = V
        self.G = [[] for _ in range(V)]

    def add_edge(self, u, v):
        self.G[u].append(v)
        self.G[v].append(u)

    def dfs(self, u):
        self.used[u] = True
        for v in self.G[u]:
            w = self.match[v]
            if w < 0 or (not self.used[w] and self.dfs(w)):
                self.match[u] = v
                self.match[v] = u
                return True
        return False

    def bipartite_matching(self):
        res = 0
        self.match = [-1] * self.V
        for v in range(self.V):
            if self.match[v] == -1:
                self.used = [False] * self.V
                if self.dfs(v):
                    res += 1
        return res
