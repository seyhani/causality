from copy import deepcopy
from typing import Dict, Callable, List, Optional, Set

from utils import topological_sort, path_vertices

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
    deps: Dict[str, List[str]]

    def __init__(self):
        self.vals = {}
        self.fns = {}
        self.deps = {}

    def add(self, var: str, fn: FN, deps: List[str]) -> None:
        self.vals[var] = None
        self.fns[var] = fn
        self.deps[var] = deps

    def add_constant(self, var: str, val: bool):
        self.add(var, lambda vals: val, [])

    def __intervene_internal(self, ints: Dict[str, bool]):
        model = deepcopy(self)
        for var, val in ints.items():
            model.fns[var] = (
                lambda val_=val: lambda vals: val_
            )()
            model.deps[var] = []
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

    # Inverse of the deps relation
    def __deps_inv(self):
        deps_inv = {}

        for k in self.deps:
            deps_inv[k] = []

        for k, vs in self.deps.items():
            for v in vs:
                deps_inv[v].append(k)
        return deps_inv

    def evaluate(self):
        deps_inv = self.__deps_inv()
        vars_sorted = topological_sort(deps_inv)
        for var in vars_sorted:
            self.vals[var] = self.fns[var](self.vals)

    def get_var_names(self):
        return self.fns.keys()

    def __get_w_projection_vars(self, X: str, Y: str) -> Set[str]:
        self.evaluate()
        vars_ = set()
        vars_.add(X)
        pv = path_vertices(X, Y, self.__deps_inv(), self.deps)
        for v in pv - {X}:
            vars_.add(v)
            vars_.update(self.deps[v])
        return vars_

    # W-projection is achieved with the following:
    # * Updating deps to remove any v not in projection variables
    #   from deps[u] for all u.
    # * Fixing any variable v in projection variables where deps[v] is empty
    #   (v only depended on variables not in the projection.)
    # * Removing variables not in the projection
    def get_w_projection(
        self, X: PrimitiveEvent, Y: PrimitiveEvent
    ) -> 'CausalModel':
        model = deepcopy(self)
        pv = model.__get_w_projection_vars(X.var, Y.var)

        for var in model.deps:
            deps = model.deps[var]
            model.deps[var] = list(filter(lambda v: v in pv, deps))

        for var in pv:
            if len(model.deps[var]) == 0:
                model.fns[var] = (
                    lambda val_=model.vals[var]: lambda vals: val_
                )()

        model.vals = {var: model.vals[var] for var in pv}
        model.fns = {var: model.fns[var] for var in pv}
        model.deps = {var: model.deps[var] for var in pv}

        return model
