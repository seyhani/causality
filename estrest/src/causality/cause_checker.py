from typing import Set, Dict

from causality import CausalModel
from causality.causal_model import PrimitiveEvent
from utils import powerset


class Witness:
    w: Set[str]
    vw: Dict[str, bool]
    vxp: bool

    def __init__(self, vw, vxp):
        self.w = set(vw.keys())
        self.vw = vw
        self.vxp = vxp


class CauseChecker:
    model: CausalModel
    cause: PrimitiveEvent
    effect: PrimitiveEvent
    witness: Witness

    def __init__(self, model, cause, effect, witness):
        self.cause = cause
        self.effect = effect

        self.model = model.get_w_projection(cause, effect)
        if not witness.w.issubset(self.model.get_var_names()):
            raise Exception("Invalid w for witness")
        self.witness = witness

    def check_ac1(self):
        m = self.model
        m.evaluate()
        return m.satisfies(self.cause) and m.satisfies(self.effect)

    def check_ac2a(self):
        m = self.model
        ints = {self.cause.var: self.witness.vxp}
        ints.update(self.witness.vw)
        return m.satisfies(self.effect.negate(), ints)

    def check_ac2b(self):
        m = self.model
        m.evaluate()
        ints = {self.cause.var: self.cause.val}
        ints.update(self.witness.vw)
        return m.satisfies(self.effect, ints)

    def check_ac2c(self):
        m = self.model
        m.evaluate()
        Z = {
            z: m.vals[z] for z in m.get_var_names()
            if z not in self.witness.w.union([self.effect.var])
        }
        ints = {self.cause.var: self.cause.val}
        ints.update(self.witness.vw)
        m = m.intervene(ints)
        return m.satisfies(self.effect, Z)

    def check_acs(self):
        return (
            self.check_ac1()
            and self.check_ac2a()
            and self.check_ac2b()
            and self.check_ac2c()
        )
