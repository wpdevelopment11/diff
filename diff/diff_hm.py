from collections import namedtuple

Candidate = namedtuple("Candidate", ["a", "b", "previous"])
EqClass = namedtuple("EqClass", ["serial", "last"])
Line = namedtuple("Line", ["serial", "hash"])

def LCS(seq_a, seq_b):
    m = len(seq_a)
    n = len(seq_b)
    H = lambda x: x

    # 1.
    V = [0] * (n + 1)
    for j in range(1, n+1):
        V[j] = (Line(j, H(seq_b[j-1])))
    V[0] = ()

    # 2.
    V.sort(key=lambda t: (t.hash, t.serial) if t else t)

    # 3.
    f = lambda j: j == n or V[j].hash != V[j+1].hash
    E = [0] * (n + 1)
    for j in range(1, n+1):
        E[j] = EqClass(V[j].serial, f(j))
    E[0] = EqClass(0, True)

    # 4.
    P = [0] * (m + 1)
    for i in range(1, m+1):
        # TODO: binary search
        hi = H(seq_a[i-1])
        for j in range(1, n+1):
            if hi == V[j].hash:
                break
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
            k = merge(K, k, i, E, P[i])

    # 7.
    J = [0] * (m + 1)

    # 8.
    c = K[k]
    while c != None:
        J[c.a] = c.b
        c = c.previous

    return [seq_a[i-1] for i in range(1, m+1) if J[i]]

def merge(K, k, i, E, p):
    r = 0
    c = K[0]
    while True:
        j = E[p].serial
        # TODO: binary search
        for s in range(r, k+1):
            if K[s].b < j and K[s+1].b > j:
                tmp = K[s]
                K[r] = c
                r = s + 1
                c = Candidate(i, j, tmp)
                if s == k:
                    K[k+2] = K[k+1]
                    k += 1

                    K[r] = c
                    return k

        if E[p].last:
            break
        p += 1

    K[r] = c
    return k
