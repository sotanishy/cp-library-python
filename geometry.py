import cmath

eps = 1e-12

Vec = complex

def eq(a, b):
    return abs(a - b) < eps

def lt(a, b):
    return a < b - eps

def leq(a, b):
    return a < b + eps

def dot(a, b):
    return (a.conjugate() * b).real

def cross(a, b):
    return (a.conjugate() * b).imag

def rot(a, ang):
    return a * cmath.rect(1, ang)

# checks if the three points are on the same line
def are_colinear(p1, p2, p3, eps=1e-12):
    return eq(cross(p2-p1, p3-p1), 0)

# checks if a -> b -> c is counter clockwise
def ccw(a, b, c):
    return (b[1] - a[1]) * (c[0] - a[0]) < (c[1] - a[1]) * (b[0] - a[0])

# returns true if the segment ab intersects the segment cd
def intersect(a, b, c, d):
    ta = cross(c-d, a-c)
    tb = cross(c-d, b-c)
    tc = cross(a-b, c-a)
    td = cross(a-b, d-a)
    return ta*tb < 0 and tc*td < 0


# checks if q is on the segment p1-p2
def on_segment(p1, p2, q, eps=1e-12):
    v1 = p1 - q
    v2 = p2 - q
    return eq(cross(v1, v2), 0) and eq(dot(v1, v2), 0)


# returns the intersection of the lines p1-p2 and q1-q2
# if the lines are parallel, returns None
def intersection(p1, p2, q1, q2, eps=1e-12):
    p = p2 - p1
    q = q2 - q1
    r = q1 - p1
    # if parallel
    if eq(cross(q, p), 0):
        return None
    return p1 + cross(q, r) / cross(q, p) * p


# returns a list of the intersections of two circles
# if they are outside of each other or one contains the other entirely, returns an empty list
def intersection_circles(c1, r1, c2, r2):
    d = abs(c1 - c2)

    # if the circles are outside of each other
    if r1 + r2 < d:
        return []

    # if one contains the other entirely
    if d < abs(r2 - r1):
        return []

    x = (r1**2-r2**2+d**2) / (2*d)
    y = (r1**2-x**2)**.5
    e1 = (c2-c1) / abs(c2-c1)
    e2 = Vec(-e1.y, e1.x)
    p1 = c1 + e1*x + e2*y
    p2 = c1 + e1*x - e2*y
    return [p1, p2]


def point_line_dist(p1, p2, q):
    p = p2 - p1
    return abs(cross(q, p) + cross(p2, p1)) / abs(p)

def area(A, B, C):
    AB = B - A
    AC = C - A
    return abs(cross(AB, AC)) / 2


def centroid(A, B, C):
    if are_colinear(A, B, C):
        return None
    return (A+B+C) / 3


def circumcenter(A, B, C):
    if are_colinear(A, B, C):
        return None
    a = abs(B - C)
    b = abs(C - A)
    c = abs(A - B)
    cosA = (b**2+c**2-a**2) / (2*b*c)
    cosB = (c**2+a**2-b**2) / (2*c*a)
    cosC = (a**2+b**2-c**2) / (2*a*b)
    return (a*cosA*A + b*cosB*B + c*cosC*C) / (a*cosA + b*cosB + c*cosC)


def incenter(A, B, C):
    if are_colinear(A, B, C):
        return None
    a = abs(B - C)
    b = abs(C - A)
    c = abs(A - B)
    return (a*A + b*B + c*C) / (a+b+c)


def convex_hull(points, eps=1e-12):
    n = len(points)
    points.sort(key=lambda p: (p.real, p.imag))
    k = 0  # # of vertices in the convex hull
    ch = [None] * (2*n)
    # bottom
    for i in range(n):
        while k > 1 and lt(cross(ch[k-1]-ch[k-2], points[i]-ch[k-1]), 0):
            k -= 1
        ch[k] = points[i]
        k += 1
    t = k
    # top
    for i in range(n-1)[::-1]:
        while k > t and lt(cross(ch[k-1]-ch[k-2], points[i]-ch[k-1]), 0):
            k -= 1
        ch[k] = points[i]
        k += 1
    return ch[:k-1]
