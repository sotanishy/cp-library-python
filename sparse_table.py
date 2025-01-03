class SparseTable:
    def __init__(self, a):
        N = len(a)
        log = N.bit_length()
        lookup = [[0] * N for _ in range(log)]
        for i in range(N):
            lookup[0][i] = a[i]
        for i in range(1, log):
            for j in range(N - (1 << i) + 1):
                lookup[i][j] = min(
                    lookup[i - 1][j], lookup[i - 1][j + (1 << (i - 1))])
        self.lookup = lookup

    def query(self, l, r):
        i = (r - l).bit_length() - 1
        return min(self.lookup[i][l], self.lookup[i][r - (1 << i)])
