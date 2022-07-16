import numpy as np
from math import pi, cos, sin

def fft(f):
    n = len(f)
    m = n
    while m > 1:
        ang = 2 * pi / m
        omega = complex(cos(ang), sin(ang))
        for s in range(n // m):
            w = 1
            for i in range(m // 2):
                l = f[s * m + i]
                r = f[s * m + i + m // 2]
                f[s * m + i] = l + r
                f[s * m + i + m // 2] = (l - r) * w
                w *= omega
        m //= 2

def ifft(f):
    n = len(f)
    m = 2
    while m <= n:
        ang = -2 * pi / m
        omega = complex(cos(ang), sin(ang))
        for s in range(n // m):
            w = 1
            for i in range(m // 2):
                l = f[s * m + i]
                r = f[s * m + i + m // 2] * w
                f[s * m + i] = l + r
                f[s * m + i + m // 2] = l - r
                w *= omega
        m *= 2

def convolve(f, g):
    size = len(f) + len(g) - 1
    n = 1
    while n < size:
        n *= 2
    nf = f[:] + [0] * (n - len(f))
    ng = g[:] + [0] * (n - len(g))
    fft(nf)
    fft(ng)
    for i in range(n):
        nf[i] *= ng[i]
    ifft(nf)
    ret = [0] * size
    for i in range(size):
        ret[i] = nf[i].real / n
    return ret

# convolution with numpy
def convolve(f, g):
    size = len(f) + len(g) - 1
    n = 1
    while n < size:
        n *= 2
    nf = np.fft.rfft(f, n)
    ng = np.fft.rfft(g, n)
    nf *= ng
    nf = np.fft.irfft(nf, n)
    return np.rint(nf).astype(np.int64)