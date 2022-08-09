from typing import Set

from event import Event
from src import ids


class EventStructureVar:
    def __init__(self):
        pass


class ConflictVar(EventStructureVar):
    e: Event
    ep: Event

    def __init__(self, e: Event, ep: Event):
        super().__init__()
        self.e = e
        self.ep = ep

    def __repr__(self):
        ids_ = ids({self.e, self.ep})
        return f'C{tuple(sorted(ids_))}'.replace('\'', '')


class EnablingVar(EventStructureVar):
    s: Set[Event]
    e: Event

    def __init__(self, s: Set[Event], e: Event):
        super().__init__()
        self.s = s
        self.e = e

    def __repr__(self):
        ids_ = ids(self.s)
        return f'EN{sorted(ids_), self.e}'.replace('\'', '')


class MinEnablingVar(EventStructureVar):
    s: Set[Event]
    e: Event

    def __init__(self, s: Set[Event], e: Event):
        super().__init__()
        self.s = s
        self.e = e

    def __repr__(self):
        ids_ = ids(self.s)
        return f'M{sorted(ids_), self.e}'.replace('\'', '')
