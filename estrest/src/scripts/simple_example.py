from event_structure import EventStructureTerm
from writer import SemanticDerivationWriter

writer = SemanticDerivationWriter('simple_example.tex')

e = writer.new_expr('b')
writer.prefix(e, 'a')

writer.export()
