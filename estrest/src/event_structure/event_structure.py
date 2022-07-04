import itertools
from copy import deepcopy
from typing import Set, List, FrozenSet

from estrest.src import utils
from estrest.src.event import Event, SyncedEvent, STAR


# noinspection SpellCheckingInspection
class EventStructure:
    def __init__(self) -> None:
        self.events = set()
        self.enabling = {}  # Event -> List[Set[Event]]
        self.conflict = {}  # Event -> Set[Event]

    def get_event(self, _id: tuple):
        for e in self.events:
            if e.idx() == _id:
                return e
        return None

    def get_enabling(self, _id: tuple):
        return self.enabling[self.get_event(_id)]

    def get_conflict(self, _id: tuple):
        return self.conflict[self.get_event(_id)]

    def prefix_events(self, prefix):
        for e in self.events:
            e.prefix(prefix)

    def update(self, es: "EventStructure"):
        self.events.update(es.events)
        self.enabling.update(es.enabling)
        self.conflict.update(es.conflict)

    def add_event(self, event: Event):
        self.events.update([event])
        self.enabling[event] = [set()]
        self.conflict[event] = set()

    def prefix(self, alpha: str):
        es = deepcopy(self)
        event = Event(alpha)

        # a -> (0,a)
        event.prefix(0)

        # x -> (1,x)
        for e in es.events:
            e.prefix(1)

        # Add (0,a) to all enabling sets
        for enabling in es.enabling.values():
            for ee in enabling:
                ee.update([event])

        es.add_event(event)

        return es

    def plus(self, es1):
        res = EventStructure()
        es = {0: deepcopy(self), 1: deepcopy(es1)}

        for i in (0, 1):
            es[i].prefix_events(i)  # Disjoint union
            res.update(es[i])

        for i in (0, 1):
            for e in es[i].events:
                # Each pair of events from different ESs are in conflict
                res.conflict[e].update([ce for ce in es[utils.dual(i)].events])

        return res

    def times(self, es1):
        res = EventStructure()
        es = {0: deepcopy(self), 1: deepcopy(es1)}

        events = set()

        # Add async events
        for i in (0, 1):
            for e in es[i].events:
                events.update([utils.async_event(e, i)])

        # Add sync events
        for e0 in es[0].events:
            for e1 in es[1].events:
                events.update([SyncedEvent(e0, e1)])

        # Projection: from event e0 to the set of events of form (e0,@)
        # @: anything
        p = {0: dict(), 1: dict()}
        for i in (0, 1):
            for e in es[i].events:
                p[i][e] = set()

        for e in events:
            for i in (0, 1):
                if e.get_event(i) != STAR:
                    p[i][e.get_event(i)].update([e])

        # Constructing conflicts
        conflicts = {}
        for e in events:
            conflicts[e] = set()

            # c[i]: conflicts of the event in es[i]
            c = {0: set(), 1: set()}
            for i in (0, 1):
                if e.get_event(i) != STAR:
                    c[i] = es[i].conflict[e.get_event(i)]

            for ec in events:
                for i in (0, 1):
                    if ec.get_event(i) in c[i]:  # if ec's ith component conflicts with e's ith component
                        conflicts[e].update([ec])
                # Conflicts of the form (a,b)#(a,c)
                if ec != e and (ec.get_event(0) == e.get_event(0) or ec.get_event(1) == e.get_event(1)):
                    conflicts[e].update([ec])

        res.conflict = conflicts

        # Constructing enabling
        enabling = {}
        for e in events:
            enabling[e] = []
            enabling_synced = {0: [], 1: []}
            for i in (0, 1):
                if e[i] == STAR:
                    enabling_synced[i].extend([set()])
                else:
                    for enabling_set in es[i].enabling[e[i]]:  # Enabling set of ith component

                        # Map each element of enabling set to a set of syncrhoinzed events
                        projected = list(map(lambda x: p[i][x], enabling_set))

                        # Cartesian product of the projected elements
                        synced_enabling_sets = list(map(lambda x: set(x), set(itertools.product(*projected))))

                        # Filter out conflicting enabling sets
                        synced_enabling_sets = filter(lambda esp: utils.is_conflict_free(esp, conflicts),
                                                      synced_enabling_sets)

                        enabling_synced[i].extend(synced_enabling_sets)

            for se0 in enabling_synced[0]:
                for se1 in enabling_synced[1]:
                    if utils.is_conflict_free(se0.union(se1), conflicts):
                        enabling[e].append(se0.union(se1))

        res.enabling = enabling
        res.events = events
        return res

    def restrict(self, labels):
        es = EventStructure()
        for e in self.events:
            if e.label in labels:
                es.events.update([e])

        for e, conflict in self.conflict.items():
            es.conflict[e] = set()
            if e.label in labels:
                for c in conflict:
                    if c.label in labels:
                        es.conflict[e].update([c])

        for e, enabling in self.enabling.items():
            es.enabling[e] = []
            if e.label in labels:
                for enabling_set in enabling:
                    is_valid = True
                    for ee in enabling_set:
                        if ee.label not in labels:
                            is_valid = False
                            break
                    if is_valid:
                        es.enabling[e].append(enabling_set)

        return es

    def relabel(self, relabeling):
        es = deepcopy(self)
        for e in es.events:
            if e.label in relabeling:
                e.label = relabeling[e.label]
        return es

    def conflict_free(self, es: Set[Event]):
        return utils.is_conflict_free(es, self.conflict)

    def get_labels(self):
        return set(map(lambda x: repr(x.label).replace("\'", ""), self.events))

    # Pre-conditions:
    # * x is a subset of self.events
    # * If event e is enabled by the null set, we have:
    #    enabling[e] = [{}]
    def is_configuration(self, x: Set[Event]):
        queue: List[Set[Event]] = [set()]
        visited: Set[FrozenSet[Event]] = set(frozenset())
        while queue:
            conf = queue.pop(0)
            for e in self.events - conf:
                conf_new = conf.union({e})
                if not self.conflict_free(conf_new):
                    continue
                for s in self.enabling[e]:
                    if s.issubset(conf_new):
                        visited.add(frozenset(conf_new))
                        queue.append(conf_new)
                        break

        return frozenset(x) in visited

    def __eq__(self, other):
        if not isinstance(other, EventStructure):
            return False
        return self.events == other.events

    def __repr__(self) -> str:
        return ",".join(map(repr, self.events))
