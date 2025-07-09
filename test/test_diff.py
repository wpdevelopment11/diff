from collections import namedtuple

import unittest

from diff import diff
from diff import diff_hm

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
        textA = [
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

        textB = [
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

        self.assertEqual(diff.LCS(textA, textB), result)
        self.assertEqual(diff_hm.LCS(textA, textB), result)
