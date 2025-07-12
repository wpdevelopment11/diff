from collections import namedtuple

import textwrap
import unittest

from diff import diff
from diff import diff_hm
from diff.diff_format import get_hunks
from diff.hunk import Add, Delete, Replace

class TestLCS(unittest.TestCase):
    def test_LCSTable(self):
        self.assertEqual(
            diff.LCSTable("GAC", "AGCAT"),
            [[0, 0, 0, 0, 0, 0],
             [0, 0, 1, 1, 1, 1],
             [0, 1, 1, 1, 2, 2],
             [0, 1, 1, 2, 2, 2]])

        self.assertEqual(
            diff.LCSTable("XMJYAUZ", "MZJAWXU"),
            [[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 1, 1],
             [0, 1, 1, 1, 1, 1, 1, 1],
             [0, 1, 1, 2, 2, 2, 2, 2],
             [0, 1, 1, 2, 2, 2, 2, 2],
             [0, 1, 1, 2, 3, 3, 3, 3],
             [0, 1, 1, 2, 3, 3, 3, 4],
             [0, 1, 2, 2, 3, 3, 3, 4]])

    def test_LCSLength(self):
        self.assertEqual(diff.LCSLength("GAC", "AGCAT"), 2)
        self.assertEqual(diff.LCSLength("XMJYAUZ", "MZJAWXU"), 4)

    def test_LCS(self):
        self.assertEqual(diff.LCS("GAC", "AGCAT"), ["G", "A"])
        self.assertEqual(diff.LCS("XMJYAUZ", "MZJAWXU"), ["M", "J", "A", "U"])
        self.assertEqual(diff.LCS("abcabba", "cbabac"), ["b", "a", "b", "a"])

        self.assertEqual(diff_hm.LCS("GAC", "AGCAT"), ["A", "C"])
        self.assertEqual(diff_hm.LCS("XMJYAUZ", "MZJAWXU"), ["M", "J", "A", "U"])
        self.assertEqual(diff_hm.LCS("abcabba", "cbabac"), ["c", "a", "b", "a"])

    def test_LCS_with_text(self):
        a = [
            "The Way that can be told of is not the eternal Way;",
            "The name that can be named is not the eternal name.",
            "The Nameless is the origin of Heaven and Earth;",
            "The Named is the mother of all things.",
            "Therefore let there always be non-being,",
            "  so we may see their subtlety,",
            "And let there always be being,",
            "  so we may see their outcome.",
            "The two are the same,",
            "But after they are produced,",
            "  they have different names.",
        ]

        b = [
            "The Nameless is the origin of Heaven and Earth;",
            "The named is the mother of all things.",
            "",
            "Therefore let there always be non-being,",
            "  so we may see their subtlety,",
            "And let there always be being,",
            "  so we may see their outcome.",
            "The two are the same,",
            "But after they are produced,",
            "  they have different names.",
            "They both may be called deep and profound.",
            "Deeper and more profound,",
            "The door of all subtleties!",
        ]

        result = [
            "The Nameless is the origin of Heaven and Earth;",
            "Therefore let there always be non-being,",
            "  so we may see their subtlety,",
            "And let there always be being,",
            "  so we may see their outcome.",
            "The two are the same,",
            "But after they are produced,",
            "  they have different names.",
        ]

        self.assertEqual(diff.LCS(a, b), result)
        self.assertEqual(diff_hm.LCS(a, b), result)

class TestDiff(unittest.TestCase):
    def to_list(self, seq):
        return list(seq) + [None]

    def test_get_hunks(self):
        a = "abcdefg"
        b = "wabxyze"
        hunks = [
            Add(0, self.to_list(b), (1, 1)),
            Replace(self.to_list(a), (3, 4), self.to_list(b), (4, 6)),
            Delete(self.to_list(a), (6, 7), 7)
        ]
        self.assertEqual(
            get_hunks(diff_hm.LCS("abcdefg", "wabxyze"), "abcdefg", "wabxyze"),
            hunks)

    def test_hunk_invert(self):
        a = "abcdefg"
        b = "wabxyze"
        hunks = [
            Add(0, self.to_list(b), (1, 1)),
            Replace(self.to_list(a), (3, 4), self.to_list(b), (4, 6)),
            Delete(self.to_list(a), (6, 7), 7)
        ]
        inverted = [
            Delete(self.to_list(b), (1, 1), 0),
            Replace(self.to_list(b), (4, 6), self.to_list(a), (3, 4)),
            Add(7, self.to_list(a), (6, 7))
        ]

        self.assertEqual(
            [hunk.invert() for hunk in hunks],
            inverted)

    def diff_to_str(self, a, b):
        lcs = diff_hm.LCS(a, b)
        hunks = get_hunks(lcs, a, b)
        res = "\n".join([str(hunk) for hunk in hunks])
        return res

    def test_diff_output(self):
        a = "abcdefg"
        b = "wabxyze"
        expected = textwrap.dedent("""\
        0a1
        > w
        3,4c4,6
        < c
        < d
        ---
        > x
        > y
        > z
        6,7d7
        < f
        < g""")

        inverted = textwrap.dedent("""\
        1d0
        < w
        4,6c3,4
        < x
        < y
        < z
        ---
        > c
        > d
        7a6,7
        > f
        > g""")

        res = self.diff_to_str(a, b)
        self.assertEqual(res, expected)

        res = self.diff_to_str(b, a)
        self.assertEqual(res, inverted)


    def test_diff_output_text(self):
        a = [
            "The Way that can be told of is not the eternal Way;",
            "The name that can be named is not the eternal name.",
            "The Nameless is the origin of Heaven and Earth;",
            "The Named is the mother of all things.",
            "Therefore let there always be non-being,",
            "  so we may see their subtlety,",
            "And let there always be being,",
            "  so we may see their outcome.",
            "The two are the same,",
            "But after they are produced,",
            "  they have different names.",
        ]
        b = [
            "The Nameless is the origin of Heaven and Earth;",
            "The named is the mother of all things.",
            "",
            "Therefore let there always be non-being,",
            "  so we may see their subtlety,",
            "And let there always be being,",
            "  so we may see their outcome.",
            "The two are the same,",
            "But after they are produced,",
            "  they have different names.",
            "They both may be called deep and profound.",
            "Deeper and more profound,",
            "The door of all subtleties!",
        ]
        expected = textwrap.dedent("""\
        1,2d0
        < The Way that can be told of is not the eternal Way;
        < The name that can be named is not the eternal name.
        4c2,3
        < The Named is the mother of all things.
        ---
        > The named is the mother of all things.
        >\x20
        11a11,13
        > They both may be called deep and profound.
        > Deeper and more profound,
        > The door of all subtleties!""")

        inverted = textwrap.dedent("""\
        0a1,2
        > The Way that can be told of is not the eternal Way;
        > The name that can be named is not the eternal name.
        2,3c4
        < The named is the mother of all things.
        <\x20
        ---
        > The Named is the mother of all things.
        11,13d11
        < They both may be called deep and profound.
        < Deeper and more profound,
        < The door of all subtleties!""")

        res = self.diff_to_str(a, b)
        self.assertEqual(res, expected)

        res = self.diff_to_str(b, a)
        self.assertEqual(res, inverted)
