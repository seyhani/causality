from causality import CausalModel
from event import Event


class EventStructureCausalModel(CausalModel):
    def __init__(self):
        super().__init__()

    def add_conflict_var(self, e: Event, ep: Event):

        pass


class ConflictVar:
    e: Event
    ep: Event

    def __init__(self, e: Event, ep: Event):
        self.e = e
        self.ep = ep
