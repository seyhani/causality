from . import Event


class SyncedEvent(Event):
    def __init__(self, e0: Event, e1: Event) -> None:
        super().__init__((e0.label, e1.label))
        self.e0 = e0
        self.e1 = e1

    def get_event(self, i):
        if i == 0:
            return self.e0
        else:
            return self.e1

    def __getitem__(self, i):
        return self.get_event(i)
