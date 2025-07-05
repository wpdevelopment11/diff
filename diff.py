# See: https://en.wikipedia.org/wiki/Longest_common_subsequence
def LCSTable(seq_a, seq_b):
    rows, cols = len(seq_a)+1, len(seq_b)+1
    table = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(1, rows):
        for j in range(1, cols):
            if seq_a[i-1] == seq_b[j-1]:
                table[i][j] = table[i-1][j-1] + 1
            else:
                table[i][j] = max(table[i-1][j], table[i][j-1])
    return table

def LCSLength(seq_a, seq_b):
    table = LCSTable(seq_a, seq_b)
    return table[-1][-1]

def LCS(seq_a, seq_b):
    def backtrack(i, j):
        if i == 0 or j == 0:
            return []
        elif seq_a[i-1] == seq_b[j-1]:
            el = seq_a[i-1]
            return backtrack(i-1, j-1) + [el]
        elif table[i][j-1] > table[i-1][j]:
            return backtrack(i, j-1)
        return backtrack(i-1, j)

    table = LCSTable(seq_a, seq_b)
    return backtrack(len(seq_a), len(seq_b))
