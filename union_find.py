class UnionFind:
    def __init__(self, N):
        self.par = [-1] * N

    def find(self, x):
        r = x
        while self.par[r] >= 0:
            r = self.par[r]
        while x != r:
            tmp = self.par[x]
            self.par[x] = r
            x = tmp
        return r

    def unite(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return
        if self.par[x] > self.par[y]:
            x, y = y, x
        self.par[x] += self.par[y]
        self.par[y] = x

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def size(self, x):
        return -self.par[self.find(x)]