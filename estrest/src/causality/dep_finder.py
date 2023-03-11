from typing import Callable, Set


class DependencyFinder:
    def __init__(self):
        super().__init__()
        self.visited = set()
    
    def __getitem__(self, x: str) -> bool:
        self.visited.add(x)
        return False
  
    def find(self, f: Callable) -> Set[str]:
        f(self)
        return self.visited
