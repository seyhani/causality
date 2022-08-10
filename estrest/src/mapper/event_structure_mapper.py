from itertools import combinations
from typing import Set

from causality.causal_model import VALS
from event import Event
from event_structure.valid_event_structure import ValidEventStructure
from mapper.event_structure_causal_model import EventStructureCausalModel
from mapper.event_structure_var import ConflictVar, MinEnablingVar, EnablingVar
from utils import powerset


class EventStructureToCausalModelMapper:
    def __init__(self, es: ValidEventStructure):
        self.es = es
        self.cm = EventStructureCausalModel()

    def __add_conflict_vars(self):
        for e, ep in combinations(self.es.events, 2):
            if self.es.conflicts(e, ep):
                self.cm.add_conflict(e, ep, True)
            else:
                self.cm.add_conflict(e, ep, False)

    def con(self, s: Set[Event], vals: VALS):
        result = True
        for e, ep in combinations(s, 2):
            result = result and not vals[repr(ConflictVar(e, ep))]
        return result

    def min(self, s: Set[Event], e: Event, vals: VALS):
        result = True
        for sp in powerset(self.es.events):
            if (sp < s or s < sp) and (e not in sp):
                result = result and not vals[repr(MinEnablingVar(sp, e))]
        return result

    def __add_min_en_vars(self):
        for s in powerset(self.es.events):
            for e in self.es.events:
                if e in s:
                    continue
                if self.es.min_enables(s, e):
                    self.cm.add_min_enabling(s, e, (
                        lambda s_=s, e_=e: lambda vals: self.min(s_, e_, vals) and self.con(s_, vals))())
                else:
                    self.cm.add_min_enabling(s, e, lambda vals: False)

    def __add_enabling_vars(self):
        def enabling_condition(vals, s_, e_):
            result = vals[repr(MinEnablingVar(s_, e_))]
            for ep in s_:
                result = result or vals[repr(EnablingVar(s_ - {ep}, e_))]
            result = result and self.con(s_, vals)
            return result

        for s in powerset(self.es.events):
            for e in self.es.events:
                if e in s:
                    continue
                self.cm.add_enabling(s, e, (lambda s_=s, e_=e: lambda vals: enabling_condition(vals, s_, e_))())

    def map(self) -> EventStructureCausalModel:
        self.__add_conflict_vars()
        self.__add_min_en_vars()
        self.__add_enabling_vars()
        return self.cm
