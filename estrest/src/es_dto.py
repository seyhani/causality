from event_structure import ES
from expr_es import ExprES
from writer import WordList


def events_to_words(es: ES) -> WordList:
    return WordList(list(map(repr, es.events)))


def conflict_to_words(es: ES) -> WordList:
    words = WordList()
    for e, conflict in es.conflict.items():
        for ce in conflict:
            words.add("{} \\# {}".format(e, ce))
    return words


def enabling_to_words(es: ES) -> WordList:
    words = WordList()
    for e, enabling in es.enabling.items():
        for enabling_set in enabling:
            words.add("\\{{ {} \\}} \\vdash {}".format(
                ", ".join(map(repr, enabling_set)),
                e
            ))
    return words


def labels_to_words(es: ES) -> WordList:
    return WordList(list(es.get_labels()))


def labeling_to_words(es: ES) -> WordList:
    words = WordList()
    for e in es.events:
        words.add("l({}) = {}".format(e, repr(e.label).replace("\'", "")))
    return words


class ESDto:
    def __init__(self, expr_es: ExprES, defs=''):
        es = expr_es.es
        self.defs = defs
        self.expr = expr_es.expr
        self.expr_eq = expr_es.expr_eq
        self.events = events_to_words(es)
        self.conflict = conflict_to_words(es)
        self.enabling = enabling_to_words(es)
        self.labels = labels_to_words(es)
        self.labeling = labeling_to_words(es)
