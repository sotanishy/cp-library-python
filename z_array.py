def z_array(s):
    n = len(s)
    z = [0] * n
    z[0] = n
    l = r = 0
    for i in range(1, n):
        k = i - l
        if i <= r and z[k] < r - i + 1:
            z[i] = z[k]
        else:
            l = i
            if i > r:
                r = i
            while r < n and s[r - l] == s[r]:
                r += 1
            r -= 1
            z[i] = r - l + 1
    return z

