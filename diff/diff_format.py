"""Create hunks that can be used to generate the diff output."""

from diff.hunk import Add, Delete, Replace

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
            lines = (aprevcomm + 2, i)
            hunks.append(Delete(seq_a, lines, j))
        elif buncommlen and not auncommlen:
            apos = aprevcomm + 1
            lines = (bprevcomm + 2, j)
            hunks.append(Add(apos, seq_b, lines))
        elif buncommlen and auncommlen:
            alines = (aprevcomm + 2, i)
            blines = (bprevcomm + 2, j)
            hunks.append(Replace(seq_a, alines, seq_b, blines))

        aprevcomm = i
        bprevcomm = j
        i += 1
        j += 1

    return hunks
