import unittest

from event import Event
from event_structure import ValidEventStructureTerm
from event_structure.valid_event_structure import ValidEventStructure
from utils import ids, ids_set


class TestEventStructure(unittest.TestCase):
    def test_enabling(self):
        es = ValidEventStructure()
        a, b, c = Event('a'), Event('b'), Event('c')
        es.add_enabling(set(), a)
        es.add_enabling(set(), b)
        es.add_enabling({a, b}, c)
        es.build_configurations()
        self.assertTrue(es.is_configuration({a, b, c}))
        self.assertFalse(es.is_configuration({b, c}))
        self.assertFalse(es.is_configuration({a, c}))

    def test_conflict(self):
        es = ValidEventStructure()
        a, b, c = Event('a'), Event('b'), Event('c')
        es.add_enabling(set(), a)
        es.add_enabling(set(), b)
        es.add_enabling({a}, c)
        es.add_enabling({b}, c)
        es.add_conflict(a, b)
        es.build_configurations()
        self.assertFalse(es.is_configuration({a, b, c}))
        self.assertTrue(es.is_configuration({b, c}))
        self.assertTrue(es.is_configuration({a, c}))


if __name__ == '__main__':
    unittest.main()
