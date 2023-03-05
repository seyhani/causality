import unittest

from causality import DependencyFinder


class TestDependencyFinder(unittest.TestCase):
    
    def test_sound_and_complete(self):
        f = lambda vals: vals['A'] & vals['B']
        result = DependencyFinder().find(f)
        
        self.assertIn('A', result)
        self.assertIn('B', result)
        self.assertNotIn('C', result)
