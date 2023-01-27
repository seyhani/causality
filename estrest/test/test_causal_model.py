import unittest

from causality.causal_model import CausalModel, PrimitiveEvent

from causal_models import SUZY_BILLY


class TestCausalModel(unittest.TestCase):

    def test_recursive(self):
        m = CausalModel()
        m.add('A', lambda vals: True, [])
        m.add('B', lambda vals: True, [])
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
        m.add('A', lambda vals: True, [])
        m.add('B', lambda vals: False, [])
        m.add('C', lambda vals: vals['A'] and vals['B'], ['A', 'B'])
        m.add('D', lambda vals: vals['C'] and True, ['C'])
        m = m.intervene({'C': True})
        m.evaluate()
        self.assertEqual(m.vals['D'], True)

    def test_invalid_intervention(self):
        m = CausalModel()
        m.add('A', lambda vals: True, [])
        self.assertRaises(Exception, lambda: m.intervene({'X': True}))

    def test_w_projection(self):
        m = CausalModel()
        m.add('A', lambda vals: True, [])
        m.add('B', lambda vals: False, [])
        m.add('C', lambda vals: vals['A'] and vals['B'], ['A', 'B'])
        m.add('D', lambda vals: vals['C'] and True, ['C'])
        m_wp = m.get_w_projection(
            PrimitiveEvent('A', True), PrimitiveEvent('D', True)
        )

        m_wp.evaluate()

        self.assertEqual(m_wp.vals['A'], True)
        self.assertEqual(m_wp.vals['B'], False)
        self.assertEqual(m_wp.vals['C'], False)
        self.assertEqual(m_wp.vals['D'], False)

    def test_w_projection_suzy_billy_billy_is_not_cause(self):
        m = SUZY_BILLY
        m_wp = m.get_w_projection(
            PrimitiveEvent('BT', True), PrimitiveEvent('BS', True)
        )

        self.assertNotIn('ST', m_wp.fns)
        self.assertNotIn('ST', m_wp.deps)


if __name__ == '__main__':
    unittest.main()
