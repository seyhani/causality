import unittest

from event_structure.valid_event_structure import ValidEventStructure
from mapper import EventStructureToCausalModelMapper
from event_structure import ValidEventStructureTerm
from event import Event


class TestCausalModel(unittest.TestCase):

    def test_firewall(self):
        i, o = Event('i'), Event('o')
        es = ValidEventStructureTerm(
            events={i, o},
            conflict={i: set(), o: set()},
            enabling={i: {frozenset()}, o: {frozenset()}},
        )

        mp = EventStructureToCausalModelMapper(es)
        cm = mp.map()
        cm.evaluate()
        self.assertEqual(cm.vals['C(i, o)'], False)
        self.assertEqual(cm.vals['M([], i)'], True)
        self.assertEqual(cm.vals['M([], o)'], True)
        self.assertEqual(cm.vals['M([i], o)'], False)
        self.assertEqual(cm.vals['M([o], i)'], False)
        self.assertEqual(cm.vals['EN([], i)'], True)
        self.assertEqual(cm.vals['EN([], o)'], True)
        self.assertEqual(cm.vals['EN([i], o)'], True)
        self.assertEqual(cm.vals['EN([o], i)'], True)
        self.assertEqual(len(cm.vals), 9)

    def test_cm_with_conflict_and_enabling(self):
        a, b, c = Event('a'), Event('b'), Event('c')
        es = ValidEventStructureTerm(
            events={a, b, c},
            conflict={a: {b}, b: {a}, c: set()},
            enabling={
                a: {frozenset()},
                b: {frozenset()},
                c: {frozenset({a}), frozenset({b})}
            },
        )
        mp = EventStructureToCausalModelMapper(es)
        cm = mp.map()
        cm.evaluate()
        self.assertEqual(cm.vals['C(a, b)'], True)
        self.assertEqual(cm.vals['M([a], c)'], True)
        self.assertEqual(cm.vals['EN([b], a)'], True)
        self.assertEqual(cm.vals['EN([a, b], c)'], False)

    def test_intervention(self):
        a, b, c = Event('a'), Event('b'), Event('c')
        es = ValidEventStructure()
        es.add_enabling(set(), a)
        es.add_enabling(set(), b)
        es.add_enabling({a, b}, c)
        es.build_configurations()
        self.assertTrue(es.is_configuration({a, b, c}))

        cm = EventStructureToCausalModelMapper(es).map()
        cm.evaluate()
        esp = cm.get_es()
        esp.build_configurations()
        self.assertTrue(esp.is_configuration({a, b, c}))

        cm = cm.intervene({'C(a, b)': True})
        cm.evaluate()
        esp = cm.get_es()
        esp.build_configurations()
        self.assertFalse(esp.is_configuration({a, b, c}))
