def largst_rectangle(h):
    n = len(h)
    left = [0] * n
    right = [0] * n
    st = [(-1, -1)]
    for i in range(n):
        while st[-1][0] >= h[i]:
            st.pop()
        left[i] = st[-1][1] + 1
        st.append((h[i], i))
    st = [(-1, n)]
    for i in range(n)[::-1]:
        while st[-1][0] >= h[i]:
            st.pop()
        right[i] = st[-1][1]
        st.append((h[i], i))
    ret = 0
    for i in range(n):
        ret = max(ret, h[i] * (right[i] - left[i]))
    return ret