import unittest

from event import Event, SyncedEvent


class TestEvent(unittest.TestCase):

    def test_event(self):
        e0 = Event('a').prefix(0)
        e1 = Event('b').prefix(0)
        e2 = Event('a').prefix(0)

        self.assertEqual(e0.idx(), (0, 'a'))

        self.assertIn(e0, {e0})
        self.assertNotIn(e1, {e0})

        self.assertEqual(repr(e0), '(0, a)')

        self.assertEqual(e0.idx(), e2.idx())
        self.assertNotEqual(e0.idx(), e1.idx())

    def test_synced_event(self):
        e0 = Event('a')
        e1 = Event('b')
        e = SyncedEvent(e0, e1)
        self.assertEqual(e.idx(), ('a', 'b'))
        self.assertEqual(repr(e), '(a, b)')


if __name__ == '__main__':
    unittest.main()
