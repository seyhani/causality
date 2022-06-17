from expr_es import ExprES
from semantic_writer import LatexWriter


class Helper:
    def __init__(self):
        self.writer = LatexWriter()

    def new_expr(self, label):
        expr = ExprES().prefix(label)
        print("{} = {}".format(expr.expr, expr))
        self.writer.write(expr)
        return expr

    def prefix(self, e: ExprES, label):
        expr = e.prefix(label)
        print("{} = {}".format(expr.expr, expr))
        self.writer.write(expr)
        return expr

    def sum(self, e1: ExprES, e2: ExprES):
        expr = e1.plus(e2)
        print("{} = {}".format(expr.expr, expr))
        self.writer.write(expr)
        return expr

    def product(self, e1: ExprES, e2: ExprES):
        expr = e1.times(e2)
        print("{} = {}".format(expr.expr, expr))
        self.writer.write(expr)
        return expr

    def restrict(self, expr: ExprES, name, labels):
        expr = expr.restrict(name, labels)
        print("{} = {}".format(expr.expr, expr))
        self.writer.write(expr, "{} = {}".format(name, labels).replace("\'", ""))
        return expr

    def relabel(self, expr: ExprES, name, relabeling):
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
