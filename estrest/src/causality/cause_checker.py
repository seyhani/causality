from causality import CausalModel
from causality.causal_model import PrimitiveEvent


class Witness:
    w: str
    vw: bool
    vxp: bool

    def __init__(self, w, vw, vxp):
        self.w = w
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
        ints = {self.cause.var: self.witness.vxp, self.witness.w: self.witness.vw}
        return m.satisfies(self.effect.negate(), ints)
