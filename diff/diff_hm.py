"""Implementation of the Hunt-McIlroy diff algorithm.

See: https://www.cs.dartmouth.edu/~doug/diff.pdf
"""

from collections import namedtuple

import math

Candidate = namedtuple("Candidate", ["a", "b", "previous"])
EqClass = namedtuple("EqClass", ["serial", "last"])
Line = namedtuple("Line", ["serial", "hash"])

def LCS(seq_a, seq_b):
    m = len(seq_a)
    n = len(seq_b)

    # 1.
    V = [0] * (n + 1)
    for j in range(1, n+1):
        V[j] = (Line(j, seq_b[j-1]))
    V[0] = ()

    # 2.
    V.sort(key=lambda t: (t.hash, t.serial) if t else t)

    # 3.
    E = [0] * (n + 1)
    for j in range(1, n+1):
        E[j] = EqClass(V[j].serial, j == n or V[j].hash != V[j+1].hash)
    E[0] = EqClass(0, True)

    # 4.
    P = [0] * (m + 1)
    for i in range(1, m+1):
        hi = seq_a[i-1]
        L = 1
        R = n+1
        while L < R:
            mid = L + math.floor((R - L) / 2)
            if V[mid].hash < hi:
                L = mid + 1
            else:
                R = mid
        if L < n+1 and V[L].hash == hi:
            j = L
        else:
            j = 0
        P[i] = j

    # 5.
    K = [0] * (min(m, n) + 2)
    K[0] = Candidate(0, 0, None)
    K[1] = Candidate(m+1, n+1, None)
    k = 0

    # 6.
    for i in range(1, m+1):
        if P[i]:
            r = 0
            c = K[0]
            p = P[i]
            while True:
                j = E[p].serial
                L = r
                R = k+2
                while L < R:
                    mid = L + math.floor((R - L) / 2)
                    if K[mid].b < j:
                        L = mid + 1
                    else:
                        R = mid
                if L < k+2 and L > r and K[L].b > j:
                    s = L - 1
                    tmp = K[s]
                    K[r] = c
                    r = s + 1
                    c = Candidate(i, j, tmp)
                    if s == k:
                        K[k+2] = K[k+1]
                        k += 1

                        K[r] = c
                        break

                if E[p].last:
                    break
                p += 1

            K[r] = c

    # 7.
    J = [0] * (m + 1)

    # 8.
    c = K[k]
    while c != None:
        J[c.a] = c.b
        c = c.previous

    return [seq_a[i-1] for i in range(1, m+1) if J[i]]
