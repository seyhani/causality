from typing import Set
from abc import ABC, abstractmethod

from event import Event
from src import ids


class EventStructureVar(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_events(self) -> Set[Event]:
        pass


class ConflictVar(EventStructureVar):
    e: Event
    ep: Event

    def __init__(self, e: Event, ep: Event):
        super().__init__()
        self.e = e
        self.ep = ep

    def get_events(self) -> Set[Event]:
        return {self.e, self.ep}

    # E.g. ConflictVar(Event('b'), Event('a')) -> 'C(a, b)'
    # Note the order of labels in return value
    def __repr__(self):
        ids_ = ids({self.e, self.ep})
        return f'C{tuple(sorted(ids_))}'.replace('\'', '')

# E.g. EnablingVar({Event('b'), Event('a')}, Event('c')) -> 'EN([a, b], c)'
     # Here the set is represented as a list of labels, as only a list can hold
     # their lexicographic order.
class EnablingVar(EventStructureVar):
    s: Set[Event]
    e: Event

    def __init__(self, s: Set[Event], e: Event):
        super().__init__()
        self.s = s
        self.e = e

    def get_events(self) -> Set[Event]:
        return self.s.union({self.e})

    def __repr__(self):
        ids_ = ids(self.s)
        return f'EN{sorted(ids_), self.e}'.replace('\'', '')


# E.g. MinEnablingVar({Event('b'), Event('a')}, Event('c')) -> 'M([a, b], c)'
# Here the set is represented as a list of labels, as only a list can hold
# their lexicographic order.
class MinEnablingVar(EventStructureVar):
    s: Set[Event]
    e: Event

    def __init__(self, s: Set[Event], e: Event):
        super().__init__()
        self.s = s
        self.e = e

    def get_events(self) -> Set[Event]:
        return self.s.union({self.e})

    def __repr__(self):
        ids_ = ids(self.s)
        return f'M{sorted(ids_), self.e}'.replace('\'', '')
