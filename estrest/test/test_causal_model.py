import unittest

from causality.causal_model import CausalModel


class TestCausalModel(unittest.TestCase):

    def test_recursive(self):
        m = CausalModel()
        m.add('A', lambda vals: True)
        m.add('B', lambda vals: True)
        m.add('C', lambda vals: vals['A'] and vals['B'])
        m.evaluate()
        print(m.vals['C'])

    def test_non_recursive(self):
        m = CausalModel()
        m.add('A', lambda vals: vals['B'])
        m.add('B', lambda vals: vals['A'])
        m.evaluate()
        print(m.vals['B'])


if __name__ == '__main__':
    unittest.main()
