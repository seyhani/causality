import itertools
from copy import deepcopy

import utils
from event import Event, SyncedEvent, STAR


class ES:
    def __init__(self) -> None:
        self.events = set()
        self.enabling = {}
        self.conflict = {}

    def mutate(self, idx):
        for e in self.events:
            e.mutate(idx)

    def disjoint(self, idx):
        for e in self.events:
            e.disjoint(idx)

    def update(self, es):
        self.events.update(es.events)
        self.enabling.update(es.enabling)
        self.conflict.update(es.conflict)

    def add_event(self, event):
        self.events.update([event])
        self.enabling[event] = [set()]
        self.conflict[event] = set()

    def prefix(self, alpha):
        es = deepcopy(self)
        event = Event(alpha)
        event.mutate(0)
        for e in es.events:
            e.mutate(1)
        for _, enabling in es.enabling.items():
            for ee in enabling:
                ee.update([event])

        es.add_event(event)
        return es

    def sum(self, es1):
        res = ES()
        es0 = deepcopy(self)
        es1 = deepcopy(es1)
        es0.mutate(0)
        es0.disjoint(0)
        res.update(es0)

        es1.mutate(1)
        es1.disjoint(1)
        res.update(es1)

        for e0 in es0.events:
            res.conflict[e0].update([e1 for e1 in es1.events])

        for e1 in es1.events:
            res.conflict[e1].update([e0 for e0 in es0.events])

        return res

    def product(self, es1):
        res = ES()
        es0 = deepcopy(self)
        es1 = deepcopy(es1)

        events = set()
        p0 = {}
        p1 = {}

        for e0 in es0.events:
            p0[e0] = set()
            events.update([SyncedEvent(e0, STAR)])

        for e1 in es1.events:
            p1[e1] = set()
            events.update([SyncedEvent(STAR, e1)])

        for e0 in es0.events:
            for e1 in es1.events:
                events.update([SyncedEvent(e0, e1)])

        for e in events:
            if e.e0 != STAR:
                p0[e.e0].update([e])
            if e.e1 != STAR:
                p1[e.e1].update([e])

        conflicts = {}
        for e in events:
            conflicts[e] = set()
            c0 = set()
            c1 = set()
            if e.e0 != STAR:
                c0 = es0.conflict[e.e0]
            if e.e1 != STAR:
                c1 = es1.conflict[e.e1]

            for ec in events:
                if ec.e0 in c0:
                    conflicts[e].update([ec])
                if ec.e1 in c1:
                    conflicts[e].update([ec])
                if ec != e and (ec.e0 == e.e0 or ec.e1 == e.e1):
                    conflicts[e].update([ec])

        res.conflict = conflicts

        enabling = {}
        for e in events:
            enabling[e] = []

            enabling0_synced = []
            if e.e0 != STAR:
                enabling0 = es0.enabling[e.e0]
                for enabling_set in enabling0:
                    projected = list(map(lambda x: p0[x], enabling_set))
                    synced_enabling_event_sets = list(map(lambda x: set(x), set(itertools.product(*projected))))
                    synced_enabling_event_sets = filter(lambda es: utils.is_conflict_free(es, conflicts),
                                                        synced_enabling_event_sets)
                    enabling0_synced.extend(synced_enabling_event_sets)
            else:
                enabling[e] = enabling0_synced

            enabling1_synced = []
            if e.e1 != STAR:
                enabling1 = es1.enabling[e.e1]
                for enabling_set in enabling1:
                    projected = list(map(lambda x: p1[x], enabling_set))
                    synced_enabling_event_sets = list(map(lambda x: set(x), set(itertools.product(*projected))))
                    synced_enabling_event_sets = filter(lambda es: utils.is_conflict_free(es, conflicts),
                                                        synced_enabling_event_sets)
                    enabling1_synced.extend(synced_enabling_event_sets)
            else:
                enabling[e] = enabling1_synced

            if not enabling0_synced:
                enabling[e].extend(enabling1_synced)
            elif not enabling1_synced:
                enabling[e].extend(enabling0_synced)
            else:
                for se0 in enabling0_synced:
                    for se1 in enabling1_synced:
                        enabling[e].append(se0.union(se1))

        res.enabling = enabling
        res.events = events
        return res

    def restrict(self, labels):
        es = ES()
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
                    if is_valid:
                        es.enabling[e].append(enabling_set)

        return es

    def relabel(self, relabeling):
        es = deepcopy(self)
        for e in es.events:
            if e.label in relabeling:
                e.label = relabeling[e.label]
        return es

    def get_labels(self):
        return set(map(lambda x: repr(x.label).replace("\'", ""), self.events))

    def __repr__(self) -> str:
        return "\nES:\n" + \
               "Events: {}\n".format(len(self.events)) + "\n".join(repr(e) for e in self.events) + \
               "\n\nConflicts: {}\n".format(sum(len(cs) for _, cs in self.conflict.items())) + \
               utils.repr_conflict(self) + \
               "\nEnabling: {}\n".format(sum(len(es) for _, es in self.enabling.items())) + \
               utils.repr_enabling(self) + \
               "\nLabels: {}\n".format(len(self.get_labels())) + utils.repr_labels(self) + \
               "\nLabeling: \n" + utils.repr_labeling(self)
