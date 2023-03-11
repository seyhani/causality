import unittest

from causality import DependencyFinder


class TestDependencyFinder(unittest.TestCase):

    def test_simple(self):
        def f(vals): return vals['A'] & vals['B']
        result = DependencyFinder().find(f)

        self.assertEqual({'A', 'B'}, result)

    def test_complex(self):
        def f(vals):
            return vals['A'] & vals['B'] | (not vals['C']) ^ vals['D']
        result = DependencyFinder().find(f)
        self.assertEqual({'A', 'B', 'C', 'D'}, result)

    def test_nested(self):
        def f(vals):
            return g(vals) | h(vals)

        def g(vals):
            return vals['A'] & vals['B']

        def h(vals):
            return (not vals['B']) | vals['C']

        result = DependencyFinder().find(f)
        self.assertEqual({'A', 'B', 'C'}, result)
