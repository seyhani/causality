import os

import jinja2

from expr_es import ExprES
from es_dto import ESDto
from utils import sem
from writer import EquationWriter, WordList


class SemanticWriter:
    def __init__(self):
        self.writer = EquationWriter()

    def write_es(self, es: ESDto):
        self.writer.begin()
        self.write_defs(es.defs)
        self.write_expr(es.expr)
        self.write_expr_eq(es.expr_eq)
        self.write_events(es.events)
        self.write_conflicts(es.conflict)
        self.write_enabling(es.enabling)
        self.write_labels(es.labels)
        self.write_labeling(es.labeling)
        self.writer.end()

    def write_expr(self, expr):
        self.writer.add_title(sem(expr))

    def write_expr_eq(self, expr):
        self.writer.add_title("= {}: ".format(expr))

    def write_events(self, events: WordList):
        self.writer.add_sub_title("\\mathcal{{E}}= \\{ ")
        self.writer.write_words(events)
        self.writer.add_sub_title("\\}")

    def write_conflicts(self, conflicts: WordList):
        if conflicts.is_empty():
            self.writer.add_sub_title("\\# = \\emptyset")
        else:
            self.writer.add_sub_title("\\#:")
            self.writer.write_words(conflicts)
        self.writer.add_sub_title("")

    def write_enabling(self, enabling: WordList):
        if enabling.is_empty():
            self.writer.add_sub_title("\\emptyset")
        else:
            self.writer.add_sub_title("\\vdash_{{min}}:")
            self.writer.write_words(enabling)
        self.writer.add_sub_title("")

    def write_labels(self, labels: WordList):
        self.writer.add_sub_title("L=\\{")
        self.writer.write_words(labels)
        self.writer.add_sub_title("\\}")
        self.writer.add_sub_title("")

    def write_labeling(self, labeling: WordList):
        self.writer.add_sub_title("l:")
        self.writer.write_words(labeling)
        self.writer.add_sub_title("")

    def get_out(self):
        return self.writer.out

    def write_defs(self, defs):
        self.writer.add_title(defs)


class LatexWriter:
    def __init__(self):
        self.writer = SemanticWriter()
        self.env = jinja2.Environment(
            block_start_string='\BLOCK{',
            block_end_string='}',
            variable_start_string='\VAR{',
            variable_end_string='}',
            comment_start_string='\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader(os.path.abspath(''))
        )

    def write(self, es: ExprES, defs=''):
        self.writer.write_es(ESDto(es, defs))

    def export(self):
        # template = self.env.get_template('latex/document.tex')
        # rendered = template.render(content=self.writer.get_out())
        with open("../out/proof.tex", "w") as file:
            file.write(self.writer.get_out())
