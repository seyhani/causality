import unittest

from causality.causal_model import CausalModel
from causality.cause_checker import CauseChecker, PrimitiveEvent, Witness


class TestCausalModel(unittest.TestCase):

    def test_recursive(self):
        m = CausalModel()
        m.add('A', lambda vals: True)
        m.add('B', lambda vals: True)
        m.add('C', lambda vals: vals['A'] or vals['B'])
        cause = PrimitiveEvent('A', True)
        effect = PrimitiveEvent('C', True)
        witness = Witness('B', False, False)
        checker = CauseChecker(m, cause, effect, witness)
        self.assertTrue(checker.check_ac1())
        self.assertTrue(checker.check_ac2a())


if __name__ == '__main__':
    unittest.main()
