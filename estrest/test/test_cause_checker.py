import unittest

from causal_models import SUZY_BILLY
from causality.causal_model import CausalModel
from causality.cause_checker import CauseChecker, PrimitiveEvent, Witness


class TestCausalModel(unittest.TestCase):

    def test_recursive(self):
        m = CausalModel()
        m.add_constant('A', True)
        m.add_constant('B', True)
        m.add('C', lambda vals: vals['A'] or vals['B'], ['A', 'B'])
        cause = PrimitiveEvent('A', True)
        effect = PrimitiveEvent('C', True)
        witness = Witness({'B'}, {'B': False}, False)
        checker = CauseChecker(m, cause, effect, witness)
        checker.check_acs()

    def test_suzy_billy_suzy_is_cause(self):
        m = SUZY_BILLY
        m.evaluate()
        effect = PrimitiveEvent('BS', True)
        cause = PrimitiveEvent('ST', True)
        witness = Witness({'BT'}, {'BT': False}, False)
        checker = CauseChecker(m, cause, effect, witness)
        self.assertTrue(m.satisfies(effect))
        self.assertTrue(checker.check_acs())

    def test_suzy_billy_billy_is_not_cause(self):
        m = SUZY_BILLY
        m.evaluate()
        effect = PrimitiveEvent('BS', True)
        cause = PrimitiveEvent('BT', True)
        witness = Witness({'ST'}, {'ST': False}, False)
        checker = CauseChecker(m, cause, effect, witness)
        self.assertTrue(m.satisfies(effect))
        self.assertFalse(checker.check_acs())


if __name__ == '__main__':
    unittest.main()
