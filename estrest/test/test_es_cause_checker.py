import unittest

from causal_models import SUZY_BILLY
from causality.causal_model import CausalModel
from causality.cause_checker import CauseChecker, PrimitiveEvent, Witness
from causality.event_structure_cause_checker import EventStructureCausalChecker
from event import Event
from event_structure.valid_event_structure import ValidEventStructure


class TestCausalModel(unittest.TestCase):

    def test_recursive(self):
        a, b, c = Event('a'), Event('b'), Event('c')
        es = ValidEventStructure()
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
        es = ValidEventStructure()
        es.add_enabling(set(), a)
        es.add_enabling(set(), b)
        es.add_enabling({a, b}, c)
        es.build_configurations()
        cause = PrimitiveEvent('M([], c)', False)
        witness = Witness(None, None, True)
        checker = EventStructureCausalChecker(es, [{a, b, c}], cause, witness)
        self.assertFalse(checker.is_cause())

    def test_blacklist(self):
        ab1, ab2, ab3, ac1, ac2 = Event('ab1'), Event('ab2'), Event('ab3'), Event('ac1'), Event('ac2')
        ad1, ad2, p1, p2, q1, q2 = Event('ad1'), Event('ad2'), Event('p1'), Event('p2'), Event('q1'), Event('q2')
        es = ValidEventStructure()
        es.add_enabling(set(), p1)
        es.add_enabling(set(), p2)
        es.build_configurations()
        print("s")
        # es.add_enabling(set(), ab1)
        # es.add_enabling(set(), p1)
        # es.add_enabling(set(), q2)


if __name__ == '__main__':
    unittest.main()
