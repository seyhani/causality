from itertools import chain, combinations
from typing import Dict, Set, List, Iterable, FrozenSet

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


# sort_rev represents the reversed topological sort
# of the fully visited DFS subtree.
def __dfs_internal(v, out: Dict, visited: Set, sort_rev: List):
    visited.add(v)
    for u in out[v]:
        if u not in visited:
            __dfs_internal(u, out, visited, sort_rev)
    sort_rev.append(v)


# out represents the out-edge relation for a given graph G:
# out[v] = { u | (v -> u) is in E(G) }
def topological_sort(out: Dict) -> List:
    visited = set()
    answer = []
    for v in out:
        if v not in visited:
            __dfs_internal(v, out, visited, answer)
    answer.reverse()
    return answer


# A vertex v is on a path from src to dst iff there is a path
# from src to v, and a path from v to dst.
def path_vertices(src, dst, out: Dict, in_: Dict) -> Set:
    visited_src_fwd, visited_dst_rev = set(), set()
    _sort_rev = []
    __dfs_internal(src, out, visited_src_fwd, _sort_rev)
    __dfs_internal(dst, in_, visited_dst_rev, _sort_rev)
    return visited_src_fwd.intersection(visited_dst_rev)
