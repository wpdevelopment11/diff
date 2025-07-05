from collections import namedtuple

import unittest

import diff

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
