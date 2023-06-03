class FenwickTree:
    def __init__(self, size):
        self.data = [0] * (size + 1)
        self.size = size

    # i is exclusive
    def prefix_sum(self, i):
        s = 0
        while i > 0:
            s += self.data[i]
            i -= i & -i
        return s

    def add(self, i, x):
        i += 1
        while i <= self.size:
            self.data[i] += x
            i += i & -i

    def lower_bound(self, x):
        if x <= 0:
            return 0
        k = 1
        while k * 2 <= self.size:
            k *= 2
        i = 0
        while k > 0:
            if i + k <= self.size and self.data[i + k] < x:
                x -= self.data[i + k]
                i += k
            k //= 2
        return i + 1


class RangeFenwickTree:
    def __init__(self, size):
        self.bit0 = FenwickTree(size)
        self.bit1 = FenwickTree(size)

    # i is exclusive
    def prefix_sum(self, i):
        return self.bit0.prefix_sum(i) * (i - 1) + self.bit1.prefix_sum(i)

    def add(self, l, r, x):
        self.bit0.add(l, x)
        self.bit0.add(r, -x)
        self.bit1.add(l, -x * (l - 1))
        self.bit1.add(r, x * (r - 1))


class FenwickTree2D:
    def __init__(self, H, W):
        self.H = H
        self.W = W
        self.data = [[0] * (W + 1) for _ in range(H + 1)]

    def add(self, a, b, x):
        a += 1
        b += 1
        i = a
        while i <= self.H:
            j = b
            while j <= self.W:
                self.data[i][j] += x
                j += j & -j
            i += i & -i

    def sum(self, a, b):
        a += 1
        b += 1
        ret = 0
        i = a
        while i > 0:
            j = b
            while j > 0:
                ret += self.data[i][j]
                j -= j & -j
            i -= i & -i
        return ret


class FenwickTreeSet:
    def __init__(self, max_val):
        self.max_val = max_val
        self.ft = FenwickTree(max_val + 1)

    def add(self, x):
        self.ft.add(x, 1)

    def remove(self, x):
        self.ft.add(x, -1)

    def pred(self, x):
        return self.ft.lower_bound(self.ft.prefix_sum(x)) - 1

    def succ(self, x):
        return self.ft.lower_bound(self.ft.prefix_sum(x) + 1) - 1

    def size(self):
        return self.ft.prefix_sum(self.max_val + 1)
