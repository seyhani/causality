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

    def intervene(self, var: str, val: bool) -> 'CausalModel':
        model = deepcopy(self)
        model.fns[var] = lambda vals: val
        return model

    def satisfies(self, event: PrimitiveEvent) -> bool:
        return self.vals[event.var] == event.val

    def evaluate(self):
        for i in range(len(self.vals)):
            for var, val in self.vals.items():
                self.vals[var] = self.fns[var](self.vals)
