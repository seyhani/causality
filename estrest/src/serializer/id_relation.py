from event_structure import EventStructure
from src import ids
from .serializable import Serializable
from .enabling import Enabling


class IdRelation(Serializable):
    def __init__(self, events, conflict, enabling):
        self.events = events
        self.conflict = conflict
        self.enabling = enabling

    @staticmethod
    def from_json(obj):
        events = set(map(tuple, obj['events']))
        conflict = set(map(lambda c: (tuple(c[0]), tuple(c[1])), obj['conflict']))
        enabling = set(map(lambda e: Enabling.from_json(e), obj['enabling']))
        return IdRelation(events, conflict, enabling)

    def to_json(self):
        return {
            'events': list(self.events),
            'conflict': list(self.conflict),
            'enabling': list(map(lambda e: e.to_json(), self.enabling))
        }

    def __eq__(self, other):
        if not isinstance(other, IdRelation):
            return False
        return self.events == other.events and self.conflict == other.conflict and self.enabling == other.enabling


def to_relation(event_structure: EventStructure):
    events = ids(event_structure.events)
    conflict = set([(e.idx(), ce.idx()) for e, conflict_set in event_structure.conflict.items() for ce in
                    conflict_set])
    enabling = set(
        Enabling(ids(es), e.idx()) for e, enabling_sets in event_structure.enabling.items() for es in enabling_sets)
    return IdRelation(events, conflict, enabling)
