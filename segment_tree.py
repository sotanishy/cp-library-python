class SegmentTree:
    def __init__(self, size, op, identity):
        n = 1 << (size - 1).bit_length()
        self.size = n
        self.op = op
        self.identity = identity
        self.node = [identity] * (2 * n)

    def __getitem__(self, k):
        return self.node[k + self.size]

    def build(self, v):
        for k in range(len(v)):
            self.node[k + self.size] = v[k]
        for k in range(self.size - 1, 0, -1):
            self.node[k] = self.op(self.node[2 * k], self.node[2 * k + 1])

    def update(self, k, x):
        k += self.size
        self.node[k] = x
        while k > 1:
            k >>= 1
            self.node[k] = self.op(self.node[2 * k], self.node[2 * k + 1])

    def fold(self, l, r):
        vl = vr = self.identity
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                vl = self.op(vl, self.node[l])
                l += 1
            if r & 1:
                r -= 1
                vr = self.op(self.node[r], vr)
            l >>= 1
            r >>= 1
        return self.op(vl, vr)

    def find_first(self, l, cond):
        vl = self.identity
        l += self.size
        r = 2 * self.size
        while l < r:
            if l & 1:
                nxt = self.op(vl, self.node[l])
                if cond(nxt):
                    while l < self.size:
                        nxt = self.op(vl, self.node[2 * l])
                        if cond(nxt):
                            l = 2 * l
                        else:
                            vl = nxt
                            l = 2 * l + 1
                    return l - self.size
                vl = nxt
                l += 1
            l >>= 1
            r >>= 1
        return -1

    def find_last(self, r, cond):
        vr = self.identity
        l = self.size
        r += self.size
        while l < r:
            if r & 1:
                r -= 1
                nxt = self.op(self.node[r], vr)
                if cond(nxt):
                    while r < self.size:
                        nxt = self.op(self.node[2 * r + 1], vr)
                        if cond(nxt):
                            r = 2 * r + 1
                        else:
                            vr = nxt
                            r = 2 * r
                    return r - self.size
                vr = nxt
            l >>= 1
            r >>= 1
        return -1
