from typing import Set

from .serializable import Serializable


class Enabling(Serializable):
    def __init__(self, enabling_set: Set, event):
        self.enabling_set = enabling_set
        self.event = event

    def to_json(self):
        return tuple([list(self.enabling_set), self.event])

    @staticmethod
    def from_json(obj):
        enabling_set = set(map(tuple, obj[0]))
        event = tuple(obj[1])
        return Enabling(enabling_set, event)

    def __eq__(self, other):
        if not isinstance(other, Enabling):
            return False
        return self.enabling_set == other.enabling_set and self.event == other.event

    def __hash__(self):
        return hash((tuple(self.enabling_set), self.event))
