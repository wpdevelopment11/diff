# Implementation of the Hunt-McIlroy algorithm and the diff command-line utility

## Command-line utilities

### diff-cli.py - Print the diff of the two files or strings

The diff is printed in the [normal output format].

<details>
    <summary>Usage:</summary>

```
diff-cli.py [-h] [-s] fileA fileB

Print the diff. In other words, print the changes needs to be done to the first file to produce the second one.

Positional arguments:
  fileA          Path to the first file
  fileB          Path to the second file

Options:
  -s, --strings  Interpret both arguments as strings
  -h, --help     show this help message and exit
```

</details>

### lcs-cli.py - Print the longest common subsequence between the two files or strings

<details>
    <summary>Usage:</summary>

```
lcs-cli.py [-h] [-s] fileA fileB

Print the longest common subsequence (LCS) between the two files.

Positional arguments:
  fileA          Path to the first file
  fileB          Path to the second file

Options:
  -s, --strings  Interpret both arguments as strings
  -h, --help     show this help message and exit
```

</details>

## API

Find the longest common subsequence (LCS) of the two sequences.

```
LCS(seq_a, seq_b)
```

---

Given the LCS and the two sequences create the hunks of differences.

```
get_hunks(lcs, seq_a, seq_b)
```

## Run tests

```bash
python -m unittest discover test
```

[normal output format]: https://www.gnu.org/software/diffutils/manual/html_node/Detailed-Normal.html
