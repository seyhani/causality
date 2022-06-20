import unittest

from event import Event, SyncedEvent


class TestEvent(unittest.TestCase):

    def test_event(self):
        e0 = Event('a').prefix(0)
        e1 = Event('b').prefix(0)
        self.assertEqual(e0.id(), (0, 'a'))
        self.assertIn(e0, {e0})
        self.assertEqual(repr(e0), '(0, a)')
        self.assertNotEqual(e0, e1)

    def test_synced_event(self):
        e0 = Event('a')
        e1 = Event('b')
        e = SyncedEvent(e0, e1)
        self.assertEqual(e.id(), ('a', 'b'))
        self.assertEqual(repr(e), '(a, b)')


if __name__ == '__main__':
    unittest.main()
