from .rmq import RMQ

# LCA using Euler tour and RMQ
class LCA:
    def __init__(self, G, root):
        self.G = G
        self.root = root
        V = len(G)
        self.vs = [-1] * (2*V-1)  # the ith visited node
        self.depth = [-1] * (2*V-1)
        self.k = 0
        self.id = [-1] * V  # the first index where v appears in vs
        self.euler_tour()
        self.rmq = RMQ(2*V-1)
        for i in range(2*V-1):
            self.rmq.update(i, self.depth[i])

    def euler_tour(self):
        stack = [(0, 0)]
        i = 0
        while stack:
            u, d = stack.pop()
            self.vs[i] = u
            self.depth[i] = d
            if self.id[u] == -1:
                self.id[u] = i
                i += 1
            else:
                i += 1
                continue
            tmp = []
            for v in G[u]:
                if self.id[v] == -1:
                    tmp.append((v, d+1))
                else:
                    stack.append((v, d-1))
            stack += tmp

    def lca(self, u, v):
        i, v = self.rmq.query(min(self.id[u], self.id[v]), max(self.id[u], self.id[v])+1, index=True)
        return self.vs[i]


# LCA using doubling
class LCA:
    def __init__(self, G, root):
        V = len(G)
        self.log = 0
        while 2**self.log <= V:
            self.log += 1

        self.parent = [[-1] * V for _ in range(self.log)]
        self.depth = [0] * V
        stack = [root]
        while stack:
            v = stack.pop()
            p = self.parent[0][v]
            for c in G[v]:
                if c != p:
                    self.parent[0][c] = v
                    self.depth[c] = self.depth[v] + 1
                    stack.append(c)

        for k in range(self.log-1):
            for v in range(V):
                if self.parent[k][v] >= 0:
                    self.parent[k+1][v] = self.parent[k][self.parent[k][v]]

    def lca(self, u, v):
        if self.depth[u] > self.depth[v]:
            u, v = v, u

        # go up to the same depth
        for k in range(self.log):
            if (self.depth[v] - self.depth[u]) >> k & 1:
                v = self.parent[k][v]
        if u == v:
            return u

        for k in range(self.log)[::-1]:
            if self.parent[k][u] != self.parent[k][v]:
                u = self.parent[k][u]
                v = self.parent[k][v]
        return self.parent[0][u]

    def dist(self, u, v):
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]

    def ancestor(self, v, k):
        for i in range(self.log)[::-1]:
            if k >= (1 << i):
                v = self.parent[i][v]
                k -= 1 << i
        return v