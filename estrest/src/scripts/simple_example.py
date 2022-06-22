from event_structure import EventStructure
from writer import SemanticDerivationWriter

writer = SemanticDerivationWriter('simple_example.tex')

e = writer.new_expr('b')
writer.prefix(e, 'a')

writer.export()
