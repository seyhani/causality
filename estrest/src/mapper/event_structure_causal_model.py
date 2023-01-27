from typing import List, Set
from itertools import combinations

from causality import CausalModel
from causality.causal_model import FN
from event import Event
from event_structure.event_structure import EventStructure
from mapper.event_structure_var import EventStructureVar, ConflictVar, EnablingVar, MinEnablingVar
from utils import powerset


class EventStructureCausalModel(CausalModel):
    vars: Set[EventStructureVar]

    def __init__(self):
        super().__init__()
        self.vars = set()

    def add_conflict(self, e: Event, ep: Event, val):
        var = ConflictVar(e, ep)
        self.vars.add(var)
        self.add_constant(repr(var), val)

    def add_enabling(
        self, s: Set[Event], e: Event, fn: FN, deps: List[EventStructureVar]
    ):
        var = EnablingVar(s, e)
        self.vars.add(var)
        self.add(repr(var), fn, [repr(d) for d in deps])

    def add_min_enabling(
        self, s: Set[Event], e: Event, fn: FN, deps: List[EventStructureVar]
    ):
        var = MinEnablingVar(s, e)
        self.vars.add(var)
        self.add(repr(var), fn, [repr(d) for d in deps])

    def get_es(self) -> EventStructure:
        es = EventStructure(set())
        for e in set.union(*map(lambda v: v.get_events(), self.vars)):
            es.add_event(e)
        for var in self.vars:
            if self.vals[repr(var)]:
                if isinstance(var, ConflictVar):
                    es.add_conflict(var.e, var.ep)
                if isinstance(var, EnablingVar):
                    es.add_enabling(var.s, var.e)
        return es

    @staticmethod
    def get_configuration_deps(s: Set[Event]) -> Set[EventStructureVar]:
        deps = set()
        deps.update(
            ConflictVar(e, ep)
            for e, ep in combinations(s, 2)
        )
        for x in powerset(s):
            for e in s - x:
                deps.add(EnablingVar(x, e))
        return deps
