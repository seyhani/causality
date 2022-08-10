from itertools import chain, combinations
from typing import Set, List, Iterable

from event import Event, SyncedEvent, STAR


def repr_conflict(es):
    res = ""
    for e0, conflicts in es.conflict.items():
        for e1 in conflicts:
            res += repr(e0) + " # " + repr(e1) + "\n"
    return res


def repr_enabling(es):
    res = ""
    for e, enabling in es.min_enabling.items():
        for enabling_set in enabling:
            res += "{" + ",".join([repr(ee.label) for ee in enabling_set]) + "} -> " + repr(e.label) + "\n"
    return res


def repr_labels(es):
    return "{ " + ",".join(es.get_labels()) + "}"
    # return "{ " + ",".join(es.get_labels()) + "}"


def repr_labeling(es):
    return "\n".join([repr(e) + " -> " + repr(e.label) for e in es.events])


def disjoint_relabeling(labels):
    relabeling = {}
    for l in labels:
        relabeling[(l, 0)] = l
        relabeling[(l, 1)] = l
    return relabeling


def sem(expr):
    return "\\llbracket {} \\rrbracket".format(expr)


def is_conflict_free(es: set, conflict):
    for e in es:
        if not es.isdisjoint(conflict[e]):
            return False
    return True


def ids(events: Iterable[Event]):
    return set(map(lambda e: e.idx(), events))


def list_ids(event_sets: List[Set[Event]]):
    return list(map(lambda event_set: ids(event_set), event_sets))


def dual(i):
    return (i + 1) % 2


def async_event(e, i):
    if i == 0:
        return SyncedEvent(e, STAR)
    else:
        return SyncedEvent(STAR, e)


def powerset(iterable):
    s = set(iterable)
    return map(
        set,
        chain.from_iterable(
            combinations(s, r) for r in range(len(s) + 1)
        )
    )
