def get_primitive_root(mod):
    if mod == 167772161:
        return 3
    if mod == 469762049:
        return 3
    if mod == 754974721:
        return 11
    if mod == 998244353:
        return 3
    if mod == 1224736769:
        return 3

def ntt(f, mod, pm):
    n = len(f)
    m = n
    while m > 1:
        omega = pow(pm, (mod - 1) // m, mod)
        for s in range(n // m):
            w = 1
            for i in range(m // 2):
                l = f[s * m + i]
                r = f[s * m + i + m // 2]
                f[s * m + i] = (l + r) % mod
                f[s * m + i + m // 2] = (l - r) * w % mod
                w = w * omega % mod
        m //= 2

def intt(f, mod, pm):
    n = len(f)
    m = 2
    while m <= n:
        omega = pow(pm, (mod - 1) // m, mod)
        omega = pow(omega, mod - 2, mod)
        for s in range(n // m):
            w = 1
            for i in range(m // 2):
                l = f[s * m + i]
                r = f[s * m + i + m // 2] * w % mod
                f[s * m + i] = (l + r) % mod
                f[s * m + i + m // 2] = (l - r) % mod
                w = w * omega % mod
        m *= 2

def convolve(f, g, mod):
    size = len(f) + len(g) - 1
    pm = get_primitive_root(mod)
    n = 1
    while n < size:
        n *= 2
    nf = f[:] + [0] * (n - len(f))
    ng = g[:] + [0] * (n - len(g))
    ntt(nf, mod, pm)
    ntt(ng, mod, pm)
    for i in range(n):
        nf[i] = nf[i] * ng[i] % mod
    intt(nf, mod, pm)
    ret = [0] * size
    invn = pow(n, mod - 2, mod)
    for i in range(size):
        ret[i] = nf[i] * invn % mod
    return ret
