import math

class Vec:
    eps = 1e-12

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __add__(self, other):
        return Vec(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vec(self.x-other.x, self.y-other.y)

    def __mul__(self, k):
        return Vec(self.x*k, self.y*k)

    def __rmul__(self, k):
        return self * k

    def __truediv__(self, k):
        return Vec(self.x/k, self.y/k)

    def __neg__(self):
        return Vec(-self.x, -self.y)

    def __eq__(self, other):
        return abs(self.x - other.x) < eps

    def __ne__(self, other):
        return not (self == other)

    def __abs__(self):
        return (self.x**2 + self.y**2)**.5

    def dot(self, other):
        return self.x*other.x + self.y*other.y

    def cross(self, other):
        return self.x*other.y - self.y*other.x

    def rot(self, ang):
        c = math.cos(ang)
        s = math.sin(ang)
        return Vec(c*self.x-s*self.y, s*self.x+c*self.y)

    def arg(self):
        return math.atan2(self.y, self.x)


# checks if the three points are on the same line
def are_colinear(p1, p2, p3, eps=1e-12):
    return abs((p2-p1).cross(p3-p1)) < eps

# checks if a -> b -> c is counter clockwise
def ccw(a, b, c):
    return (b[1] - a[1]) * (c[0] - a[0]) < (c[1] - a[1]) * (b[0] - a[0])

# returns true if the segment ab intersects the segment cd
def intersect(a, b, c, d):
    ta = (c-d).cross(a-c)
    tb = (c-d).cross(b-c)
    tc = (a-b).cross(c-a)
    td = (a-b).cross(d-a)
    return ta*tb < 0 and tc*td < 0


# checks if q is on the segment p1-p2
def on_segment(p1, p2, q, eps=1e-12):
    v1 = p1 - q
    v2 = p2 - q
    return abs(v1.cross(v2)) < eps and v1.dot(v2) < eps


# returns the intersection of the lines p1-p2 and q1-q2
# if the lines are parallel, returns None
def intersection(p1, p2, q1, q2, eps=1e-12):
    p = p2 - p1
    q = q2 - q1
    r = q1 - p1
    # if parallel
    if abs(q.cross(p)) < eps:
        return None
    return p1 + (q.cross(r) / q.cross(p)) * p


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
    return abs(q.cross(p)+p2.cross(p1)) / abs(p)

def area(A, B, C):
    AB = B - A
    AC = C - A
    return abs(AB.cross(AC)) / 2


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
    points.sort(key=lambda p: (p.x, p.y))
    k = 0  # # of vertices in the convex hull
    ch = [None] * (2*n)
    # bottom
    for i in range(n):
        while k > 1 and (ch[k-1]-ch[k-2]).cross(points[i]-ch[k-1]) < eps:
            k -= 1
        ch[k] = points[i]
        k += 1
    t = k
    # top
    for i in range(n-1)[::-1]:
        while k > t and (ch[k-1]-ch[k-2]).cross(points[i]-ch[k-1]) < eps:
            k -= 1
        ch[k] = points[i]
        k += 1
    return ch[:k-1]
