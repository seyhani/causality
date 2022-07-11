from typing import Dict, Callable

VALS = Dict[str, bool]
FN = Callable[[VALS], bool]


class CausalModel:
    vals: VALS
    fns: Dict[str, FN]

    def __init__(self):
        self.vals = {}
        self.fns = {}

    def add(self, var: str, fn: FN):
        self.vals[var] = None
        self.fns[var] = fn

    def evaluate(self):
        for i in range(len(self.vals)):
            for var, val in self.vals.items():
                if val is None:
                    self.vals[var] = self.fns[var](self.vals)
