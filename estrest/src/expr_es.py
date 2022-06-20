from event_structure import EventStructure
from utils import sem


class ExprES:
    def __init__(self):
        self.es = EventStructure()
        self.expr = 'nil'
        self.expr_eq = sem('nil')

    def prefix(self, alpha):
        self.expr_eq = "{}{}".format(alpha, sem(self.expr))
        self.expr = "{}{}".format(alpha, self.expr if self.expr != 'nil' else '')
        self.es = self.es.prefix(alpha)
        return self

    def plus(self, es1):
        self.expr_eq = "{} + {}".format(sem(self.expr), sem(es1.expr))
        self.expr = "({} + {})".format(self.expr, es1.expr)
        self.es = self.es.sum(es1.es)
        return self

    def times(self, es1):
        self.expr_eq = "{} \\times {}".format(sem(self.expr), sem(es1.expr))
        self.expr = "({} \\times {})".format(self.expr, es1.expr)
        self.es = self.es.product(es1.es)
        return self

    def restrict(self, name, labels):
        self.expr_eq = "{} \\lceil {}".format(sem(self.expr), name)
        self.expr = "({} \\lceil {})".format(self.expr, name)
        self.es = self.es.restrict(labels)
        return self

    def relabel(self, name, relabeling):
        self.expr_eq = "{} [{}]".format(sem(self.expr), name)
        self.expr = "({} [{}])".format(self.expr, name)
        self.es = self.es.relabel(relabeling)
        return self

    def __repr__(self):
        return "({}, {}, {}, {})".format(
            len(self.es.events),
            sum(map(len, self.es.conflict.values())),
            sum(map(len, self.es.enabling.values())),
            len(self.es.get_labels())
        )
