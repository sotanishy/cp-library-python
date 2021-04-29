class SuffixArray:
    def __init__(self, s):
        n = len(s)
        sa = list(range(n))
        sa.sort(key=lambda i: s[i])
        cl = 0
        rank = [0] * n
        for i in range(1, n):
            if s[sa[i - 1]] != s[sa[i]]:
                cl += 1
            rank[sa[i]] = cl
        tmp = [0] * n
        nrank = [0] * n
        k = 1
        while k < n:
            # sort by second half
            cnt1 = 0
            cnt2 = k
            for i in range(n):
                j = sa[i] - k
                if j >= 0:
                    tmp[cnt2] = j
                    cnt2 += 1
                else:
                    tmp[cnt1] = j + n
                    cnt1 += 1

            # sort by first half
            cnt = [0] * n
            for i in range(n):
                cnt[rank[tmp[i]]] += 1
            for i in range(1, n):
                cnt[i] += cnt[i - 1]
            for i in range(n)[::-1]:
                cnt[rank[tmp[i]]] -= 1
                sa[cnt[rank[tmp[i]]]] = tmp[i]

            # assign new rank
            nrank[sa[0]] = 0
            cl = 0
            for i in range(1, n):
                if rank[sa[i - 1]] != rank[sa[i]] or (rank[sa[i - 1] + k] if sa[i - 1] + k < n else -1) != (rank[sa[i] + k] if sa[i] + k < n else -1):
                    cl += 1
                nrank[sa[i]] = cl
            rank, nrank = nrank, rank
            k <<= 1

        self.sa = sa
        self.s = s

    def __getitem__(self, k):
        return self.sa[k]

    def lower_bound(self, t):
        lb, ub = -1, len(self.sa)
        while ub - lb > 1:
            m = (lb + ub) // 2
            if self._lt_substr(t, self.sa[m]):
                lb = m
            else:
                ub = m
        return ub

    def _lt_substr(self, t, si):
        sn, tn = len(self.s), len(t)
        ti = 0
        while si < sn and ti < tn:
            if self.s[si] < t[ti]:
                return True
            if self.s[si] > t[ti]:
                return False
            si += 1
            ti += 1