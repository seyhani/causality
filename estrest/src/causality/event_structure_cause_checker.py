from typing import Set, List

from causality import PrimitiveEvent
from causality.cause_checker import Witness
from event import Event
from event_structure.event_structure import EventStructure
from mapper import EventStructureToCausalModelMapper
from mapper.event_structure_causal_model import EventStructureCausalModel
from utils import powerset


class EventStructureCausalChecker:
    cm: EventStructureCausalModel
    ces: List[Set[Event]]
    cause: PrimitiveEvent
    witness: Witness

    def __init__(self, es: EventStructure, ces: List[Set[Event]], cause: PrimitiveEvent, witness: Witness):
        self.ces = ces
        self.cause = cause
        self.witness = witness
        self.cm = EventStructureToCausalModelMapper(es).map()

    def check_ac1(self):
        return self.cm.satisfies(self.cause) and self.check_effect(self.cm)

    def check_ac2a(self):
        ints = {self.cause.var: self.witness.vxp}
        if self.witness.w is not None:
            ints[self.witness.w] = self.witness.vw
        cm = self.cm.intervene(ints)
        return not self.check_effect(cm)

    def check_ac2b(self):
        self.cm.evaluate()
        Z = {z: self.cm.vals[z] for z in self.cm.vals if z != self.witness.w}
        ints = {self.cause.var: self.cause.val}
        if self.witness.w is not None:
            ints[self.witness.w] = self.witness.vw
        m = self.cm.intervene(ints)
        m.evaluate()
        return self.check_effect(m.intervene({z: Z[z] for z in Z}))
        # for Zp in powerset(Z):
        #     if not self.check_effect(m.intervene({z: Z[z] for z in Zp})):
        #         return False
        # return True

    def check_effect(self, cm: EventStructureCausalModel):
        cm.evaluate()
        es = cm.get_es()
        es.build_configurations()
        return any([es.is_configuration(c) for c in self.ces])

    def is_cause(self):
        return self.check_ac1() \
               and self.check_ac2a() \
               and self.check_ac2b()
