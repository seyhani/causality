from typing import Set, Dict

from causality import CausalModel
from causality.causal_model import PrimitiveEvent
from utils import powerset


class Witness:
    w: Set[str]
    vw: Dict[str, bool]
    vxp: bool

    def __init__(self, vw, vxp):
        self.w = vw.keys()
        self.vw = vw
        self.vxp = vxp


class CauseChecker:
    model: CausalModel
    cause: PrimitiveEvent
    effect: PrimitiveEvent
    witness: Witness

    def __init__(self, model, cause, effect, witness):
        self.model = model
        self.cause = cause
        self.effect = effect
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
        Z = {z: m.vals[z] for z in m.vals if z not in self.witness.w}
        ints = {self.cause.var: self.cause.val}
        ints.update(self.witness.vw)
        m = m.intervene(ints)
        m.evaluate()
        for Zp in powerset(Z):
            if not m.satisfies(self.effect, {z: Z[z] for z in Zp}):
                return False
        return True

    def check_acs(self):
        return self.check_ac1() and self.check_ac2a() and self.check_ac2b()
