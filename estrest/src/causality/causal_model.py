from copy import deepcopy
from typing import Dict, Callable, Optional

VALS = Dict[str, Optional[bool]]
FN = Callable[[VALS], bool]


class PrimitiveEvent:
    var: str
    val: bool

    def __init__(self, var, val):
        if not isinstance(var, str):
            self.var = repr(var)
        else:
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

    def __intervene_internal(self, ints: Dict[str, bool]):
        model = deepcopy(self)
        for var, val in ints.items():
            model.fns[var] = (
                lambda val_=val: lambda vals: val_
            )()
        return model

    def intervene(self, ints: Dict[str, bool]) -> 'CausalModel':
        model = self
        if not set(ints.keys()).issubset(self.get_var_names()):
            raise Exception("Unknown variables")
        model = model.__intervene_internal(ints)
        return model

    def satisfies(self, event: PrimitiveEvent, ints: VALS = None) -> bool:
        if ints is None:
            ints = {}
        m = self
        m = m.intervene(ints)
        m.evaluate()
        return m.vals[event.var] == event.val

    def evaluate(self):
        for i in range(len(self.vals)):
            for var, val in self.vals.items():
                self.vals[var] = self.fns[var](self.vals)

    def get_var_names(self):
        return self.fns.keys()
