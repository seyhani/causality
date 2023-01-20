import unittest

import utils
from causality.cause_checker import PrimitiveEvent, Witness
from causality.event_structure_cause_checker import EventStructureCausalChecker
from event import Event
from event_structure import ValidEventStructureTerm
from event_structure.valid_event_structure import ValidEventStructure
from mapper.event_structure_var import MinEnablingVar, ConflictVar


class TestCausalModel(unittest.TestCase):

    def test_es_expression(self):
        ab = ValidEventStructureTerm(set()) \
            .prefix('b').prefix('a')
        cd = ValidEventStructureTerm(set()) \
            .prefix('d').prefix('c')
        es = ab.plus(cd)

        a = es.find_events_by_label('a').pop()
        b = es.find_events_by_label('b').pop()
        c = es.find_events_by_label('c').pop()
        d = es.find_events_by_label('d').pop()

        cause = PrimitiveEvent(MinEnablingVar({b}, a), False)
        witness = Witness({}, True)
        checker = EventStructureCausalChecker(es, [{a, b}], cause, witness)
        self.assertTrue(checker.is_cause())

        cause = PrimitiveEvent(ConflictVar(a, b), False)
        witness = Witness({}, True)
        checker = EventStructureCausalChecker(es, [{a, b}], cause, witness)
        self.assertTrue(checker.is_cause())

        cause = PrimitiveEvent(MinEnablingVar({d}, c), False)
        witness = Witness({}, True)
        checker = EventStructureCausalChecker(es, [{a, b}], cause, witness)
        self.assertFalse(checker.is_cause())

    def test_recursive_model(self):
        a, b, c = Event('a'), Event('b'), Event('c')
        es = ValidEventStructure({a, b, c})
        es.add_min_enabling(set(), a)
        es.add_min_enabling(set(), b)
        es.add_min_enabling({a, b}, c)
        es.build_configurations()
        cause = PrimitiveEvent('C(a, b)', False)
        witness = Witness({}, True)
        checker = EventStructureCausalChecker(es, [{a, b, c}], cause, witness)
        self.assertTrue(checker.is_cause())

    def test_no_cause(self):
        a, b, c = Event('a'), Event('b'), Event('c')
        es = ValidEventStructure({a, b, c})
        es.add_min_enabling(set(), a)
        es.add_min_enabling(set(), b)
        es.add_min_enabling({a, b}, c)
        es.build_configurations()
        cause = PrimitiveEvent('M([], c)', False)
        witness = Witness({}, True)
        checker = EventStructureCausalChecker(es, [{a, b, c}], cause, witness)
        self.assertFalse(checker.is_cause())

    def test_blacklist(self):
        ab1, ab2, ab3, ac1, ac2, ac3 = Event('ab1'), Event('ab2'), Event('ab3'), \
                                       Event('ac1'), Event('ac2'), Event('ac3')
        ad1, ad2, p1, p2, q1, q2 = Event('ad1'), Event('ad2'), Event('p1'), Event('p2'), \
                                   Event('q1'), Event('q2')
        es = ValidEventStructure({ab1, ab2, ab3, ac1, ac2, ac3, ad1, ad2, p1, p2, q1, q2})

        es.add_min_enabling(set(), ab1)
        es.add_min_enabling(set(), p1)
        es.add_min_enabling(set(), q2)
        es.add_min_enabling({p1}, ac1)
        es.add_min_enabling({p1}, ab2)
        es.add_min_enabling({p1}, q1)
        es.add_min_enabling({p1, q1}, ac2)
        es.add_min_enabling({p1, q1}, ad1)
        es.add_min_enabling({q2}, p2)
        es.add_min_enabling({q2}, ab3)
        es.add_min_enabling({p2, q2}, ad2)
        es.add_min_enabling({p2, q2}, ac3)

        es.add_conflict_set({ab1, p1, q2})
        es.add_conflict_set({ac1, ab2, q1})
        es.add_conflict_set({ac2, ad1})
        es.add_conflict_set({p2, ab3})
        es.add_conflict_set({ad2, ac3})

        es.build_configurations()

        c1 = {p1, q1, ad1}
        c2 = {p2, q2, ad2}

        self.assertTrue(es.is_configuration(c1))
        self.assertTrue(es.is_configuration(c2))

        cause = PrimitiveEvent('C(p1, q1)', False)
        witness = Witness({'C(p2, q2)': True}, True)
        checker = EventStructureCausalChecker(es, [c1, c2], cause, witness)
        self.assertTrue(checker.is_cause())


if __name__ == '__main__':
    unittest.main()
