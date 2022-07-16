from bisect import bisect_left

class Compress:
    def __init__(self, vs):
        self.xs = list(set(vs))
        self.xs.sort()

    def compress(self, x):
        return bisect_left(self.xs, x)

    def decompress(self, i):
        return self.xs[i]

    def size(self):
        return len(self.xs)