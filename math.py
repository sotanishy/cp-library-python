def mod_inv(n, mod=10**9+7):
    return pow(n, mod-2, mod)


def comb(n, k, mod=10**9+7):
    num = den = 1
    for i in range(k):
        num = num * (n-i) % mod
        den = den * (i+1) % mod
    return num * pow(den, mod-2, mod) % mod


def comb_preprocess(n, mod):
    fact = [1] * (n+1)
    fact_inv = [1] * (n+1)
    for i in range(1, n+1):
        fact[i] = i * fact[i-1] % mod
    fact_inv[n] = pow(fact[n], mod-2, mod)
    for i in range(1, n+1)[::-1]:
        fact_inv[i-1] = i * fact_inv[i] % mod
    comb = lambda n, k: fact[n] * fact_inv[k] * fact_inv[n-k] % mod
    return fact, fact_inv, comb


def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    if n < 9:
        return True
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def divisor(n):
    divisors = []
    i = 1
    while i * i < n:
        if n % i == 0:
            divisors.append(i)
            divisors.append(n // i)
        i += 1
    if i * i == n:
        divisors.append(i)
    divisors.sort()
    return divisors


def prime_factor(n):
    factors = {}
    if n % 2 == 0:
        cnt = 0
        while n % 2 == 0:
            cnt += 1
            n //= 2
        factors[2] = cnt
    i = 3
    while i * i <= n:
        if n % i == 0:
            cnt = 0
            while n % i == 0:
                cnt += 1
                n //= i
            factors[i] = cnt
        i += 2
    if n != 1:
        factors[n] = 1
    return factors


def sieve(n):
    is_prime = [True] * (n+1)
    is_prime[0] = is_prime[1] = False
    for j in range(4, n+1, 2):
        is_prime[j] = False
    prime = [2]
    for i in range(3, n+1):
        if is_prime[i]:
            prime.append(i)
            for j in range(i*i, n+1, 2*i):
                is_prime[j] = False
    return prime


# returns the number of integers less than and coprime to n
def euler_totient(n):
    for p in prime_factor(n).keys():
        n = n * (p - 1) // p
    return n

# returns x such that a^x = b (mod p)
def baby_step_giant_step(a, b, p):
    m = int(p**0.5) + 1
    baby = [0] * m
    x = 1
    for i in range(m):
        baby[i] = x
        x = x * a % p
    c = pow(a, m * (p-2), p)
    giant = [0] * m
    x = 1
    for i in range(m):
        giant[i] = x
        x = x * c % p
    baby_index = {b : i for i, b in enumerate(baby)}
    for i, g in giant:
        y = b * g % p
        if y in baby_index:
            return i * m + baby_index[y]


def change_base(n, base):
    q, r = divmod(n, base)
    if q == 0:
        return str(r)
    return change_base(q, base) + str(r)


def matmul(a, b, mod):
    m = len(a)
    l = len(a[0])
    n = len(b[0])
    ret = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            e = 0
            for k in range(l):
                e = (e + a[i][k] * b[k][j]) % mod
            ret[i][j] = e
    return ret

def matpow(X, exp, mod):
    Y = [[int(i == j) for j in range(len(X))] for i in range(len(X))]
    while exp > 0:
        if exp & 1:
            Y = matmul(X, Y, mod)
        X = matmul(X, X, mod)
        exp >>= 1
    return Y

def rref(A):
    n, m = len(A), len(A[0])
    pivot = 0
    for j in range(m):
        i = pivot
        while i < n and A[i][j] == 0:
            i += 1
        if i == n:
            continue
        if i != pivot:
            A[i], A[pivot] = A[pivot], A[i]

        p = A[pivot][j]
        for l in range(j, m):
            A[pivot][l] //= p

        for k in range(n):
            if k == pivot:
                continue
            v = A[k][j]
            for l in range(j, m):
                A[k][l] -= A[pivot][l] * v

        pivot += 1

def extgcd(a, b):
    s, sx, sy, t, tx, ty = a, 1, 0, b, 0, 1
    while t:
        q = s // t
        s -= t * q
        s, t = t, s
        sx -= tx * q
        sx, tx = tx, sx
        sy -= ty * q
        sy, ty = ty, sy
    return sx, sy

def floor_sum(n, m, a, b):
    s = 0
    if a >= m:
        s += (a // m) * n * (n - 1) // 2
        a %= m
    if b >= m:
        s += (b // m) * n
        b %= m
    y = (a * n + b) // m
    if y == 0:
        return s
    x = (m * y - b + a - 1) // a
    s += (n - x) * y + floor_sum(y, a, m, a * x - m * y + b)
    return s