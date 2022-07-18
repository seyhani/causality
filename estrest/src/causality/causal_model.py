from copy import deepcopy
from typing import Dict, Callable, Optional

VALS = Dict[str, Optional[bool]]
FN = Callable[[VALS], bool]


class PrimitiveEvent:
    var: str
    val: bool

    def __init__(self, var, val):
        self.var = var
        self.val = val

    def negate(self):
        event = deepcopy(self)
        event.val = not event.val
        return event


class CausalModel:
    vals: VALS
    fns: Dict[str, FN]

    def __init__(self):
        self.vals = {}
        self.fns = {}

    def add(self, var: str, fn: FN) -> None:
        self.vals[var] = None
        self.fns[var] = fn

    def add_constant(self, var: str, val: bool):
        self.add(var, lambda vals: val)

    def __intervene_internal(self, var, val):
        model = deepcopy(self)
        model.fns[var] = lambda vals: val
        return model

    def intervene(self, ints: Dict[str, bool]) -> 'CausalModel':
        model = self
        for var, val in ints.items():
            model = model.__intervene_internal(var, val)
        return model

    def satisfies(self, event: PrimitiveEvent, ints: VALS = None) -> bool:
        if ints is None:
            ints = {}
        m = self
        for var, val in ints.items():
            m = m.intervene({var: val})
        m.evaluate()
        return m.vals[event.var] == event.val

    def evaluate(self):
        for i in range(len(self.vals)):
            for var, val in self.vals.items():
                self.vals[var] = self.fns[var](self.vals)
