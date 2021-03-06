import unittest

from event import Event
from event_structure import EventStructure
from utils import list_ids


class TestConfiguration(unittest.TestCase):

    def test_configuration_base(self):
        es = EventStructure()
        a, b = Event('a'), Event('b')
        es.events = {a, b}
        es.conflict = {a: set(), b: set()}
        es.enabling = {a: [set()], b: [{a}]}
        es.build_configurations()

        self.assertTrue(es.is_configuration({a, b}))

    def test_configuration_conflict(self):
        es = EventStructure()
        a, b = Event('a'), Event('b')
        es.events = {a, b}
        es.conflict = {a: {b}, b: {a}}
        es.enabling = {a: [set()], b: [set()]}
        es.build_configurations()

        self.assertFalse(es.is_configuration({a, b}))

    def test_configuration_not_secured(self):
        es = EventStructure()
        a, b, c = Event('a'), Event('b'), Event('c')
        es.events = {a, b, c}
        es.conflict = {a: set(), b: set(), c: set()}
        es.enabling = {a: [set()], b: [{a}], c: [{a, b}]}
        es.build_configurations()

        self.assertFalse(es.is_configuration({a, c}))
        self.assertFalse(es.is_configuration({b}))
        self.assertTrue(es.is_configuration({a, b}))
        self.assertTrue(es.is_configuration({a, b, c}))

    def test_configuration_generic(self):
        es = EventStructure()
        a, b, c, d, e = [Event(x) for x in 'abcde']
        es.events = {a, b, c, d, e}
        es.conflict = {a: set(), b: {d, e}, c: set(), d: {b}, e: {b}}
        es.enabling = {
            a: [set()],
            b: [{a}],
            d: [{a}],
            e: [{a, d}],
            c: [{a, b}, {a, d, e}]
        }
        es.build_configurations()

        self.assertTrue(es.is_configuration({a, c, d, e}))
        self.assertTrue(es.is_configuration({a, b, c}))

        self.assertFalse(es.is_configuration({a, b, c, d}))

    def test_configuration_prefix(self):
        a, b = Event('a'), Event('b')
        es = EventStructure(
            events={a, b},
            enabling={a: [set()], b: [{a}]},
            conflict={a: set(), b: set()},
        )
        es.build_configurations()

        self.assertIn({'a', 'b'}, list_ids(es.configurations))
        es = es.prefix('c')
        self.assertIn(
            {(0, 'c'), (1, 'a'), (1, 'b')},
            list_ids(es.configurations)
        )

    def test_configuration_plus(self):
        a, b = Event('a'), Event('b')
        es = {
            0: EventStructure(
                events={a},
                enabling={a: [set()]},
                conflict={a: set()},
            ),
            1: EventStructure(
                events={b},
                enabling={b: [set()]},
                conflict={b: set()},
            ),
        }

        es[0].build_configurations()
        es[1].build_configurations()

        es[2] = es[0].plus(es[1])

        self.assertIn({(0, 'a')}, list_ids(es[2].configurations))
        self.assertNotIn({(0, 'a'), (1, 'b')}, list_ids(es[2].configurations))

    def test_configuration_restrict(self):
        a, b = Event('a'), Event('b')
        es = EventStructure(
            events={a, b},
            enabling={a: [set()], b: [{a}]},
            conflict={a: set(), b: set()},
        )
        es.build_configurations()

        es = es.restrict({'a'})
        self.assertIn({'a'}, list_ids(es.configurations))
        self.assertNotIn({'a', 'b'}, list_ids(es.configurations))

    def test_configuration_relabelling(self):
        a, b = Event('a'), Event('b')
        es = EventStructure(
            events={a, b},
            enabling={a: [set()], b: [{a}]},
            conflict={a: set(), b: set()},
        )
        es.build_configurations()

        es = es.relabel({'a': 'c'})
        self.assertIn({'c', 'b'}, list_ids(es.configurations))
        self.assertNotIn({'a'}, list_ids(es.configurations))

    def test_configuration_times(self):
        a, b, c = Event('a'), Event('b'), Event('c')
        es = {
            0: EventStructure(
                events={a, b},
                enabling={a: [set()], b: [set()]},
                conflict={a: {b}, b: {a}},
            ),
            1: EventStructure(
                events={c},
                enabling={c: [set()]},
                conflict={c: set()},
            ),
        }

        es[2] = es[0].times(es[1])
        con = list_ids(es[2].configurations)

        self.assertIn({('a', '*')}, con)
        self.assertIn({('*', 'c')}, con)
        self.assertIn({('a', '*'), ('*', 'c')}, con)
        self.assertNotIn({('a', '*'), ('a', 'c')}, con)


if __name__ == '__main__':
    unittest.main()
