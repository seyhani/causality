import itertools
from copy import deepcopy
from typing import Set, List, FrozenSet

import utils
from event import Event, SyncedEvent, STAR


# noinspection SpellCheckingInspection
class EventStructure:
    def __init__(self, events=None, enabling=None, conflict=None) -> None:
        self.events = events or set()
        self.enabling = enabling or {}  # Event -> List[Set[Event]]
        self.conflict = conflict or {}  # Event -> Set[Event]
        self.configurations = set()  # Set[FrozenSet[Event]]

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

        # Add (0,a) as an event with no conflicts and no enablings
        es.events.update([event])
        es.enabling[event] = [set()]
        es.conflict[event] = set()

        # Configurations = {} union (
        #   {(0,a)} union x
        #   forall x in previous configurations
        # )
        es.configurations = {frozenset()}.union(
            set(
                map(
                    lambda c_: c_.union({event}),
                    es.configurations
                )
            )
        )

        return es

    def plus(self, es1):
        res = EventStructure()
        es = {0: deepcopy(self), 1: deepcopy(es1)}

        for i in (0, 1):
            es[i].prefix_events(i)  # Disjoint union
            res.events.update(es[i].events)
            res.enabling.update(es[i].enabling)
            res.conflict.update(es[i].conflict)

        for i in (0, 1):
            for e in es[i].events:
                # Each pair of events from different ESs are in conflict
                res.conflict[e].update([ce for ce in es[utils.dual(i)].events])

        # Sum configurations will be union of operand configurations
        # (with updated events)
        for i in (0, 1):
            res.configurations.update(es[i].configurations)

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

        res.build_configurations()

        return res

    def restrict(self, labels):
        es = deepcopy(self)
        res = EventStructure()
        for e in es.events:
            if e.label in labels:
                res.events.update([e])

        for e, conflict in es.conflict.items():
            res.conflict[e] = set()
            if e.label in labels:
                for c in conflict:
                    if c.label in labels:
                        res.conflict[e].update([c])

        for e, enabling in es.enabling.items():
            res.enabling[e] = []
            if e.label in labels:
                for enabling_set in enabling:
                    is_valid = True
                    for ee in enabling_set:
                        if ee.label not in labels:
                            is_valid = False
                            break
                    if is_valid:
                        res.enabling[e].append(enabling_set)

        for c in es.configurations:
            is_valid = True
            for e in c:
                if e.label not in labels:
                    is_valid = False
                    break
            if is_valid:
                res.configurations.update([c])
        return res

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
                if not [s_ for s_ in self.enabling[e] if s_.issubset(conf_new)]:
                    continue
                visited.add(frozenset(conf_new))
                queue.append(conf_new)
        self.configurations = visited

    def is_configuration(self, x: Set[Event]):
        return frozenset(x) in self.configurations

    def __eq__(self, other):
        if not isinstance(other, EventStructure):
            return False
        return self.events == other.events

    def __repr__(self) -> str:
        return ",".join(map(repr, self.events))
