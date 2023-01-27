import unittest

from event import Event
from mapper import EventStructureCausalModel
from mapper.event_structure_var import ConflictVar, EnablingVar


class TestEventStructureCausalModel(unittest.TestCase):
    def test_get_configuration_deps(self):
        a, b, c = Event('a'), Event('b'), Event('c')
        deps = EventStructureCausalModel.\
            get_configuration_deps({a, b, c})
        deps = set(map(repr, deps))
        self.assertIn(repr(ConflictVar(a, b)), deps)
        self.assertIn(repr(EnablingVar({a, b}, c)), deps)
        self.assertNotIn(repr(EnablingVar({a}, a)), deps)
