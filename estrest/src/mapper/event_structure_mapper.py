from typing import Set
from itertools import combinations

from causality import CausalModel
from causality.causal_model import VALS
from event import Event
from event_structure import EventStructure
from utils import powerset, ids


class EventStructureToCausalModelMapper:
    def __init__(self, es: EventStructure):
        self.es = es

    @staticmethod
    def __conflict_var(e: Event, ep: Event):
        ids_ = ids({e, ep})
        return f'C{tuple(sorted(ids_))}'.replace('\'', '')

    def __add_conflict_vars(self, cm: CausalModel):
        for e, ep in combinations(self.es.events, 2):
            var = self.__conflict_var(e, ep)
            if self.es.conflicts(e, ep):
                cm.add_constant(var, True)
            else:
                cm.add_constant(var, False)

    def con(self, s: Set[Event], vals: VALS):
        result = True
        for e, ep in combinations(s, 2):
            result = result and not vals[self.__conflict_var(e, ep)]
        return result

    @staticmethod
    def __min_en_var(s: Set[Event], e: Event):
        ids_ = ids(s)
        return f'M{sorted(ids_), e}'.replace('\'', '')

    def min(self, s: Set[Event], e: Event, vals: VALS):
        result = True
        for sp in powerset(self.es.events):
            if (sp < s or s < sp) and (e not in sp):
                result = result and not vals[self.__min_en_var(sp, e)]
        return result

    def __add_min_en_vars(self, cm: CausalModel):
        for s in powerset(self.es.events):
            for e in self.es.events:
                if e in s:
                    continue
                var = self.__min_en_var(s, e)
                if self.es.min_en(s, e):
                    cm.add(var, lambda vals, s_=s, e_=e: self.min(s_, e_, vals) and self.con(s_, vals))
                else:
                    cm.add_constant(var, False)

    @staticmethod
    def __enabling_var(s: Set[Event], e: Event):
        ids_ = ids(s)
        return f'EN{sorted(ids_), e}'.replace('\'', '')

    def __add_enabling_vars(self, cm: CausalModel):
        def enabling_condition(vals, s_, e_):
            result = vals[self.__min_en_var(s_, e_)]
            for ep in s_:
                result = result or vals[self.__enabling_var(s_ - {ep}, e_)]
            result = result and self.con(s_, vals)
            return result

        for s in powerset(self.es.events):
            for e in self.es.events:
                if e in s:
                    continue
                var = self.__enabling_var(s, e)
                cm.add(var, lambda vals, s_=s, e_=e: enabling_condition(vals, s_, e_))

    def map(self) -> CausalModel:
        cm = CausalModel()
        self.__add_conflict_vars(cm)
        self.__add_min_en_vars(cm)
        self.__add_enabling_vars(cm)
        return cm
