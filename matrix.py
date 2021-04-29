class Matrix:
    def __init__(self, X):
        self.X = X
        self.shape = (len(X), len(X[0]))

    @staticmethod
    def zero(n):
        return Matrix([[0] * n for _ in range(n)])

    @staticmethod
    def identity(n):
        return Matrix([[int(i == j) for j in range(n)] for i in range(n)])

    def __str__(self):
        return '\n'.join(map(str, self.X))

    def __getitem__(self, i):
        return self.X[i]

    def __add__(self, other):
        assert self.shape == other.shape
        m, n = self.shape
        ret = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                ret[i][j] = self[i][j] + other[i][j]
        return Matrix(ret)

    def __sub__(self, other):
        assert self.shape == other.shape
        m, n = self.shape
        ret = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                ret[i][j] = self[i][j] - other[i][j]
        return Matrix(ret)

    def __mul__(self, k):
        m, n = self.shape
        ret = [[self[i][j] * k for j in range(n)] for i in range(m)]
        return Matrix(ret)

    def __truediv__(self, k):
        m, n = self.shape
        ret = [[self[i][j] / k for j in range(n)] for i in range(m)]
        return Matrix(ret)

    def matmul(self, other, mod=None):
        m, n = self.shape
        n_, l = other.shape
        assert n == n_
        ret = [[0] * l for _ in range(m)]
        for i in range(m):
            for j in range(l):
                e = 0
                for k in range(n):
                    e += self[i][k] * other[k][j]
                    if mod:
                        e %= mod
                ret[i][j] = e
        return Matrix(ret)

    def pow(self, exp, mod=None):
        m, n = self.shape
        assert m == n
        X = self
        ret = Matrix.identity(n)
        while exp > 0:
            if exp & 1:
                ret = ret.matmul(X, mod)
            X = X.matmul(X)
            exp >>= 1
        return ret

    def transpose(self):
        m, n = self.shape
        ret = [[self[j][i] for j in range(m)] for i in range(n)]
        return Matrix(ret)