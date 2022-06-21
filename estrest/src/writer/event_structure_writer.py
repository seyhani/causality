from .es_dto import ESDto
from .evnet_structure_expression import EventStructureExpression
from utils import sem
from .latex_writer import LatexWriter
from .word_list import WordList

OUTPUT_FILE = '../out/derivation.tex'


class EventStructureWriter:
    def __init__(self):
        self.writer = LatexWriter()

    def write_expr(self, expr):
        self.writer.write_title(sem(expr))

    def write_expr_eq(self, expr):
        self.writer.write_title("= {}: ".format(expr))

    def write_events(self, events: WordList):
        self.writer.write_sub_title("\\mathcal{{E}}= \\{ ")
        self.writer.write_words(events)
        self.writer.write_sub_title("\\}")

    def write_conflicts(self, conflicts: WordList):
        if conflicts.is_empty():
            self.writer.write_sub_title("\\# = \\emptyset")
        else:
            self.writer.write_sub_title("\\#:")
            self.writer.write_words(conflicts)
        self.writer.write_sub_title("")

    def write_enabling(self, enabling: WordList):
        if enabling.is_empty():
            self.writer.write_sub_title("\\emptyset")
        else:
            self.writer.write_sub_title("\\vdash_{{min}}:")
            self.writer.write_words(enabling)
        self.writer.write_sub_title("")

    def write_labels(self, labels: WordList):
        self.writer.write_sub_title("L=\\{")
        self.writer.write_words(labels)
        self.writer.write_sub_title("\\}")
        self.writer.write_sub_title("")

    def write_labeling(self, labeling: WordList):
        self.writer.write_sub_title("l:")
        self.writer.write_words(labeling)
        self.writer.write_sub_title("")

    def write_defs(self, defs):
        self.writer.write_title(defs)

    def write(self, es: EventStructureExpression, defs=''):
        dto = ESDto(es, defs)
        self.writer.begin()
        self.write_defs(dto.defs)
        self.write_expr(dto.expr)
        self.write_expr_eq(dto.expr_eq)
        self.write_events(dto.events)
        self.write_conflicts(dto.conflict)
        self.write_enabling(dto.enabling)
        self.write_labels(dto.labels)
        self.write_labeling(dto.labeling)
        self.writer.end()

    def export(self):
        with open(OUTPUT_FILE, "w+") as file:
            file.write(self.writer.out)
