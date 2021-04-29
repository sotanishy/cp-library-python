class UnionFind:
    def __init__(self, N):
        self.par = list(range(N))
        self.size = [1] * N
        self.weight = [0] * N

    def find(self, x):
        stack = [x]
        while self.par[x] != x:
            x = self.par[x]
            stack.append(x)
        r = stack[-1]
        while stack:
            x = stack.pop()
            self.weight[x] += self.weight[self.par[x]]
            self.par[x] = r
        return r

    def unite(self, x, y, w):
        w += self.weight[x] - self.weight[y]
        x = self.find(x)
        y = self.find(y)
        if x == y:
            return False
        if self.size[x] < self.size[y]:
            x, y = y, x
            w = -w
        self.par[y] = x
        self.size[x] += self.size[y]
        self.weight[y] = w
        return True

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def diff(self, x, y):
        return self.weight[self.find(y)] - self.weight[self.find(x)]

    def get_size(self, x):
        return self.size[self.find(x)]