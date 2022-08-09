import unittest

from causal_models import SUZY_BILLY
from causality.causal_model import CausalModel
from causality.cause_checker import CauseChecker, PrimitiveEvent, Witness
from causality.event_structure_cause_checker import EventStructureCausalChecker
from event import Event
from event_structure.event_structure import EventStructure


class TestCausalModel(unittest.TestCase):

    def test_recursive(self):
        a, b, c = Event('a'), Event('b'), Event('c')
        es = EventStructure()
        es.add_enabling(set(), a)
        es.add_enabling(set(), b)
        es.add_enabling({a, b}, c)
        es.build_configurations()
        cause = PrimitiveEvent('C(a, b)', False)
        witness = Witness(None, None, True)
        checker = EventStructureCausalChecker(es, [{a, b, c}], cause, witness)
        self.assertTrue(checker.is_cause())

    def test_no_cause(self):
        a, b, c = Event('a'), Event('b'), Event('c')
        es = EventStructure()
        es.add_enabling(set(), a)
        es.add_enabling(set(), b)
        es.add_enabling({a, b}, c)
        es.build_configurations()
        cause = PrimitiveEvent('M([], c)', False)
        witness = Witness(None, None, True)
        checker = EventStructureCausalChecker(es, [{a, b, c}], cause, witness)
        self.assertFalse(checker.is_cause())


if __name__ == '__main__':
    unittest.main()
