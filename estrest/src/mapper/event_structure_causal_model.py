from typing import Set

from causality import CausalModel
from causality.causal_model import FN
from event import Event
from event_structure.event_structure import EventStructure
from mapper.event_structure_var import EventStructureVar, ConflictVar, EnablingVar, MinEnablingVar


class EventStructureCausalModel(CausalModel):
    vars: Set[EventStructureVar]

    def __init__(self):
        super().__init__()
        self.vars = set()

    def add_conflict(self, e: Event, ep: Event, val):
        var = ConflictVar(e, ep)
        self.vars.add(var)
        self.add_constant(repr(var), val)

    def add_enabling(self, s: Set[Event], e: Event, fn: FN):
        var = EnablingVar(s, e)
        self.vars.add(var)
        self.add(repr(var), fn)

    def add_min_enabling(self, s: Set[Event], e: Event, fn: FN):
        var = MinEnablingVar(s, e)
        self.vars.add(var)
        self.add(repr(var), fn)

    def get_es(self) -> EventStructure:
        es = EventStructure()
        for var in self.vars:
            if self.vals[repr(var)]:
                if isinstance(var, ConflictVar):
                    es.add_conflict(var.e, var.ep)
                if isinstance(var, EnablingVar):
                    es.add_enabling(var.s, var.e)
        return es
