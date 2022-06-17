class Event:
    def __init__(self, label) -> None:
        self.mutations = [label]
        self.label = label

    def mutate(self, idx):
        self.mutations.insert(0, idx)

    def disjoint(self, idx):
        self.label = (self.label, idx)

    def __repr__(self) -> str:
        if self.mutations:
            return "(" + ", ".join(list(map(lambda x: repr(x).replace("\'", ""), self.mutations))) + ")"
        else:
            return self.label


class SyncedEvent(Event):
    def __init__(self, e0, e1) -> None:
        self.e0 = e0
        self.e1 = e1
        self.label = (e0.label, e1.label)

    def __repr__(self):
        return "(" + repr(self.e0) + ", " + repr(self.e1) + ")"


STAR = Event('*')
STAR.mutations = []
