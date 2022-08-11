import unittest

from event_structure import ValidEventStructureTerm
from utils import ids, ids_set


class TestEventStructureTerm(unittest.TestCase):

    def test_prefix(self):
        es = ValidEventStructureTerm(set()).prefix('b').prefix('a')
        a = es.get_event((0, 'a'))
        b = es.get_event((1, 0, 'b'))
        self.assertIsNotNone(a)
        self.assertIsNotNone(b)
        self.assertTrue(es.enables({a}, b))

    def test_sum(self):
        a = ValidEventStructureTerm(set()).prefix('a')
        b = ValidEventStructureTerm(set()).prefix('b')
        s = a.plus(b)
        self.assertIn((0, 0, 'a'), ids(s.events))
        self.assertIn((1, 0, 'b'), ids(s.events))
        self.assertIn((0, 0, 'a'), ids(s.get_conflict((1, 0, 'b'))))
        self.assertIn((1, 0, 'b'), ids(s.get_conflict((0, 0, 'a'))))

    def test_product(self):
        a = ValidEventStructureTerm(set()).prefix('a')
        b = ValidEventStructureTerm(set()).prefix('b')
        p = a.times(b)
        self.assertIn(('a', '*'), ids(p.events))
        self.assertIn(('*', 'b'), ids(p.events))
        self.assertIn(('a', 'b'), ids(p.events))

    def test_product_prefix(self):
        p = ValidEventStructureTerm(set()).prefix('b').prefix('a').times(
            ValidEventStructureTerm(set()).prefix('y').prefix('x'))

        self.assertTrue(p.enables(set(), p.get_event(('a', '*'))))
        self.assertIn(('a', 'y'), ids(p.get_conflict(('a', 'x'))))
        self.assertTrue(p.enables({p.get_event(('a', '*')), p.get_event(('*', 'x'))}, p.get_event(('b', 'y'))))
        self.assertTrue(p.conflicts(p.get_event(('a', '*')), p.get_event(('a', 'x'))))

    def test_restrict(self):
        s = ValidEventStructureTerm(set()).prefix('a').plus(ValidEventStructureTerm(set()).prefix('b'))
        self.assertIn((1, 0, 'b'), ids(s.events))
        self.assertIn((1, 0, 'b'), ids(s.get_conflict((0, 0, 'a'))))
        s = s.restrict({'a'})
        self.assertNotIn((1, 0, 'b'), ids(s.events))
        self.assertNotIn((1, 0, 'b'), ids(s.get_conflict((0, 0, 'a'))))

    def test_relabeling(self):
        p = ValidEventStructureTerm(set()).prefix('a').times(ValidEventStructureTerm(set()).prefix('b'))
        p = p.relabel({('a', '*'): 'x', ('*', 'b'): 'y'})
        self.assertEqual(p.get_labels(), {'(a, b)', 'x', 'y'})


if __name__ == '__main__':
    unittest.main()
