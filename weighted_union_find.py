class WeightedUnionFind:
    def __init__(self, N):
        self.par = [-1] * N
        self.weight = [0] * N

    def find(self, x):
        stack = [x]
        while self.par[x] >= 0:
            x = self.par[x]
            stack.append(x)
        r = stack.pop()
        while stack:
            x = stack.pop()
            self.weight[x] += self.weight[self.par[x]]
            self.par[x] = r
        return r

    def unite(self, x, y, w):
        w += self.weight[x] - self.weight[y]
        x = self.find(x)
        y = self.find(y)
        if self.par[x] > self.par[y]:
            x, y = y, x
            w = -w
        self.par[x] += self.par[y]
        self.par[y] = x
        self.weight[y] = w

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def diff(self, x, y):
        self.find(x)
        self.find(y)
        return self.weight[y] - self.weight[x]

    def size(self, x):
        return -self.par[self.find(x)]