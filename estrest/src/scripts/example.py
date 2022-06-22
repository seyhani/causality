from event_structure import EventStructure
from writer.semantic_derivation_writer import SemanticDerivationWriter
from utils import disjoint_relabeling

helper = SemanticDerivationWriter("derivation.tex")

c = helper.new_expr('c')
d = helper.new_expr('d')

cd = helper.product(c, d)
cd = helper.restrict(cd, "\\Lambda_1", {('c', '*'), ('*', 'd')})
cd = helper.relabel(cd, "\\Xi_1", {('c', '*'): 'A', ('*', 'd'): 'B'})

ay = helper.new_expr('y')
ay = helper.prefix(ay, 'a')

bax = helper.new_expr('x')
bax = helper.prefix(bax, 'a')
bax = helper.prefix(bax, 'b')

s1 = helper.sum(bax, ay)
s1 = helper.relabel(s1, "\\Xi_2", disjoint_relabeling({'a', 'b', 'x', 'y'}))

abx = helper.new_expr('x')
abx = helper.prefix(abx, 'b')
abx = helper.prefix(abx, 'a')

s = helper.sum(abx, s1)
s = helper.relabel(s, "\\Xi_2", disjoint_relabeling({'a', 'b', 'x', 'y'}))

r = helper.product(s, cd)
r = helper.restrict(r, "\\Lambda_2", {('a', 'A'), ('b', 'B'), ('x', '*'), ('y', '*')})

helper.export()
