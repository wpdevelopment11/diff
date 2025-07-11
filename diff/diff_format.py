from collections import namedtuple

Add = namedtuple("Add", ["apos", "blines"])
Delete = namedtuple("Delete", ["alines", "bpos"])
Replace = namedtuple("Replace", ["alines", "blines"])

def get_hunks(lcs, seq_a, seq_b):
    i = j = 0
    aprevcomm = bprevcomm = -1

    lcs = lcs + [None]
    seq_a = list(seq_a) + [None]
    seq_b = list(seq_b) + [None]

    hunks = []

    for comm in lcs:
        while seq_a[i] != comm:
            i += 1
        while seq_b[j] != comm:
            j += 1
        auncommlen = i - (aprevcomm + 1)
        buncommlen = j - (bprevcomm + 1)

        if not buncommlen and auncommlen:
            lines = aprevcomm + 2
            if auncommlen > 1:
                lines = (lines, i)
            hunks.append(Delete(lines, j))
        elif buncommlen and not auncommlen:
            apos = aprevcomm + 1
            lines = bprevcomm + 2
            if buncommlen > 1:
                lines = (lines, j)
            hunks.append(Add(apos, lines))
        elif buncommlen and auncommlen:
            alines = aprevcomm + 2
            if auncommlen > 1:
                alines = (alines, i)

            blines = bprevcomm + 2
            if buncommlen > 1:
                blines = (blines, j)

            hunks.append(Replace(alines, blines))

        aprevcomm = i
        bprevcomm = j
        i += 1
        j += 1

    return hunks

def invert_hunk(hunk):
    pass

def print_hunk(stream, hunk):
    pass
