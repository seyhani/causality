from .evnet_structure_expression import EventStructureExpression
from .event_structure_writer import EventStructureWriter


class SemanticDerivationWriter:
    def __init__(self, output_file):
        self.writer = EventStructureWriter(output_file)

    def new_expr(self, label):
        expr = EventStructureExpression().prefix(label)
        print("{} = {}".format(expr.expr, expr))
        self.writer.write(expr)
        return expr

    def prefix(self, e: EventStructureExpression, label):
        expr = e.prefix(label)
        print("{} = {}".format(expr.expr, expr))
        self.writer.write(expr)
        return expr

    def sum(self, e1: EventStructureExpression, e2: EventStructureExpression):
        expr = e1.plus(e2)
        print("{} = {}".format(expr.expr, expr))
        self.writer.write(expr)
        return expr

    def product(self, e1: EventStructureExpression, e2: EventStructureExpression):
        expr = e1.times(e2)
        print("{} = {}".format(expr.expr, expr))
        self.writer.write(expr)
        return expr

    def restrict(self, expr: EventStructureExpression, name, labels):
        expr = expr.restrict(name, labels)
        print("{} = {}".format(expr.expr, expr))
        self.writer.write(expr, "{} = {}".format(name, labels).replace("\'", ""))
        return expr

    def relabel(self, expr: EventStructureExpression, name, relabeling):
        expr = expr.relabel(name, relabeling)
        print("{} = {}".format(expr.expr, expr))
        relabeling_def = "{}: {}".format(
            name, ", ".join("{}({})={}".format(name, old, new).replace("\'", "")
                            for old, new in relabeling.items())
        )
        self.writer.write(expr, relabeling_def)
        return expr

    def export(self):
        self.writer.export()
