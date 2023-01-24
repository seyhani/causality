import unittest

import utils


class TestUtils(unittest.TestCase):

    def test_topological_sort(self):
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

    def test_path_vertices(self):
        out = {
            'a': ['b', 'c'],
            'b': ['c', 'f'],
            'c': ['d', 'e'],
            'd': [],
            'e': [],
            'f': [],
        }

        in_ = {
            'a': [],
            'b': ['a'],
            'c': ['a', 'b'],
            'd': ['c'],
            'e': ['c'],
            'f': ['b']
        }

        pv = utils.path_vertices('a', 'd', out, in_)

        self.assertEqual(pv, {'a', 'b', 'c', 'd'})
