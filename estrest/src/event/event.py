class Event:
    def __init__(self, label) -> None:
        self._mutations = tuple()
        self.label = label

    def prefix(self, prefix):
        self._mutations = (prefix,) + self._mutations
        return self

    def idx(self):
        if self._mutations:
            return self._mutations + (self.label,)
        else:
            return self.label

    def __repr__(self):
        return repr(self.idx()).replace("\'", "")

    def to_json(self):
        return dict(label=self.label)
