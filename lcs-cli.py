from diff import diff_hm
from parser import parse_args

args = parse_args(description="Print the longest common subsequence (LCS) between the two files.")

lcs = diff_hm.LCS(args.fileA, args.fileB)

if args.strings:
    lcs = "".join(lcs)
    print(lcs)
else:
    for line in lcs:
        print(line)
