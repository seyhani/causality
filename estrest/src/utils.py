from itertools import chain, combinations
from typing import Dict, Set, List, Iterable, FrozenSet, TypeVar

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
    return frozenset(map(lambda e: e.idx(), events))


def ids_set(event_sets: Set[FrozenSet[Event]]):
    return frozenset(map(lambda event_set: ids(event_set), event_sets))


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


def superset_closure(elements: FrozenSet, subset: FrozenSet):
    return set(map(lambda s: frozenset(s.union(subset)), powerset(elements - subset)))

T = TypeVar("T")
def __topol_sort_internal(
    v: T,
    out: Dict[T, List[T]],
    visited: Set[T] = set(),
    answer: List[T] = []
) -> List[T]:
    visited.add(v)
    for u in out[v]:
        if u not in visited:
            __topol_sort_internal(u, out, visited, answer)
    answer.append(v)
    return answer


# out represents the out-edge relation for a given graph G:
# out[v] = { u | (v -> u) is in E(G) }
def topological_sort(
    out: Dict[T, List[T]]
) -> List[T]:
    visited = set()
    answer = []
    for v in out:
        if v not in visited:
            __topol_sort_internal(v, out, visited, answer)
    return answer.reverse()
    