import argparse

def readlines(path):
    f = open(path, encoding="utf-8")
    lines = [line.removesuffix("\n") for line in f.readlines()]
    return lines

def parse_args(*args, **kwargs):
    parser = argparse.ArgumentParser(*args, **kwargs)
    parser.add_argument("-s", "--strings", action="store_true", help="Interpret both arguments as strings")
    parser.add_argument("fileA", help="Path to the first file")
    parser.add_argument("fileB", help="Path to the second file")

    args = parser.parse_args()

    if not args.strings:
        args.fileA = readlines(args.fileA)
        args.fileB = readlines(args.fileB)
    return args
