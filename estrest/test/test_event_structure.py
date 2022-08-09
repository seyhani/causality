import unittest

from event import Event
from event_structure import EventStructureTerm
from event_structure.event_structure import EventStructure
from utils import ids, list_ids


class TestEventStructure(unittest.TestCase):
    def test_enabling(self):
        es = EventStructure()
        a, b, c = Event('a'), Event('b'), Event('c')
        es.add_enabling(set(), a)
        es.add_enabling(set(), b)
        es.add_enabling({a, b}, c)
        es.build_configurations()
        self.assertTrue(es.is_configuration({a, b, c}))
        self.assertFalse(es.is_configuration({b, c}))
        self.assertFalse(es.is_configuration({a, c}))

    def test_conflict(self):
        es = EventStructure()
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
