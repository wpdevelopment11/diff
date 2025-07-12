from diff import diff_hm
from diff.diff_format import get_hunks
from parser import parse_args

args = parse_args(description="Print the diff. In other words, print the changes needs to be done to the first file to produce the second one.")

lcs = diff_hm.LCS(args.fileA, args.fileB)
hunks = get_hunks(lcs, args.fileA, args.fileB)

for hunk in hunks:
    print(hunk)
