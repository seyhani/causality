from typing import Callable, Set

from causality.causal_model import VALS


class DependencyFinder:
    def __init__(self):
        self.visited = set()
    
    def __getitem__(self, x: str) -> bool:
        self.visited.add(x)
        return False
  
    def find(self, f: Callable[[VALS], bool]) -> Set[str]:
        f(self)
        return self.visited
