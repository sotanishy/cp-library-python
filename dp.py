def LCS(A, B):
    dp = [[0] * (len(B)+1) for _ in range(len(A)+1)]
    for i in range(len(A)):
        for j in range(len(B)):
            if A[i] == B[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
    return dp[-1][-1]

def LIS(A, strict=False):
    from bisect import bisect_left

    INF = 10**18
    N = len(A)
    dp = [INF] * N
    for a in A:
        i = bisect_left(dp, a + (1 - strict))
        dp[i] = a
    return bisect_left(dp, INF)
