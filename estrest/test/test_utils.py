import unittest

import utils


class TestUtils(unittest.TestCase):

    def test_topol_sort(self):
        out = {
            'a': ['b', 'c'],
            'b': ['c'],
            'c': ['d'],
            'd': []
        }

        ts = utils.topological_sort(out)

        self.assertTrue(ts.index('d') > ts.index('c'))
        self.assertTrue(ts.index('c') > ts.index('b'))
        self.assertTrue(ts.index('c') > ts.index('a'))
        self.assertTrue(ts.index('b') > ts.index('a'))
