import unittest

from causality.causal_model import CausalModel


class TestCausalModel(unittest.TestCase):

    def test_recursive(self):
        m = CausalModel()
        m.add('A', lambda vals: True)
        m.add('B', lambda vals: True)
        m.add('C', lambda vals: vals['A'] and vals['B'], ['A', 'B'])
        m.evaluate()
        self.assertEqual(m.vals['C'], True)

    def test_non_recursive(self):
        m = CausalModel()
        m.add('A', lambda vals: vals['B'], ['B'])
        m.add('B', lambda vals: vals['A'], ['A'])
        m.evaluate()
        self.assertIsNone(m.vals['B'])

    def test_intervention(self):
        m = CausalModel()
        m.add('A', lambda vals: True)
        m.add('B', lambda vals: False)
        m.add('C', lambda vals: vals['A'] and vals['B'], ['A', 'B'])
        m.add('D', lambda vals: vals['C'] and True, ['C'])
        m = m.intervene({'C': True})
        m.evaluate()
        self.assertEqual(m.vals['D'], True)

    def test_invalid_intervention(self):
        m = CausalModel()
        m.add('A', lambda vals: True)
        self.assertRaises(Exception, lambda: m.intervene({'X': True}))


if __name__ == '__main__':
    unittest.main()
