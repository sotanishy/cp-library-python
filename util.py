def subset_k(n, k):
    S = (1 << k) - 1
    while S < (1 << n) - 1:
        yield S
        x = S & -S
        y = S + x
        S = ((S & ~y) // x >> 1) | y

def popcount(n):
    return sum((n >> i & 1) for i in range(N))
