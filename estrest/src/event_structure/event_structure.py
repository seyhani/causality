from typing import Set, List, FrozenSet, Dict

import utils
from event import Event


# noinspection SpellCheckingInspection
class EventStructure:
    events: Set[Event]
    enabling: Dict[Event, Set[FrozenSet[Event]]]
    conflict: Dict[Event, Set[Event]]
    configurations: Set[FrozenSet[Event]]

    def __init__(self, events=set()) -> None:
        self.events = events
        self.enabling = {}
        self.conflict = {}
        self.configurations = set()

    def add_enabling(self, s: Set[Event], e: Event):
        for ep in s.union({e}) - self.events:
            self.__add_event(ep)
        self.enabling[e].add(frozenset(s))

    def add_conflict(self, e: Event, ep: Event):
        for e_ in {e, ep}.difference(self.events):
            self.__add_event(e_)
        self.conflict[e].add(ep)
        self.conflict[ep].add(e)

    def get_event(self, _id: tuple):
        for e in self.events:
            if e.idx() == _id:
                return e
        return None

    def get_enabling(self, _id: tuple):
        return self.enabling[self.get_event(_id)]

    def get_conflict(self, _id: tuple):
        return self.conflict[self.get_event(_id)]

    def conflict_free(self, es: Set[Event]):
        return utils.is_conflict_free(es, self.conflict)

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
                if not [s_ for s_ in self.min_enabling[e] if s_.issubset(conf_new)]:
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
