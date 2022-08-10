from typing import Set, List, FrozenSet, Dict

import utils
from event import Event


# noinspection SpellCheckingInspection
class EventStructure:
    events: Set[Event]
    enabling: Dict[Event, Set[FrozenSet[Event]]]
    conflict: Dict[Event, Set[Event]]
    configurations: Set[FrozenSet[Event]]

    def __init__(self, events: Set[Event]) -> None:
        self.events = events
        self.enabling = {e: set() for e in self.events}
        self.conflict = {e: set() for e in self.events}
        self.configurations = set()

    def __enablings_conflict_free(self):
        return all(map(lambda s: self.conflict_free(s), set.union(*self.enabling.values())))

    def __enabling_closure_valid(self):
        for e in self.events:
            closure = set()
            for s in self.enabling[e]:
                closure = closure.union(utils.superset_closure(frozenset(self.events - {e}), s))
            if closure != self.enabling[e]:
                return False
        return True

    def is_valid(self):
        return self.__enablings_conflict_free() and self.__enabling_closure_valid()

    def add_event(self, e: Event):
        if e in self.events:
            raise Exception("Event already exists")
        self.events.add(e)
        self.enabling[e] = set()
        self.conflict[e] = set()

    def add_enabling(self, s: Set[Event], e: Event):
        if not s.union({e}).issubset(self.events):
            raise Exception("Unknown events")

        self.enabling[e].add(frozenset(s))

    def add_conflict(self, e: Event, ep: Event):
        if not {e, ep}.issubset(self.events):
            raise Exception("Unknown events")

        self.conflict[e].add(ep)
        self.conflict[ep].add(e)

    def enables(self, s: Set[Event], e: Event):
        if not s.union({e}).issubset(self.events):
            raise Exception("Unknown events")

        return s in self.enabling[e]

    def min_enables(self, s: Set[Event], e: Event):
        raise NotImplementedError()

    def get_event(self, _id: tuple):
        for e in self.events:
            if e.idx() == _id:
                return e
        return None

    def get_enabling(self, _id: tuple):
        return self.enabling[self.get_event(_id)]

    def get_conflict(self, _id: tuple):
        return self.conflict[self.get_event(_id)]

    def conflict_free(self, s: Set[Event]):
        return utils.is_conflict_free(s, self.conflict)

    def get_labels(self):
        return set(map(lambda x: repr(x.label).replace("\'", ""), self.events))

    # Pre-conditions:
    # * x is a subset of self.events
    # * If event e is enabled by the null set, we have:
    #    enabling[e] = [{}]
    def build_configurations(self):
        # BFS to find all configurations
        queue: List[Set[Event]] = [set()]
        visited: Set[FrozenSet[Event]] = {frozenset()}
        while queue:
            conf = queue.pop(0)
            for e in self.events - conf:
                conf_new = conf.union({e})
                if not self.conflict_free(conf_new):
                    continue
                if not self.enables(conf, e):
                    continue
                visited.add(frozenset(conf_new))
                queue.append(conf_new)
        self.configurations = visited

    def is_configuration(self, x: Set[Event]):
        return utils.ids(x) in map(utils.ids, self.configurations)

    def conflicts(self, e1: Event, e2: Event):
        return e1 in self.conflict[e2] and e2 in self.conflict[e1]

    def __repr__(self) -> str:
        return ",".join(map(repr, self.events))
