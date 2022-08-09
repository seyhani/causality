import unittest

from event_structure import EventStructureTerm
from utils import ids, list_ids


class TestEventStructureTerm(unittest.TestCase):

    def test_prefix(self):
        es = EventStructureTerm().prefix('b').prefix('a')
        self.assertIsNotNone(es.get_event((0, 'a')))
        self.assertIsNotNone(es.get_event((1, 0, 'b')))
        self.assertIn({(0, 'a')}, list_ids(es.get_enabling((1, 0, 'b'))))

    def test_sum(self):
        a = EventStructureTerm().prefix('a')
        b = EventStructureTerm().prefix('b')
        s = a.plus(b)
        self.assertIn((0, 0, 'a'), ids(s.events))
        self.assertIn((1, 0, 'b'), ids(s.events))
        self.assertIn((0, 0, 'a'), ids(s.get_conflict((1, 0, 'b'))))
        self.assertIn((1, 0, 'b'), ids(s.get_conflict((0, 0, 'a'))))

    def test_product(self):
        a = EventStructureTerm().prefix('a')
        b = EventStructureTerm().prefix('b')
        p = a.times(b)
        self.assertIn(('a', '*'), ids(p.events))
        self.assertIn(('*', 'b'), ids(p.events))
        self.assertIn(('a', 'b'), ids(p.events))

    def test_product_prefix(self):
        p = EventStructureTerm().prefix('b').prefix('a').times(EventStructureTerm().prefix('y').prefix('x'))
        self.assertIn(set(), p.get_enabling(('a', '*')))
        self.assertIn(('a', 'y'), ids(p.get_conflict(('a', 'x'))))
        self.assertNotIn({('a', 'x'), ('b', 'x')}, list_ids(p.get_enabling(('b', 'y'))))

    def test_restrict(self):
        s = EventStructureTerm().prefix('a').plus(EventStructureTerm().prefix('b'))
        self.assertIn((1, 0, 'b'), ids(s.events))
        self.assertIn((1, 0, 'b'), ids(s.get_conflict((0, 0, 'a'))))
        s = s.restrict({'a'})
        self.assertNotIn((1, 0, 'b'), ids(s.events))
        self.assertNotIn((1, 0, 'b'), ids(s.get_conflict((0, 0, 'a'))))

    def test_relabeling(self):
        p = EventStructureTerm().prefix('a').times(EventStructureTerm().prefix('b'))
        p = p.relabel({('a', '*'): 'x', ('*', 'b'): 'y'})
        self.assertEqual(p.get_labels(), {'(a, b)', 'x', 'y'})


if __name__ == '__main__':
    unittest.main()
