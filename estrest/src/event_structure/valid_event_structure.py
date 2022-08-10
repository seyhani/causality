from typing import Set, List, FrozenSet, Dict

import utils
from event import Event

# noinspection SpellCheckingInspection
from event_structure.event_structure import EventStructure


class ValidEventStructure(EventStructure):
    events: Set[Event]
    min_enabling: Dict[Event, Set[FrozenSet[Event]]]
    conflict: Dict[Event, Set[Event]]
    configurations: Set[FrozenSet[Event]]

    def __init__(self, events: Set[Event]) -> None:
        super().__init__(events)
        self.min_enabling = {e: set() for e in events}

    def add_event(self, e: Event):
        super(ValidEventStructure, self).add_event(e)
        self.min_enabling[e] = set()

    def add_min_enabling(self, s: Set[Event], e: Event):
        if not s.union({e}).issubset(self.events):
            raise Exception("Unknown events")

        self.min_enabling[e].add(frozenset(s))

    def enables(self, s: Set[Event], e: Event):
        if not s.union({e}).issubset(self.events):
            raise Exception("Unknown events")

        return any([ms.issubset(s) for ms in self.min_enabling[e]])

    def min_enables(self, s: Set[Event], e: Event):
        if not s.union({e}).issubset(self.events):
            raise Exception("Unknown events")

        return s in self.min_enabling[e]
