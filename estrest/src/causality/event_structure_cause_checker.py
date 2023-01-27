from typing import Set, List

from causality import PrimitiveEvent
from causality.cause_checker import Witness
from event import Event
from event_structure.valid_event_structure import ValidEventStructure
from mapper import EventStructureToCausalModelMapper
from mapper.event_structure_causal_model import EventStructureCausalModel

ES_CM_EFFECT_EVENT = PrimitiveEvent('PV', False)


class EventStructureCausalChecker:
    cm: EventStructureCausalModel
    ces: List[Set[Event]]
    cause: PrimitiveEvent
    witness: Witness

    def __init__(
        self,
        es: ValidEventStructure,
        ces: List[Set[Event]],
        cause: PrimitiveEvent,
        witness: Witness
    ):
        self.ces = ces
        self.cause = cause

        self.cm = EventStructureToCausalModelMapper(es).map()
        self.__add_effect_var(ces)
        self.cm = self.cm.get_w_projection(cause, ES_CM_EFFECT_EVENT)

        if not witness.w.issubset(self.cm.vals):
            raise Exception("Invalid w for witness")
        self.witness = witness

    def __add_effect_var(self, ces):
        self.cm.add(
            ES_CM_EFFECT_EVENT.var,
            lambda _: False,
            self.__get_effect_deps(ces)
        )

    @staticmethod
    def __get_effect_deps(
        ces: List[Set[Event]]
    ) -> List[str]:
        deps = set()
        for c in ces:
            deps.update(EventStructureCausalModel.get_configuration_deps(c))
        deps = list(map(repr, deps))
        return deps

    def check_ac1(self):
        return self.cm.satisfies(self.cause) and self.check_effect(self.cm)

    def check_ac2a(self):
        ints = {self.cause.var: self.witness.vxp}
        ints.update(self.witness.vw)
        cm = self.cm.intervene(ints)
        return not self.check_effect(cm)

    def check_ac2b(self):
        self.cm.evaluate()
        Z = {
            z: self.cm.vals[z] for z in self.cm.get_var_names()
            if z != self.witness.w.union([ES_CM_EFFECT_EVENT.var])
        }
        ints = {self.cause.var: self.cause.val}
        ints.update(self.witness.vw)
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
        return es.is_valid() and any([es.is_configuration(c) for c in self.ces])

    def is_cause(self):
        return self.check_ac1() \
               and self.check_ac2a() \
               and self.check_ac2b()
